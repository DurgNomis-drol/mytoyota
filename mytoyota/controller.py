"""Toyota Connected Services Controller """
from datetime import datetime, timedelta
from http import HTTPStatus
import logging
from typing import Any, Optional, Union, Dict, List
from urllib import parse  # For parse query string, can this be done with httpx?

import httpx
import jwt

from mytoyota.const import (
    ACCESS_TOKEN_URL,
    AUTHENTICATE_URL,
    AUTHORIZE_URL,
    SUPPORTED_REGIONS,
    TIMEOUT,
)
from mytoyota.exceptions import ToyotaApiError, ToyotaInternalError, ToyotaLoginError
from mytoyota.utils.logs import censor_all

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Controller:
    """Controller class."""

    def __init__(
        self,
        locale: str,
        region: str,
        username: str,
        password: str,
        brand: str,
        uuid: Optional[str] = None,
    ) -> None:
        self._locale: str = locale
        self._region: str = region
        self._username: str = username
        self._password: str = password
        self._brand: str = brand
        self._uuid: str = uuid
        self._token: Optional[str] = None
        self._token_expiration: Optional[datetime] = None

    @property
    def _authorize_endpoint(self) -> str:
        """Returns auth endpoint."""
        return SUPPORTED_REGIONS[self._region].get(AUTHORIZE_URL)

    @property
    def _access_token_endpoint(self) -> str:
        """Returns auth endpoint."""
        return SUPPORTED_REGIONS[self._region].get(ACCESS_TOKEN_URL)

    @property
    def _authenticate_endpoint(self) -> str:
        """Returns auth endpoint."""
        return SUPPORTED_REGIONS[self._region].get(AUTHENTICATE_URL)

    #    @property
    #    def _auth_valid_endpoint(self) -> str:
    #        """Returns token is valid endpoint."""
    #        return SUPPORTED_REGIONS[self._region].get(TOKEN_VALID_URL)

    @property
    # TODO Dont think this is required outside of the controller anymore.
    def uuid(self) -> Optional[str]:
        """Return uuid."""
        return self._uuid

    async def first_login(self) -> None:
        """Perform first login."""
        await self._update_token()

    async def _update_token(self, retry: bool = True) -> None:
        """Performs login to toyota servers and retrieves token and uuid for the account."""

        _LOGGER.debug("Authenticate")
        async with httpx.AsyncClient() as client:
            # Authenticate. (Better approach as found in toyota_na, as opposed to multiple stages)
            data: dict[str, Any] = {}
            for _ in range(10):
                if "callbacks" in data:
                    for cb in data["callbacks"]:
                        if (
                            cb["type"] == "NameCallback"
                            and cb["output"][0]["value"] == "User Name"
                        ):
                            cb["input"][0]["value"] = self._username
                        elif cb["type"] == "PasswordCallback":
                            cb["input"][0]["value"] = self._password
                resp = await client.post(self._authenticate_endpoint, json=data)
                if resp.status_code != HTTPStatus.OK:
                    _LOGGER.error(
                        f"Authenticcation failed:\n"
                        f"  Status_Code = {resp.status_code}\n"
                        f"  Text        = {resp.text}\n"
                        f"  Headers     = {resp.headers}"
                    )
                    raise ToyotaLoginError("Could not authenticate")
                data = resp.json()
                if "tokenId" in data:
                    break

            if "tokenId" not in data:
                raise ToyotaLoginError("Authentication process looping")

            # Authorise
            resp = await client.get(
                self._authorize_endpoint,
                headers={"cookie": f"iPlanetDirectoryPro={data['tokenId']}"},
            )
            if resp.status_code != HTTPStatus.FOUND:
                _LOGGER.error(
                    f"Authorization failed:\n"
                    f"  Status_Code = {resp.status_code}\n"
                    f"  Text        = {resp.text}\n"
                    f"  Headers     = {resp.headers}"
                )
                raise ToyotaLoginError("Authorization failed")
            authentication_code = parse.parse_qs(
                httpx.URL(resp.headers.get("location")).query.decode()
            )["code"]

            # Retrieve tokens
            resp = await client.post(
                self._access_token_endpoint,
                headers={"authorization": "basic b25lYXBwOm9uZWFwcA=="},
                # f"basic {self.BASIC_AUTH_STRING}"},
                data={
                    "client_id": "oneapp",
                    "code": authentication_code,
                    "redirect_uri": "com.toyota.oneapp:/oauth2Callback",
                    "grant_type": "authorization_code",
                    "code_verifier": "plain",
                },
            )
            if resp.status_code != HTTPStatus.OK:
                _LOGGER.debug(
                    f"Authorization failed:\n"
                    f"  Status_Code = {resp.status_code}\n"
                    f"  Text        = {resp.text}\n"
                    f"  Headers     = {resp.headers}"
                )
                raise ToyotaLoginError("Failed to retrieve required tokens")

            access_tokens: dict[str, Any] = resp.json()
            if (
                "access_token" not in access_tokens
                or "id_token" not in access_tokens
                or "refresh_token" not in access_tokens
                or "expires_in" not in access_tokens
            ):
                raise ToyotaLoginError("Missing tokens in response")

            self._token = access_tokens["access_token"]
            self._uuid = jwt.decode(
                access_tokens["id_token"],
                algorithms=["RS256"],
                options={"verify_signature": False},
                audience="oneappsdkclient",
            )[
                "uuid"
            ]  # Usefully found in toyota_na
            self._token_expiration = datetime.now() + timedelta(
                seconds=access_tokens["expires_in"]
            )

    def _is_token_valid(self, retry: bool = True) -> bool:
        """Checks if token is valid"""
        if self._token is None:
            return False

        return self._token_expiration > datetime.now()

    async def request_raw(
        self,  # pylint: disable=too-many-branches
        method: str,
        endpoint: str,
        base_url: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        """Shared request method"""
        if method not in ("GET", "POST", "PUT", "DELETE"):
            raise ToyotaInternalError("Invalid request method provided")

        if not self._is_token_valid():
            await self._update_token()

        if base_url:
            url = SUPPORTED_REGIONS[self._region].get(base_url) + endpoint
        else:
            url = endpoint

        _LOGGER.debug("Constructing additional headers...")
        if headers is None:
            headers = {}
        headers.update(
            {
                "x-api-key": "tTZipv6liF74PwMfk9Ed68AQ0bISswwf3iHQdqcF",
                "x-guid": self._uuid,
                "guid": self._uuid,
                "authorization": f"Bearer {self._token}",
                "x-channel": "ONEAPP",
                "x-brand": self._brand.upper(),
            }
        )

        _LOGGER.debug(f"Additional headers: {censor_all(headers.copy())}")

        # Cannot authenticate with aiohttp (returns 415),
        # but it works with httpx.
        _LOGGER.debug("Creating client...")
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            _LOGGER.debug(
                f"Body: {censor_all(body) if body else body} - Parameters: {params}"
            )
            response = await client.request(
                method,
                url,
                headers=headers,
                json=body,
                params=params,
                follow_redirects=True,
            )
            if response.status_code in [
                HTTPStatus.OK,
                HTTPStatus.ACCEPTED,
            ]:
                return response

            # Errored if we get here
            import pprint

            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(response.request.method)
            pp.pprint(response.request.url)
            pp.pprint(response.request.headers)
            pp.pprint(response.request.content)

        raise ToyotaApiError(
            f"Status Code: {response.status_code}, Description: {response.reason_phrase}"
        )

    async def request_json(
        self,
        method: str,
        endpoint: str,
        base_url: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        response = await self.request_raw(
            method, endpoint, base_url, body, params, headers
        )

        return response.json()

    async def request(
        self,
        method: str,
        endpoint: str,
        base_url: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> Optional[Union[Dict[str, Any], List[Any]]]:
        # TODO possibly remove if/when fully pydantic
        response = await self.request_raw(
            method, endpoint, base_url, body, params, headers
        )
        ret: Dict[str, Any] = response.json()
        return ret

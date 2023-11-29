"""Toyota Connected Services Controller """
from datetime import datetime, timedelta
from http import HTTPStatus
import logging
from typing import Any, Dict, Optional
from urllib import parse

import httpx
import jwt

from mytoyota.exceptions import ToyotaApiError, ToyotaInternalError, ToyotaLoginError
from mytoyota.utils.logs import format_httpx_response

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Controller:
    """Controller class."""

    ACCESS_TOKEN_URL = httpx.URL(
        "HTTPS://b2c-login.toyota-europe.com/oauth2/realms/root/realms/tme/access_token"  # pylint: disable=C0301
    )
    AUTHENTICATE_URL = httpx.URL(
        "HTTPS://b2c-login.toyota-europe.com/json/realms/root/realms/tme/authenticate?authIndexType=service&authIndexValue=oneapp"  # pylint: disable=C0301
    )
    AUTHORIZE_URL = httpx.URL(
        "HTTPS://b2c-login.toyota-europe.com/oauth2/realms/root/realms/tme/authorize?client_id=oneapp&scope=openid profile write&response_type=code&redirect_uri=com.toyota.oneapp:/oauth2Callback&code_challenge=plain&code_challenge_method=plain"  # pylint: disable=C0301
    )
    API_URL = httpx.URL("HTTPS://ctpa-oneapi.tceu-ctp-prd.toyotaconnectedeurope.io")
    BASE_URL = httpx.URL("HTTPS://ctpa-oneapi.tceu-ctp-prd.toyotaconnectedeurope.io")

    def __init__(self, username: str, password: str, timeout: int = 30) -> None:
        self._username: str = username
        self._password: str = password
        self._token: Optional[str] = None
        self._token_expiration: Optional[datetime] = None
        self._refresh_token: Optional[str] = None
        self._uuid: Optional[str] = None
        self._timeout = timeout

    async def login(self) -> None:
        """Perform first login."""
        await self._update_token()

    async def _update_token(self, retry: bool = True) -> None:
        """Performs login to toyota servers and retrieves token and uuid for the account."""

        # Does this help with "Access Denied" issues?
        standard_headers: dict = {
            "accept-api-version": "resource=2.1, protocol=1.0",
            "x-brand": "T",
            "user-agent": "okhttp/4.10.0",
        }

        _LOGGER.debug("Authenticating")
        async with httpx.AsyncClient() as client:
            data: Dict[str, Any] = {}
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
                resp = await client.post(
                    self.AUTHENTICATE_URL, json=data, headers=standard_headers
                )
                _LOGGER.debug(format_httpx_response(resp))
                if resp.status_code != HTTPStatus.OK:
                    raise ToyotaLoginError(
                        f"Authentication Failed. {resp.status_code}, {resp.text}."
                    )
                data = resp.json()
                # Wait for tokenId to be returned in response
                if "tokenId" in data:
                    break

            if "tokenId" not in data:
                raise ToyotaLoginError("Authentication Failed. Unknown method.")

            # Authorise
            resp = await client.get(
                self.AUTHORIZE_URL,
                headers={"cookie": f"iPlanetDirectoryPro={data['tokenId']}"},
            )
            _LOGGER.debug(format_httpx_response(resp))
            if resp.status_code != HTTPStatus.FOUND:
                raise ToyotaLoginError(
                    f"Authorization failed. {resp.status_code}, {resp.text}."
                )
            authentication_code = parse.parse_qs(
                httpx.URL(resp.headers.get("location")).query.decode()
            )["code"]

            # Retrieve tokens
            resp = await client.post(
                self.ACCESS_TOKEN_URL,
                headers={"authorization": "basic b25lYXBwOm9uZWFwcA=="},
                data={
                    "client_id": "oneapp",
                    "code": authentication_code,
                    "redirect_uri": "com.toyota.oneapp:/oauth2Callback",
                    "grant_type": "authorization_code",
                    "code_verifier": "plain",
                },
            )
            _LOGGER.debug(format_httpx_response(resp))
            if resp.status_code != HTTPStatus.OK:
                raise ToyotaLoginError(
                    f"Token retrieval failed. {resp.status_code}, {resp.text}."
                )

            access_tokens: Dict[str, Any] = resp.json()
            if (
                "access_token" not in access_tokens
                or "id_token" not in access_tokens
                or "refresh_token" not in access_tokens
                or "expires_in" not in access_tokens
            ):
                raise ToyotaLoginError(
                    f"Token retrieval failed. Missing Tokens. {resp.status_code}, {resp.text}."
                )

            self._token = access_tokens["access_token"]
            self._refresh_token = access_tokens["refresh_token"]
            self._uuid = jwt.decode(
                access_tokens["id_token"],
                algorithms=["RS256"],
                options={"verify_signature": False},
                audience="oneappsdkclient",
            )["uuid"]
            self._token_expiration = datetime.now() + timedelta(
                seconds=access_tokens["expires_in"]
            )

    def _is_token_valid(self, retry: bool = True) -> bool:
        """Checks if token is valid"""
        if self._token or self._token_expiration is None:
            return False

        return self._token_expiration > datetime.now()

    async def request_raw(
        self,  # pylint: disable=too-many-branches
        method: str,
        endpoint: str,
        vin: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        """Shared request method"""
        if method not in ("GET", "POST", "PUT", "DELETE"):
            raise ToyotaInternalError("Invalid request method provided")

        if not self._is_token_valid():
            await self._update_token()

        if headers is None:
            headers = {}
        headers.update(
            {
                "x-api-key": "tTZipv6liF74PwMfk9Ed68AQ0bISswwf3iHQdqcF",
                "x-guid": self._uuid,
                "guid": self._uuid,
                "authorization": f"Bearer {self._token}",
                "x-channel": "ONEAPP",
                "x-brand": "T",
                "user-agent": "okhttp/4.10.0",
            }
        )
        # Add vin if passed
        if vin is not None:
            headers.update({"vin": vin})

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.request(
                method,
                f"{self.BASE_URL}{endpoint}",
                headers=headers,
                json=body,
                params=params,
                follow_redirects=True,
            )
            _LOGGER.debug(format_httpx_response(response))
            if response.status_code in [
                HTTPStatus.OK,
                HTTPStatus.ACCEPTED,
            ]:
                return response

        raise ToyotaApiError(
            f"Request Failed.  {response.status_code}, {response.text}."
        )

    async def request_json(
        self,
        method: str,
        endpoint: str,
        vin: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        response = await self.request_raw(method, endpoint, vin, body, params, headers)

        return response.json()

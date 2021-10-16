"""Token validation utilities"""
from mytoyota.const import TOKEN_LENGTH
from mytoyota.exceptions import ToyotaInvalidToken


def is_valid_token(token: str) -> bool:
    """Checks if token is the correct length"""
    if token and len(token) == TOKEN_LENGTH and token.endswith("..*"):
        return True

    raise ToyotaInvalidToken(
        f"Token must end with '..*' and be {TOKEN_LENGTH} characters long."
    )

import jwt

from app.config.jwt import jwt_settings


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(
        token,
        jwt_settings.public_key,
        algorithms=[jwt_settings.algorithm],
    )

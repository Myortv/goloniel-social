from typing import Annotated

from jwt.exceptions import ExpiredSignatureError
from fastapi import Header, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.configs import token_manager, settings

from app.controllers.user_profile import _get_full_profile
from app.schemas.user_profile import Profile


# oauth_scheme = OAuth2PasswordBearer('/token/refresh')
oauth_scheme = OAuth2PasswordBearer(settings.refresh_token_url)


async def identify_request(token: str = Depends(oauth_scheme)):
    if token:
        try:
            decoded_token = token_manager.get_content(token)
            full_profile = Profile(
                **(await _get_full_profile(decoded_token['sub'])),
                role=decoded_token['role'],
            )
            return full_profile
        except ExpiredSignatureError:
            raise HTTPException(403, "Expired signature")
    raise HTTPException(403, "No token?")


async def parse_token(token: str = Depends(oauth_scheme)):
    if token:
        try:
            decoded_token = token_manager.get_content(token)
            return decoded_token
        except ExpiredSignatureError:
            raise HTTPException(403, "Expired signature")
    raise HTTPException(403, "No token?")


async def identify_user(real_user_id: int):
    return Profile(
        **(await _get_full_profile(real_user_id)),
        role=None,
    )

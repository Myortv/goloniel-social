from typing import Optional, List

from datetime import timedelta

from os.path import dirname, abspath, join

import aiohttp
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator

from cryptography.hazmat.primitives import serialization

from fastapiplugins.token import TokenManager


BASE_DIR = dirname(dirname(dirname(abspath(__file__))))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='env.sh', env_file_encoding='utf-8')

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = 'Goloniel Social'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]
    DOCS_URL: str = '/docs'

    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: Optional[str] = 'localhost'

    ADMIN_ROLES: Optional[List[str]] = ['admin', 'internal service']
    # SUSPENDED_ROLE_STRING: Optional[str] = 'suspended'

    refresh_token_url: str = 'http://test.goloniel.org/auth/api/v1/token/refresh'
    # email_url: str = 'http://?/v1/user/closed/get-by-email'
    # save_url: str = 'http://?/v1/user/closed'
    # change_pass: str = 'http://?/v1/user/closed/password-change'

    PUBLIC_JWT_KEY: Optional[str] = None
    JWT_ALGORITHM: str = 'RS256'

    # API_JWT_KEY: Optional[str] = None
    # API_JWT_AGORITHM: str = 'HS256'
    # api_token: Optional[str] = None

    AIOHTTP_SESSION: Optional[aiohttp.ClientSession] = None

    RABBITMQ_HOST: Optional[str] = 'localhost'
    RABBITMQ_PORT: Optional[int] = 5672
    RABBITMQ_USER: Optional[str] = 'guest'
    RABBITMQ_PASSWORD: Optional[str] = 'guest'

    GROUP_MEMBERSHIP_REQUEST_ACCEPTED: Optional[str] = 'ACCEPTED'

    @property
    def aiohttp_session(self):
        if not self.AIOHTTP_SESSION:
            self.AIOHTTP_SESSION = aiohttp.ClientSession()
        return self.AIOHTTP_SESSION

    def load_public_key(self):
        if not self.PUBLIC_JWT_KEY:
            with open(join(BASE_DIR, 'public_key.pem'), 'rb') as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                )
                self.PUBLIC_JWT_KEY = public_key
        return self.PUBLIC_JWT_KEY

    def load_privat_key(self):
        if not self.PRIVATE_JWT_KEY:
            with open(join(BASE_DIR, 'private_key.pem'), 'rb') as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=bytes(self.PEM_PASS, 'utf-8'),
                )
                self.PRIVATE_JWT_KEY = private_key
        return self.PRIVATE_JWT_KEY

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls,
        v: str | List[str]
    ) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
settings.load_public_key()

tags_metadata = [
    {
        "name": "Master",
        "description": ". . .",
    },
    {
        "name": "Master Rating",
        "description": ". . .",
    },
    {
        "name": "Master Approval",
        "description": ". . .",
    },
    {
        "name": "Group",
        "description": ". . .",
    },
    {
        "name": "Fraction",
        "description": ". . .",
    },
    {
        "name": "Fraction Roles",
        "description": ". . .",
    },
    {
        "name": "User Profile",
        "description": "User profile related endpoints.\n"
        "Usually you don't need this endpoints, because "
        "rabbit handle sincronization between microservices.",
    },
    {
        "name": "Group",
        "description": "Group represents one party of players\n"
        "Group has it's master. Master is persistent for group.\n"
        "There lays all endpoints related to managing group itself.",
    },
    {
        "name": "Group Membership",
        "description": "testtest",
    },
]


token_manager = TokenManager(
    # settings.PRIVATE_JWT_KEY,
    None,
    settings.PUBLIC_JWT_KEY,
    settings.JWT_ALGORITHM,
)

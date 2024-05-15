import berserk
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    lichess_api_token: str = ""


settings = Settings()


def get_client(lichess_api_token):
    if not lichess_api_token:
        lichess_api_token = settings.lichess_api_token
    session = berserk.TokenSession(lichess_api_token)
    client = berserk.Client(session=session)
    return client, lichess_api_token

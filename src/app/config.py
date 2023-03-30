from typing import Optional

from src.app.utils.schemas_utils import AbstractSettings, BaseModel, EmailStr


class DBSettings(AbstractSettings):
    """Database Settings

    Args:
        AbstractSettings (_type_): inherits Core settings.
    """

    name: str
    username: str
    password: str
    hostname: str
    port: int


class AuthSettings(AbstractSettings):
    """Authentication Settings

    Args:
        AbstractSettings (_type_): inherits Core settings.
    """

    access_secret_key: str
    refresh_secret_key: str
    access_time_exp: int
    refresh_time_exp: int
    algorithm: str


class TestSettings(AbstractSettings):
    should_test: Optional[bool]


db_settings = DBSettings()
auth_settings = AuthSettings()
test_status = TestSettings()

from enum import Enum

from pydantic import BaseModel, BaseSettings, EmailStr


class AbstractModel(BaseModel):
    """Schema Models

    Args:
        BaseModel (_type_): Inherits from Pydantic and specifies Config
    """

    class Config:
        orm_mode = True
        use_enum_values = True


class AbstractSettings(BaseSettings):
    """Settings Models

    Args:
        BaseModel (_type_): Inherits from Pydantic and specifies Config
    """

    class Config:
        env_file = ".env"


class ResponseModel(AbstractModel):
    """Base Response Models

    Args:
        BaseModel (_type_): Inherits from Pydantic and specifies Config
    """

    message: str
    status: int


class StatusOptions(Enum):
    sent = "Sent"
    accepted = "Accepted"
    rejected = "Rejected"
    reverted = "Reverted"


class User(AbstractModel):
    """User Schema Models

    Args:
        BaseModel (_type_): Inherits from Pydantic and specifies Config
    """

    first_name: str
    last_name: str
    username: str
    email: EmailStr

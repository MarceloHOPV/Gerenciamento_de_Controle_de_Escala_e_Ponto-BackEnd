from pydantic import BaseModel

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: str

class TokenData(BaseModel):
    username: str | None = None
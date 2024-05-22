from pydantic import BaseModel


class WelcomeObject(BaseModel):
    welcome_text: str

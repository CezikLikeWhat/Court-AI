from pydantic import BaseModel


class WelcomeObject(BaseModel):
    welcome_text: str


class OutputModel(BaseModel):
    liczba: int
    tekst: str

from pydantic import BaseModel


class ConfirmBodySchema(BaseModel):
    to: str
    text: str
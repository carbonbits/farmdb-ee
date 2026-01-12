from pydantic import BaseModel


class Farm(BaseModel):
    name: str
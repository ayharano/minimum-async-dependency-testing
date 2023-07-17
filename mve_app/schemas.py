from pydantic import BaseModel


class T1Schema(BaseModel):
    name: str
    character: str

    class Config:
        orm_mode = True

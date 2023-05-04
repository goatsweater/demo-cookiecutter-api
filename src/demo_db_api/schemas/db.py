from typing import Optional
from pydantic import BaseModel, constr

class Meta(BaseModel):
    series: constr(to_upper=True, min_length=1, max_length=128)
    attribute: constr(min_length=1, max_length=256)
    value: Optional[str]

    class Config:
        orm_mode = True


class Data(BaseModel):
    series: constr(to_upper=True, min_length=1, max_length=128)
    refperiod: constr(to_upper=True, min_length=1, max_length=20)
    value: float
    status: constr(to_upper=True, min_length=1, max_length=2)

    class Config:
        orm_mode = True


class Control(BaseModel):
    id: constr(min_length=1, max_length=200)
    value: Optional[str]

    class Config:
        orm_mode = True
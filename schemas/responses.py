from pydantic import BaseModel

from schemas.beens import SBeen


class SBeenResponse(BaseModel):
    status_code: int
    been: SBeen

class SBeensResponse(BaseModel):
    status_code: int
    beens: list[SBeen]


class SBaseResponse(BaseModel):
    status_code: int
    detail: str
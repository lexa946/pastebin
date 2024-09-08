from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict


class SBeenAdd(BaseModel):
    text: str
    expire: datetime | None = datetime.now() + timedelta(minutes=20)
    delete_it: bool = False


    model_config = {
        "json_schema_extra": {
            "examples": [
                {"text": "My seconds shared text!",
                 "expire": "2024-09-07T22:20:55.384477",
                 "delete_it": False,
                 },
            ]
        }
    }


class SBeen(SBeenAdd):
    id: int
    hash: str

    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "examples": [
            {"text": "My shared text!",
             "expire": "2024-09-07T22:20:55.384477",
             "hash": "484fdfd4-0ee4-4ee4-b4fd-161f5b49aaf9",
             "id": 1,
             },
        ]
    })
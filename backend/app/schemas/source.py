from base import BaseModel


class Source(BaseModel):
    id: int | None = None
    name: str
    url: str
    type: str | None = None


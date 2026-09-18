from base import BaseModel

class Strain(BaseModel):
    id: int | None = None
    name: str
    strain_type: str | None = None
    genetics: str | None = None
    model_config = {
        "from_attributes": True
    }


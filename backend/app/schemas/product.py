from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=180)
    asin: str = Field(min_length=5, max_length=20)
    marketplace: str = Field(default="US", max_length=40)
    selling_price: float = Field(gt=0)
    profit_margin_percent: float = Field(ge=0, le=100)
    target_acos_percent: float = Field(gt=0, le=100)


class ProductUpdate(BaseModel):
    name: str | None = None
    marketplace: str | None = None
    selling_price: float | None = Field(default=None, gt=0)
    profit_margin_percent: float | None = Field(default=None, ge=0, le=100)
    target_acos_percent: float | None = Field(default=None, gt=0, le=100)


class ProductResponse(BaseModel):
    id: int
    name: str
    asin: str
    marketplace: str
    selling_price: float
    profit_margin_percent: float
    target_acos_percent: float

    model_config = {
        "from_attributes": True
    }
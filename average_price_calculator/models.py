"""Pydantic models for the calculator."""

from pydantic import BaseModel, ConfigDict, Field


class PriceData(BaseModel):
    """Data model for price calculation."""

    initial_quantity: float = Field(
        ...,
        gt=0,
        description="Initial quantity",
        examples=[4.37562],
        json_schema_extra={"example": 4.37562},
    )
    initial_price: float = Field(
        ...,
        gt=0,
        description="Initial average price",
        examples=[3.602],
        json_schema_extra={"example": 3.602},
    )
    new_quantity: float = Field(
        ...,
        gt=0,
        description="Newly purchased quantity",
        examples=[2.93867],
        json_schema_extra={"example": 2.93867},
    )
    new_price: float = Field(
        ...,
        gt=0,
        description="New purchase price",
        examples=[2.11],
        json_schema_extra={"example": 2.11},
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "initial_quantity": 4.37562,
                "initial_price": 3.602,
                "new_quantity": 2.93867,
                "new_price": 2.11,
            }
        }
    )


class CalculationResult(BaseModel):
    """Result model for average price calculation."""

    average_price: float = Field(..., description="Weighted average price")
    total_quantity: float = Field(..., description="Total quantity after purchase")
    total_investment: float = Field(..., description="Total investment amount")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "average_price": 2.956,
                "total_quantity": 7.31429,
                "total_investment": 21.617,
            }
        }
    )

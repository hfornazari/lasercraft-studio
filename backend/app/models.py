from pydantic import BaseModel, Field, model_validator


class MatrixConfig(BaseModel):
    width_mm: float = Field(default=350, gt=0, le=350)
    height_mm: float = Field(default=275, gt=0, le=275)
    margin_mm: float = Field(default=5, ge=0, le=50)

    @model_validator(mode="after")
    def validate_margin(self):
        if 2 * self.margin_mm >= min(self.width_mm, self.height_mm):
            raise ValueError("Margem deve ser menor que metade de cada dimensão")
        return self

    @property
    def usable_width_mm(self) -> float:
        return self.width_mm - 2 * self.margin_mm

    @property
    def usable_height_mm(self) -> float:
        return self.height_mm - 2 * self.margin_mm


class FitRequest(BaseModel):
    source_width: float = Field(gt=0)
    source_height: float = Field(gt=0)
    matrix: MatrixConfig = Field(default_factory=MatrixConfig)


class FitResponse(BaseModel):
    scale: float
    width_mm: float
    height_mm: float
    x_mm: float
    y_mm: float

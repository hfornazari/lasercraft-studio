from .models import FitRequest, FitResponse


def fit_contain(request: FitRequest) -> FitResponse:
    """Proportional fit, centered inside safe area, coordinates from bed top-left."""
    bed = request.matrix
    scale = min(bed.usable_width_mm / request.source_width,
                bed.usable_height_mm / request.source_height)
    width = request.source_width * scale
    height = request.source_height * scale
    return FitResponse(scale=scale, width_mm=width, height_mm=height,
                       x_mm=bed.margin_mm + (bed.usable_width_mm - width) / 2,
                       y_mm=bed.margin_mm + (bed.usable_height_mm - height) / 2)

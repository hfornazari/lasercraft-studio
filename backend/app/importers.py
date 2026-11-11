"""Metadata-only import. Never execute uploaded SVG or infer manufacturing paths."""
from io import BytesIO
import re
from collections import Counter
from PIL import Image, UnidentifiedImageError
from defusedxml import ElementTree as ET

MAX_BYTES = 10 * 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# Block remote references and potentially active SVG content conservatively.
FORBIDDEN_TAGS = {"script", "foreignObject", "iframe", "image", "use", "animate", "set", "animateMotion", "animateTransform", "style", "feImage", "a"}
LENGTH_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(px|mm|cm|in|pt)?\s*$", re.I)


def _svg_length(value: str | None) -> float | None:
    if not value:
        return None
    match = LENGTH_RE.fullmatch(value)
    if not match:
        return None
    value, unit = match.groups()
    return float(value) * {None: 1, "px": 1, "mm": 96/25.4,
                           "cm": 960/25.4, "in": 96, "pt": 96/72}[unit.lower() if unit else None]


def inspect_svg(content: bytes) -> dict:
    if b"<!DOCTYPE" in content.upper() or b"<!ENTITY" in content.upper():
        raise ValueError("DTD e entidades não são aceitas")
    try:
        root = ET.fromstring(content)
    except Exception as exc:
        raise ValueError("SVG inválido") from exc
    if root.tag.split("}")[-1] != "svg":
        raise ValueError("Elemento raiz não é svg")
    for element in root.iter():
        tag = element.tag.split("}")[-1]
        if tag in FORBIDDEN_TAGS or tag.lower() in {x.lower() for x in FORBIDDEN_TAGS}:
            raise ValueError(f"Elemento SVG não permitido: {tag}")
        for key, val in element.attrib.items():
            key_lower = key.lower().split("}")[-1]
            if key_lower.startswith("on") or key_lower == "href" or "url(" in val.lower() or "@import" in val.lower():
                raise ValueError("Referência externa ou atributo executável no SVG")
    view_box = root.attrib.get("viewBox")
    vb = None
    if view_box:
        try:
            values = [float(x) for x in re.split(r"[\s,]+", view_box.strip())]
            if len(values) == 4 and values[2] > 0 and values[3] > 0:
                vb = values
        except ValueError:
            pass
    width = _svg_length(root.attrib.get("width"))
    height = _svg_length(root.attrib.get("height"))
    if (not width or not height) and vb:
        width, height = width or vb[2], height or vb[3]
    if not width or not height or width <= 0 or height <= 0 or width > 100000 or height > 100000:
        raise ValueError("SVG precisa de dimensões válidas em width/height ou viewBox")
    return {"type": "svg", "width": width, "height": height,
            "units": "css-px", "colors": [], "preview_svg": content.decode("utf-8")}


def inspect_png(content: bytes) -> dict:
    if not content.startswith(PNG_SIGNATURE):
        raise ValueError("Assinatura PNG inválida")
    try:
        with Image.open(BytesIO(content)) as img:
            if img.format != "PNG":
                raise ValueError("Formato não é PNG")
            if img.width * img.height > 25_000_000:
                raise ValueError("PNG excede limite de 25 megapixels")
            img.load()
            width, height = img.size
            thumb = img.convert("RGBA")
            thumb.thumbnail((256, 256))
            counts = Counter()
            for r, g, b, a in thumb.get_flattened_data() if hasattr(thumb, "get_flattened_data") else thumb.getdata():
                if a < 16:
                    continue
                key = "#%02x%02x%02x" % ((r//32)*32, (g//32)*32, (b//32)*32)
                counts[key] += 1
    except (OSError, UnidentifiedImageError) as exc:
        raise ValueError("PNG inválido ou corrompido") from exc
    return {"type": "png", "width": width, "height": height,
            "units": "pixels", "colors": [{"hex": k, "pixels": v} for k, v in counts.most_common(12)]}


def inspect_upload(filename: str, content: bytes) -> dict:
    if not content or len(content) > MAX_BYTES:
        raise ValueError("Arquivo vazio ou maior que 10 MiB")
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext == "png":
        return inspect_png(content)
    if ext == "svg":
        return inspect_svg(content)
    raise ValueError("Aceitos apenas arquivos .png e .svg")

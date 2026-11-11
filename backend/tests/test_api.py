from io import BytesIO
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app

client = TestClient(app)


def test_default_matrix():
    response = client.get("/api/matrix/default")
    assert response.status_code == 200
    assert response.json()["usable_width_mm"] == 340
    assert response.json()["usable_height_mm"] == 265


def test_fit_contain():
    result = client.post("/api/geometry/fit", json={"source_width": 100, "source_height": 100}).json()
    assert result["width_mm"] == 265
    assert result["height_mm"] == 265
    assert result["x_mm"] == 42.5
    assert result["y_mm"] == 5


def test_bad_margin():
    response = client.post("/api/geometry/fit", json={"source_width": 10,"source_height": 10,
        "matrix": {"width_mm": 20,"height_mm": 20,"margin_mm": 10}})
    assert response.status_code == 422


def test_inspect_png():
    image = Image.new("RGB", (40, 20), "red")
    out = BytesIO(); image.save(out, format="PNG")
    response = client.post("/api/import/inspect", files={"file": ("test.png", out.getvalue(), "image/png")})
    assert response.status_code == 200
    assert response.json()["width"] == 40
    assert response.json()["height"] == 20


def test_inspect_svg():
    svg = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 40"><rect width="80" height="40"/></svg>'
    response = client.post("/api/import/inspect", files={"file": ("test.svg", svg, "image/svg+xml")})
    assert response.status_code == 200
    assert response.json()["type"] == "svg"
    assert response.json()["width"] == 80


def test_reject_script_svg():
    svg = b'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><script>alert(1)</script></svg>'
    response = client.post("/api/import/inspect", files={"file": ("bad.svg", svg, "image/svg+xml")})
    assert response.status_code == 422


def test_reject_png_disguised_as_svg():
    response = client.post("/api/import/inspect", files={"file": ("bad.png", b"notpng", "image/png")})
    assert response.status_code == 422

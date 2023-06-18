#!/usr/bin/env python3
import json
from pathlib import Path

from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from main import app


def main():
    out_dir = Path("build")
    if not out_dir.exists():
        out_dir.mkdir()
    with Path(out_dir, "openaip.json").open("w") as f:
        json.dump(
            get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                routes=app.routes,
            ),
            f,
        )
    with Path(out_dir, "index.html").open("wb") as f:
        text = get_redoc_html(
            openapi_url="openapi.json", title=app.title + " - ReDoc"
        ).body
        f.write(text)
    with Path(out_dir, "docs.html").open("wb") as f:
        text = get_swagger_ui_html(
            openapi_url="openapi.json", title=app.title + " - Swagger UI"
        ).body
        f.write(text)


if __name__ == "__main__":
    main()

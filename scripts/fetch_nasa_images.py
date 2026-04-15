from __future__ import annotations

import io
import json
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image


OUTPUT_DIR = Path("assets/photos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGES = [
    {
        "slug": "featured-launch-pad",
        "collection_url": "https://images-assets.nasa.gov/image/KSC-20260210-PH-JBS01-0074/collection.json",
        "max_width": 1600,
    },
    {
        "slug": "launch-pad-wide",
        "collection_url": "https://images-assets.nasa.gov/image/KSC-20260210-PH-JBS01-0205/collection.json",
        "max_width": 1200,
    },
    {
        "slug": "moon-behind-stack",
        "collection_url": "https://images-assets.nasa.gov/image/Artemis%20II%20at%20the%20pad%20Moon%2001292026_4/collection.json",
        "max_width": 1200,
    },
    {
        "slug": "full-moon-rise",
        "collection_url": "https://images-assets.nasa.gov/image/Artemis%20II%20at%20the%20pad%20Full%20Snow%20Moon%2002012026_6/collection.json",
        "max_width": 1200,
    },
    {
        "slug": "crew-with-egs",
        "collection_url": "https://images-assets.nasa.gov/image/KSC-20230807-PH-KLS01_0518/collection.json",
        "max_width": 1200,
    },
    {
        "slug": "crew-recovery",
        "collection_url": "https://images-assets.nasa.gov/image/JB5_0746/collection.json",
        "max_width": 1200,
    },
    {
        "slug": "orion-delivery-a",
        "collection_url": "https://images-assets.nasa.gov/image/KSC-20230602-PH-GEB01-0019/collection.json",
        "max_width": 1200,
    },
    {
        "slug": "orion-delivery-b",
        "collection_url": "https://images-assets.nasa.gov/image/KSC-20230602-PH-GEB01-0056/collection.json",
        "max_width": 1200,
    },
    {
        "slug": "crew-with-egs-wide",
        "collection_url": "https://images-assets.nasa.gov/image/KSC-20230807-PH-KLS01_0511/collection.json",
        "max_width": 1200,
    },
]


def pick_asset_url(collection: list[str]) -> str:
    priorities = ("~large.jpg", "~orig.JPG", "~orig.jpg", "~medium.jpg", ".jpg", ".jpeg")
    for suffix in priorities:
        for item in collection:
            if item.lower().endswith(suffix.lower()):
                return item
    raise RuntimeError("No JPG asset found in collection payload.")


def download_json(url: str):
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def download_bytes(url: str) -> bytes:
    parts = urllib.parse.urlsplit(url)
    safe_url = urllib.parse.urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            urllib.parse.quote(parts.path),
            parts.query,
            parts.fragment,
        )
    )
    with urllib.request.urlopen(safe_url, timeout=60) as response:
        return response.read()


def resize_and_save(image_bytes: bytes, output_path: Path, max_width: int) -> None:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = image.size
    if width > max_width:
        resized_height = int(height * (max_width / width))
        image = image.resize((max_width, resized_height), Image.LANCZOS)
    image.save(output_path, "WEBP", quality=82, method=6)


def main() -> None:
    manifest = []
    for item in IMAGES:
        collection = download_json(item["collection_url"])
        asset_url = pick_asset_url(collection)
        output_path = OUTPUT_DIR / f"{item['slug']}.webp"
        resize_and_save(download_bytes(asset_url), output_path, item["max_width"])
        manifest.append(
            {
                "slug": item["slug"],
                "source": item["collection_url"],
                "asset": asset_url,
                "output": str(output_path),
            }
        )
        print(f"saved {output_path}")

    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote {manifest_path}")


if __name__ == "__main__":
    main()

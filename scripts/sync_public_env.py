from __future__ import annotations

import json
import sys
from pathlib import Path


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        raise SystemExit(f"missing env file: {path}")

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def main() -> None:
    env_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".env.production")
    out_path = Path(sys.argv[2] if len(sys.argv) > 2 else "assets/public-env.js")
    dotenv = load_dotenv(env_path)

    payload = {
        "webUrl": dotenv.get("NEXT_PUBLIC_WEB_URL", ""),
        "projectName": dotenv.get("NEXT_PUBLIC_PROJECT_NAME", ""),
        "googleAnalyticsId": dotenv.get("NEXT_PUBLIC_GOOGLE_ANALYTICS_ID", ""),
        "clarityProjectId": dotenv.get("NEXT_PUBLIC_CLARITY_PROJECT_ID", ""),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        "window.__ARTEMIS_PUBLIC_ENV__ = " + json.dumps(payload, indent=2) + ";\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

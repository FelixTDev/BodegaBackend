from pathlib import Path
import sys

from dotenv import load_dotenv
import uvicorn


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    (root / ".e2e").mkdir(exist_ok=True)
    env_path = root / ".env.e2e"
    load_dotenv(env_path, override=True)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8100, reload=False)


if __name__ == "__main__":
    main()

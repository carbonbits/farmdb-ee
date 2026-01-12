from pathlib import Path
import tomllib


def get_version_from_pyproject() -> str:
    try:
        root_dir = Path(__file__).resolve().parents[2]
        pyproject_path = root_dir / "pyproject.toml"

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            
            return data["project"]["version"]
    except Exception:
        return "0.1.0"

from pathlib import Path
import os

DEFAULT_CONFIG = Path(os.getenv("SEARCH_ENGINE_CONFIG", "config/development.yaml"))

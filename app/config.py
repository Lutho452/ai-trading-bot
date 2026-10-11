from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = APP_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

DEFAULT_SYMBOL = "BTCUSD"
DEFAULT_PERIODS = 250

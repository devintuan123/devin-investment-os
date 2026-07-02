from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.snapshot_store import save_snapshot


if __name__ == "__main__":
    print(save_snapshot())

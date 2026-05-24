from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if ROOT_DIR not in [Path(p).resolve() for p in sys.path if p]:
    sys.path.insert(0, str(ROOT_DIR))

from core.models.model_manager import ModelManager
from core.voice.voice_manager import VoiceManager


def run_checks() -> None:
    print("\n=== Thalexa Setup Check ===\n")

    model_manager = ModelManager()
    model_manager.ensure_models()

    voice_manager = VoiceManager()
    voice_manager.ensure_voice_runtime()
    voice_manager.test_wake_cycle()

    print("\n=== Setup check complete ===\n")


if __name__ == "__main__":
    run_checks()

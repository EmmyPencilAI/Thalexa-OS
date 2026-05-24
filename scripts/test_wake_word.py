from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if ROOT_DIR not in [Path(p).resolve() for p in sys.path if p]:
    sys.path.insert(0, str(ROOT_DIR))

from core.voice.voice_manager import VoiceManager


def main() -> None:
    print("=== Thalexa Wake Word Test ===")
    voice_manager = VoiceManager()
    voice_manager.ensure_voice_runtime()

    if not voice_manager.available:
        print("Voice runtime is not ready. Fix the missing dependencies and try again.")
        return

    print("Using local Whisper model:", voice_manager.stt_model)
    if voice_manager.can_start_listening():
        print("Speak clearly for a few seconds after the recording starts.")
        print("Thalexa will keep listening until the wake word is detected or you stop the script.")
        voice_manager.run_wake_word_loop(duration_seconds=5)
    elif voice_manager.vad_available:
        print("Voice transcription runtime is not ready, but silero-vad is available for VAD-only listening.")
        print("Thalexa will now continuously monitor audio and report speech activity.")
        voice_manager.run_vad_listen_loop(duration_seconds=5)
    else:
        print("Wake-word listening is not active because the STT runtime or model path is not ready.")
        print("Install a compatible local whisper runtime or use a converted model directory to enable it.")


if __name__ == "__main__":
    main()

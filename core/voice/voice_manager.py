from importlib import util
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


class VoiceManager:
    DEFAULT_STT_MODEL = Path("models/whisper-tiny-q4_0.gguf")

    def __init__(self, wake_word: str = "Thalexa", stt_model: str | Path | None = None):
        self.wake_word = wake_word
        self.stt_model = Path(stt_model) if stt_model else self.DEFAULT_STT_MODEL
        self.available, self.missing = self._detect_runtime()
        self.vad_available = any(util.find_spec(pkg) for pkg in ["silero_vad"])
        self._speech_model = None
        self._vad_model = None
        self._silero_vad = None

    def _detect_runtime(self) -> tuple[bool, list[str]]:
        required = ["faster_whisper"]
        audio_backends = ["sounddevice", "pyaudio"]
        missing = []

        for package_name in required:
            if util.find_spec(package_name) is None:
                missing.append(package_name)

        if not any(util.find_spec(backend) for backend in audio_backends):
            missing.append("sounddevice or pyaudio")

        return (len(missing) == 0, missing)

    def ensure_voice_runtime(self) -> bool:
        if self.available:
            print("Voice runtime is available.")
            if not self.stt_model.exists():
                print(f"Speech transcription model not found: {self.stt_model}")
                print("Download a Whisper GGUF model and place it at this path, or update the path in the voice manager.")
            elif self.stt_model.suffix.lower() == ".gguf":
                if not any(util.find_spec(pkg) for pkg in ["whisper_cpp", "whispercpp"]):
                    print("Local GGUF model support requires a Whisper C++ runtime package such as whisper_cpp or whispercpp.")
            if self.vad_available:
                print("Voice activity detection is available via silero-vad.")
            else:
                print("Voice activity detection is not enabled. Install silero-vad to improve wake-word listening.")
            return True

        print("Voice runtime is not fully available.")
        print("Install or enable the following packages:")
        for item in self.missing:
            print(f" - {item}")
        print("Optional but recommended:")
        print(" - webrtcvad (for voice activity detection)")
        print(" - piper or another TTS runtime")
        return False

    def _load_speech_model(self):
        if self._speech_model is not None:
            return self._speech_model

        if not self.stt_model.exists():
            return None

        if self.stt_model.suffix.lower() == ".gguf":
            try:
                import whisper_cpp as wc
            except ImportError:
                try:
                    import whispercpp as wc
                except ImportError:
                    print(
                        "Local GGUF model paths require a Whisper C++ runtime package such as `whisper_cpp` or `whispercpp`."
                    )
                    return None

            try:
                self._speech_model = wc.WhisperModel(str(self.stt_model))
                return self._speech_model
            except Exception as exc:
                print(f"Failed to load GGUF model with Whisper C++ binding: {exc}")
                return None

        try:
            from faster_whisper import WhisperModel
        except ImportError:
            return None

        if self.stt_model.is_dir():
            self._speech_model = WhisperModel(str(self.stt_model), device="cpu", compute_type="int8")
            return self._speech_model

        return None

    def _load_vad_model(self):
        if self._vad_model is not None:
            return self._vad_model

        if not self.vad_available:
            return None

        try:
            import silero_vad
        except ImportError:
            return None

        try:
            self._vad_model = silero_vad.load_silero_vad()
            self._silero_vad = silero_vad
            return self._vad_model
        except Exception as exc:
            print(f"Unable to initialize silero-vad model: {exc}")
            return None

    def _vad_has_speech(self, audio, samplerate: int = 16000) -> bool:
        vad_model = self._load_vad_model()
        if vad_model is None:
            return True

        try:
            import numpy as np
            import torch
        except ImportError as exc:
            print(f"Cannot run silero-vad because a required package is missing: {exc}")
            return True

        audio_tensor = torch.from_numpy(audio.astype("float32")) if isinstance(audio, np.ndarray) else torch.tensor(audio, dtype=torch.float32)
        if audio_tensor.ndim > 1:
            audio_tensor = audio_tensor.mean(dim=-1)

        if audio_tensor.dtype != torch.float32:
            audio_tensor = audio_tensor.float()

        timestamps = self._silero_vad.get_speech_timestamps(
            audio_tensor,
            vad_model,
            sampling_rate=samplerate,
            threshold=0.5,
        )

        has_speech = bool(timestamps)
        print(f"Silero VAD detected {'speech' if has_speech else 'no speech'} in audio.")
        return has_speech

    def detect_speech_audio(self, duration_seconds: int = 5, samplerate: int = 16000) -> bool:
        audio = self.record_audio(duration_seconds=duration_seconds, samplerate=samplerate)
        return self._vad_has_speech(audio, samplerate)

    def can_start_listening(self) -> bool:
        if not self.available:
            return False

        if not self.stt_model.exists():
            return False

        if self.stt_model.suffix.lower() == ".gguf":
            return any(util.find_spec(pkg) for pkg in ["whisper_cpp", "whispercpp"])

        return self.stt_model.is_dir()

    def test_wake_cycle(self) -> None:
        print(f"Wake word configured: {self.wake_word}")
        print("Test flow: Wake → Speak → Process → Respond")

    def listen(self) -> None:
        print(f"Listening for wake word: {self.wake_word}")

    def speak(self, text: str) -> None:
        print(f"Thalexa says: {text}")

    def record_audio(self, duration_seconds: int = 5, samplerate: int = 16000) -> "np.ndarray":
        try:
            import numpy as np
            import sounddevice as sd
        except ImportError as exc:
            raise RuntimeError("sounddevice and numpy are required for audio recording") from exc

        print(f"Recording {duration_seconds} seconds of microphone audio...")
        audio = sd.rec(int(duration_seconds * samplerate), samplerate=samplerate, channels=1, dtype="float32")
        sd.wait()
        return audio.squeeze()

    def transcribe_audio(self, audio, samplerate: int = 16000) -> str | None:
        model = self._load_speech_model()
        if model is None:
            return None

        result = model.transcribe(audio, beam_size=5, language="en")
        segments = result[0] if isinstance(result, tuple) else getattr(result, "segments", [])
        return " ".join(getattr(segment, "text", str(segment)) for segment in segments).strip()

    def listen_for_wake_word(self, duration_seconds: int = 5) -> bool:
        self.listen()
        try:
            audio = self.record_audio(duration_seconds=duration_seconds)
        except Exception as exc:
            print(f"Audio capture failed: {exc}")
            return False

        if self.vad_available and not self._vad_has_speech(audio):
            print("No speech detected. Skipping transcription until next cycle.")
            return False

        transcription = self.transcribe_audio(audio)
        if transcription is None:
            print("Speech transcription model is not configured or available.")
            print(
                "To use a local GGUF file, install a Whisper C++ runtime package or provide a converted model directory."
            )
            return False

        print(f"Transcription result: {transcription}")
        triggered = self.wake_word.lower() in transcription.lower()
        if triggered:
            print("Wake word detected.")
        else:
            print("Wake word not detected.")
        return triggered

    def run_wake_word_loop(self, duration_seconds: int = 5, max_cycles: int = 0) -> None:
        print("Starting Thalexa wake-listen loop. Press Ctrl+C to stop.")
        cycle = 0
        while True:
            triggered = self.listen_for_wake_word(duration_seconds=duration_seconds)
            if triggered:
                self.speak("Wake word received. Thalexa is now listening.")
                break
            cycle += 1
            if max_cycles and cycle >= max_cycles:
                print("Max wake-listen cycles reached.")
                break

    def run_vad_listen_loop(self, duration_seconds: int = 5, max_cycles: int = 0) -> None:
        print("Starting Thalexa VAD-only listen loop. Press Ctrl+C to stop.")
        if not self.vad_available:
            print("Silero VAD is not available. Install silero-vad to enable this mode.")
            return

        cycle = 0
        while True:
            try:
                audio = self.record_audio(duration_seconds=duration_seconds)
            except Exception as exc:
                print(f"Audio capture failed: {exc}")
                break

            if self._vad_has_speech(audio, samplerate=16000):
                self.speak(
                    "Speech activity detected. Install a transcription runtime to process commands, or speak again to keep testing."
                )
            else:
                print("No speech detected in this segment.")

            cycle += 1
            if max_cycles and cycle >= max_cycles:
                print("Max VAD listen cycles reached.")
                break

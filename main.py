"""Entry point for Thalexa OS."""

from core.agents.orchestrator import OrchestratorAgent
from core.brain.thalexabot import ThalexaBrain
from core.memory.memory_store import MemoryStore
from core.models.model_manager import ModelManager
from core.personality.personality import PersonalityConfig
from core.voice.voice_manager import VoiceManager


def main():
    personality = PersonalityConfig.load("config/personality.yaml")
    model_manager = ModelManager()
    voice_manager = VoiceManager()
    orchestrator = OrchestratorAgent()
    memory = MemoryStore.initialize("vector_db")
    brain = ThalexaBrain(personality=personality)

    print("Starting Thalexa OS...")
    print(f"Loaded personality: {personality.name}")
    print(f"Memory store path: {memory.path}")

    model_manager.ensure_models()
    voice_manager.ensure_voice_runtime()

    if voice_manager.can_start_listening():
        voice_manager.run_wake_word_loop(duration_seconds=5)
    elif voice_manager.vad_available:
        print("STT is unavailable, but silero-vad is present. Entering VAD-only listening mode.")
        voice_manager.run_vad_listen_loop(duration_seconds=5)
    else:
        print("Wake-word listening is not active. Install a compatible STT runtime or update the local model to enable it.")

    orchestrator.run()
    brain.start()


if __name__ == "__main__":
    main()

from core.personality.personality import PersonalityConfig


class ThalexaBrain:
    def __init__(self, personality: PersonalityConfig):
        self.personality = personality

    def start(self):
        print("Thalexa Brain is online.")
        print(f"Mode: {self.personality.assistant_mode}")
        print("Awaiting input and monitoring agent workflows.")

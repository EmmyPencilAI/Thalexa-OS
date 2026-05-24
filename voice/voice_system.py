class VoiceSystem:
    def __init__(self, wake_word: str = "Hey Thalexa"):
        self.wake_word = wake_word

    def listen(self):
        print(f"Listening for wake word: {self.wake_word}")

    def speak(self, text: str):
        print(f"Thalexa says: {text}")

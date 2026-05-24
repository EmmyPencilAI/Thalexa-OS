from core.agents.agent import BaseAgent


class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Memory Agent")

    def run(self, *args, **kwargs):
        print(f"{self.name} is managing long-term memory and recall.")

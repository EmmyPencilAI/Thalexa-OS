from core.agents.agent import BaseAgent


class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Research Agent")

    def run(self, *args, **kwargs):
        print(f"{self.name} is exploring open-source intelligence and research signals.")

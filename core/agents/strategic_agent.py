from core.agents.agent import BaseAgent


class StrategicAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Strategic Agent")

    def run(self, *args, **kwargs):
        print(f"{self.name} is generating long-term strategy and planning guidance.")

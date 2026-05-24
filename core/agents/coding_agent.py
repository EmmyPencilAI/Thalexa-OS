from core.agents.agent import BaseAgent


class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Coding Agent")

    def run(self, *args, **kwargs):
        print(f"{self.name} is generating code and reviewing project tasks.")

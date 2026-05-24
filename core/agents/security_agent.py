from core.agents.agent import BaseAgent


class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Security Agent")

    def run(self, *args, **kwargs):
        print(f"{self.name} is evaluating defenses and threat status.")

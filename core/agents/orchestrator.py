from core.agents.agent import BaseAgent


class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Orchestrator")

    def run(self, *args, **kwargs):
        print(f"{self.name} is coordinating agent workflows.")

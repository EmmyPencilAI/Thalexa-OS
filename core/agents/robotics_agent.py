from core.agents.agent import BaseAgent


class RoboticsAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Robotics Agent")

    def run(self, *args, **kwargs):
        print(f"{self.name} is supporting hardware, firmware, and sensor workflows.")

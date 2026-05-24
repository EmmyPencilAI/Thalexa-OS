class Planner:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: str):
        self.tasks.append(task)

    def plan(self):
        return list(self.tasks)

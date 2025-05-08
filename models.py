from typing import Generic, TypeVar, List

T = TypeVar('T')

class Task(Generic[T]):
    def __init__(self, name: T):
        self.name = name
        self.state = 'To Do'

    def __str__(self):
        return f"{self.name} [{self.state}]"

class TaskList(Generic[T]):
    def __init__(self):
        self.tasks: List[Task[T]] = []

    def add(self, task: Task[T]):
        self.tasks.append(task)

    def get_all(self) -> List[Task[T]]:
        return self.tasks


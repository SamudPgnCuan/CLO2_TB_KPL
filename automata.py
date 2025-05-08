class TaskStateMachine:
    def __init__(self, task):
        self.task = task

    def next_state(self):
        if self.task.state == 'To Do':
            self.task.state = 'In Progress'
        elif self.task.state == 'In Progress':
            self.task.state = 'Done'
        elif self.task.state == 'Done':
            print(f"Tugas '{self.task.name}' sudah selesai.")
        else:
            raise Exception("Status tidak valid")

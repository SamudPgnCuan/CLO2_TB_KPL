class TaskStateMachine:
    def __init__(self, task):
        self.task = task
        assert self.task.state in ['To Do', 'In Progress', 'Done'], \
            "Invariant failed: state tidak dikenal"

    def next_state(self):
        if self.task.state == 'To Do':
            self.task.state = 'In Progress'
        elif self.task.state == 'In Progress':
            self.task.state = 'Done'
        elif self.task.state == 'Done':
            print(f"Tugas '{self.task.name}' sudah selesai.")
        else:
            raise Exception("Status tidak valid")
        assert self.task.state in ['To Do', 'In Progress', 'Done'], \
        "Postcondition failed: status akhir tugas tidak valid"

        if self.task.state == 'To Do':
            assert self.task.state == 'In Progress', \
                "Postcondition failed: transisi dari 'To Do' harus ke 'In Progress'"
        elif self.task.state == 'In Progress':
            assert self.task.state == 'Done', \
                "Postcondition failed: transisi dari 'In Progress' harus ke 'Done'"
        elif self.task.state == 'Done':
            assert self.task.state == 'Done', \
                "Invariant: status tidak berubah dari 'Done'"
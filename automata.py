class TaskStateMachine:
    def __init__(self, task):
        self.task = task

        #  Invariant: status tugas harus selalu salah satu dari status valid
        assert self.task.state in ['To Do', 'In Progress', 'Done'], \
            "Invariant failed: status tugas tidak valid saat FSM dibuat"

    def next_state(self):
        prev_state = self.task.state

        #  Precondition: status awal harus valid
        assert prev_state in ['To Do', 'In Progress', 'Done'], \
            "Precondition failed: status awal tugas tidak valid"

        # Logika transisi FSM
        if prev_state == 'To Do':
            self.task.state = 'In Progress'
        elif prev_state == 'In Progress':
            self.task.state = 'Done'
        elif prev_state == 'Done':
            print(f"Tugas '{self.task.name}' sudah selesai.")
        else:
            raise Exception("Status tidak dikenal")

        #  Invariant: status setelah transisi juga harus valid
        assert self.task.state in ['To Do', 'In Progress', 'Done'], \
            "Invariant failed: status akhir tugas tidak valid"

        #  Postcondition: transisi harus sesuai aturan FSM
        if prev_state == 'To Do':
            assert self.task.state == 'In Progress', \
                "Postcondition failed: dari 'To Do' harus ke 'In Progress'"
        elif prev_state == 'In Progress':
            assert self.task.state == 'Done', \
                "Postcondition failed: dari 'In Progress' harus ke 'Done'"
        elif prev_state == 'Done':
            assert self.task.state == 'Done', \
                "Postcondition failed: status tidak boleh berubah dari 'Done'"

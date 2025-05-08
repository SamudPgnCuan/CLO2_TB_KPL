from models import Task, TaskList
from automata import TaskStateMachine

def main():
    # Buat daftar tugas
    task1 = Task("Belajar Git")
    task2 = Task("Push ke GitHub")

    task_list = TaskList[str]()
    task_list.add(task1)
    task_list.add(task2)

    # Tampilkan daftar tugas awal
    print("=== Daftar Tugas ===")
    for idx, task in enumerate(task_list.get_all()):
        print(f"{idx + 1}. {task}")

    # Uji FSM (finite state machine) pada task1
    print("\n--- Transisi Status Otomatis pada Tugas 1 ---")
    fsm = TaskStateMachine(task1)

    print(f"Sebelum: {task1}")
    fsm.next_state()  # To Do → In Progress
    print(f"Setelah 1x next_state(): {task1}")
    fsm.next_state()  # In Progress → Done
    print(f"Setelah 2x next_state(): {task1}")
    fsm.next_state()  # Done → tidak berubah
    print(f"Setelah 3x next_state(): {task1}")

def __main__check__():
    print("Program dijalankan sebagai skrip utama.")

if __name__ == "__main__":
    main()

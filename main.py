import json
from models import Task, TaskList
from automata import TaskStateMachine

# Load konfigurasi dari config.json
def load_config():
    with open("config.json") as f:
        return json.load(f)

# Simpan daftar tugas ke file
def save_tasks_to_file(task_list: TaskList[str], filepath: str):
    with open(filepath, "w") as f:
        for task in task_list.get_all():
            f.write(f"{task.name}|{task.state}\n")

# Baca daftar tugas dari file
def load_tasks_from_file(filepath: str) -> TaskList[str]:
    task_list = TaskList[str]()
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    name, state = line.split("|")
                    task = Task(name)
                    task.state = state
                    task_list.add(task)
    except FileNotFoundError:
        print(f"(File '{filepath}' belum ada, daftar tugas dimulai kosong)")
    return task_list

def main():
    # Load config
    config = load_config()
    task_file = config["task_file"]

    print("\n=== Konfigurasi Runtime ===")
    print(f"File penyimpanan tugas: {task_file}")

    # Load tugas dari file
    task_list = load_tasks_from_file(task_file)

    # Tampilkan daftar tugas lama
    print("\n=== Daftar Tugas Sebelumnya ===")
    for idx, task in enumerate(task_list.get_all()):
        print(f"{idx + 1}. {task}")

    # Tambah tugas baru
    print("\nTambah tugas baru: 'Review Coding'")
    new_task = Task("Review Coding")
    task_list.add(new_task)

    # Uji transisi status dengan automata
    print("\n--- Transisi Status Tugas Baru ---")
    fsm = TaskStateMachine(new_task)
    print(f"Sebelum: {new_task}")
    fsm.next_state()  # To Do -> In Progress
    print(f"Setelah 1x next_state(): {new_task}")
    fsm.next_state()  # In Progress -> Done
    print(f"Setelah 2x next_state(): {new_task}")
    fsm.next_state()  # Done → (tidak berubah)

    # Simpan ke file
    save_tasks_to_file(task_list, task_file)
    print("\nData tugas disimpan ke file.")

if __name__ == "__main__":
    main()

import json
from models import Task, TaskList
from menu import show_menu, menu_options
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
    config = load_config()
    task_file = config["task_file"]
    task_list = load_tasks_from_file(task_file)

    print("=== Aplikasi To-Do List CLI ===")
    options = menu_options(task_list, save_tasks_to_file, task_file)

    while True:
        show_menu()
        choice = input("Pilih opsi (1-4): ").strip()
        action = options.get(choice)
        if action:
            action()
        else:
            print("Opsi tidak dikenal. Silakan coba lagi.")

if __name__ == "__main__":
    main()

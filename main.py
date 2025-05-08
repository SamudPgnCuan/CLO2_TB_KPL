from models import Task, TaskList

def main():
    # Buat sebuah task
    task1 = Task("Belajar Git")
    task2 = Task("Push ke GitHub")
    
    # Buat daftar tugas
    task_list = TaskList[str]()
    task_list.add(task1)
    task_list.add(task2)

    # Tampilkan semua tugas
    print("=== Daftar Tugas ===")
    for idx, task in enumerate(task_list.get_all()):
        print(f"{idx + 1}. {task}")

if __name__ == "__main__":
    main()

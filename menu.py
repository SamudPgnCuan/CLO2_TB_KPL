from automata import TaskStateMachine
from models import Task

def show_menu():
    print("\n=== MENU ===")
    print("1. Tambah Tugas")
    print("2. Lihat Semua Tugas")
    print("3. Ubah Status Tugas")
    print("4. Simpan dan Keluar")

def menu_options(task_list, save_func, task_file):

    def add_task():
        name = input("Masukkan nama tugas: ")
        if name.strip():
            task = Task(name)
            task_list.add(task)
            print(f"Tugas '{name}' ditambahkan.")
        else:
            print("Nama tugas tidak boleh kosong.")

    def view_tasks():
        print("\n=== Daftar Tugas ===")
        if not task_list.get_all():
            print("(Tidak ada tugas)")
        for idx, task in enumerate(task_list.get_all()):
            print(f"{idx + 1}. {task}")

    def update_task():
        view_tasks()
        if not task_list.get_all():
            return
        try:
            index = int(input("Pilih nomor tugas untuk update status: ")) - 1
            task = task_list.get_all()[index]
            fsm = TaskStateMachine(task)
            fsm.next_state()
            print(f"Status tugas '{task.name}' diperbarui menjadi [{task.state}].")
        except (ValueError, IndexError):
            print("Input tidak valid.")

    def exit_program():
        save_func(task_list, task_file)
        print("Tugas disimpan. Program selesai.")
        exit()

    return {
        '1': add_task,
        '2': view_tasks,
        '3': update_task,
        '4': exit_program
    }

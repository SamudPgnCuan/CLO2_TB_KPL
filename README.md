# Aplikasi to-do-list

## KELOMPOK X - Konstruksi Perangkat Lunak SE06-03

| Nama                   | NIM        |
| ---------------------- | ---------- |
| Muhammad Samudra       | 2211104062 |
| Dawnie Julian Nugroho  | 2211104064 |
| Aditya Sendi Hana S.   | 2211104067 |
| Mohammad Fathurrohman  | 2211104070 |

## Cara Penggunaan
1. Ubah isi file config.json untuk mengubah nama file dan lokasi file text list tugas
2. Jalankan main.py
3. Input opsi sesuai menu
4. Jangan lupa pilih opsi 4 (simpan dan keluar) untuk menyimpan perubahan

## Deskripsi Singkat

Aplikasi ini adalah program simpel untuk membuat dan menyimpan to-do-list (di sini lebih untuk list tugas). Sistem ini berbasis command line interface tanpa GUI dengan sistem **menu interaktif berbasis table-driven construction**. Pengguna dapat:
    1. Menambah tugas
    2. Melihat daftar tugas
    3. Memperbarui status tugas (menggunakan Finite State Machine/konsep automata)
    4. Dan menyimpan data tugas ke file tasks.txt


##  Teknik Konstruksi yang Diterapkan

| Teknik Konstruksi     | File/Modul         | Penjelasan Ringkas                                     |
|------------------------|---------------------|----------------------------------------------------------|
| Generics               | `models.py`         | `Task<T>` dan `TaskList<T>` dengan `typing.Generic`     |
| Automata (FSM)         | `automata.py`       | Transisi status `To Do → In Progress → Done`            |
| Runtime Configuration  | `config.json`       | File eksternal untuk path penyimpanan tugas             |
| Table-driven CLI       | `menu.py`           | Menu CLI menggunakan dictionary pemetaan fungsi         |


---

##  Contoh Output 

![contoh output  1](https://github.com/user-attachments/assets/baf4303c-597d-4fc3-9de2-e462ca9064a5) 

![contoh output  2](https://github.com/user-attachments/assets/6bc431e6-f6d6-4462-a893-dba4e2b98e4f)

---

# Penjelasan Program dan Teknik Konstruksi Terapan

## models.py (Penerapan Teknik Generics)

Generics adalah teknik pemrograman yang memungkinkan kelas atau fungsi bekerja dengan berbagai tipe data

**Code:**
``` python
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
```
Di sini `T` merupakan variabel tipe generik yang bisa mewakili `str`, `int`, atau tipe buatan lain. Berarti juga `Task` adalah kelas generik sehingga argumen `name` bisa bertipe apapun (jika mendeklarasikan Task[int] maka argumen `name` juga bertipe `int`). Untuk saat ini tidak mengharuskan variabel `T` untuk berbentuk generik tetapi jika suatu saat program dikembangkan dan memerlukan `Task[int]` maka kelas siap pakai.

---

## automata.py (Penerapan Teknik Automata)
Teknik Automata di sini diimplementasikan sebagai **Finite State Machine**, yaitu model logika yang terdiri dari State, Transisi, dan Aturan perubahan state. Di sini terdapat tiga state yaitu `To Do` (akan dikerjakan), ``In Progress`` (sedang dikerjakan), `Done` (selesai). Perubahan satu arah dari `To Do` ke `In Progress` dan terakhir ke `Done`, dan perubahan state terjadi ketika user memilih opsi 3 ("Ubah Status Tugas") pada menu interface.

**code:**

```python
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
```

---

## config.json (Penerapan Teknik Runtime Configuration)
Runtime Configuration adalah teknik konstruksi perangkat lunak di mana pengaturan penting aplikasi disimpan di luar kode sumber, di sini di file `config.json`. Hal ini berguna agar pengguna tidak perlu mengubah sumber kode untuk mengganti pengaturan.

**Code:**
File config.json:
```
{
  "task_file": "tasks.txt"
}
```

File ini menyimpan nama atau lokasi file penyimpanan tugas (tasks.txt), yang dibaca saat program dijalankan.

Kode di main.py:
  Fungsi untuk membaca konfigurasi:
  ```
  import json

  def load_config():
      with open("config.json") as f:
          return json.load(f)
  ```

  Penggunaan hasil konfigurasi:
  ```
  config = load_config()
  task_file = config["task_file"]
  task_list = load_tasks_from_file(task_file)
  ```
  Variabel task_file kemudian digunakan di seluruh program untuk:

  - Membaca daftar tugas dari file saat startup
  - Menyimpan daftar tugas kembali ke file saat ada perubahan

---

## menu.py (Penerapan Teknik Table-Driven Construction)
Table-driven construction adalah teknik di mana logika program dikendalikan oleh data table, seperti dictionary atau lookup table, daripada `if-else` atau `switch-case` panjang.

```
return {
        '1': add_task,
        '2': view_tasks,
        '3': update_task,
        '4': exit_program,
        '5': delete_task
    }
```
Inilah bagian dari Table-Driven. Tidak ada `if` dan `else` ataupun `case` dan `switch`. Jika ingin menambahkan opsi hanya menambahkan 1 key-fungsi di dictionary, tidak harus membuat blok `elif` atau `case` baru. Hal ini membuat pengendali logika lebih mudah ditambahkan dan dikelola daripada harus membuat blok baru atau mencari dulu blok yang ingin dihapus.

# Alur Kerja Progam

**Code:**
main.py
```python
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
        choice = input("Pilih opsi (1-5): ").strip()
        action = options.get(choice)
        if action:
            action()
        else:
            print("Opsi tidak dikenal. Silakan coba lagi.")

if __name__ == "__main__":
    main()

```

Saat program dijalankan:

1. Program membaca konfigurasi dari `config.json`
2. Memuat daftar tugas dari file `tasks.txt` 
3. Menampilkan menu CLI
4. Pengguna dapat:
   - Menambah tugas baru
   - Melihat semua tugas
   - Memperbarui status tugas
   - Menyimpan & keluar


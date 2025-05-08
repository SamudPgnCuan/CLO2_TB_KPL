# Aplikasi to-do-list

## Deskripsi Singkat

Aplikasi ini adalah program simpel untuk membuat dan menyimpan to-do-list (di sini lebih untuk list tugas). Sistem ini berbasis command line interface tanpa GUI dengan sistem **menu interaktif berbasis table-driven construction**. Pengguna dapat:
    1. Menambah tugas
    2. Melihat daftar tugas
    3. Memperbarui status tugas (menggunakan Finite State Machine/konsep automata)
    4. Dan menyimpan data tugas ke file tasks.txt




<!-- ## Alur Penggunaan

Saat program dijalankan:

1. Program membaca konfigurasi dari `config.json`
2. Memuat daftar tugas dari file `tasks.txt` 
3. Menampilkan menu CLI
4. Pengguna dapat:
   - Menambah tugas baru
   - Melihat semua tugas
   - Memperbarui status tugas
   - Menyimpan & keluar

--- -->




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

## models.py (Penerapan Generics)

Generics adalah teknik pemrograman yang memungkinkan kelas atau fungsi bekerja dengan berbagai tipe data
```
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
Di sini `T` 

---
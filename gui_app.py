import json
import tkinter as tk
from tkinter import ttk, messagebox
from models import Task, TaskList
from automata import TaskStateMachine

class TodoListGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi To-Do List")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Load configuration
        self.config = self.load_config()
        self.task_file = self.config["task_file"]
        
        # Load tasks
        self.task_list = self.load_tasks_from_file(self.task_file)
        
        # Create UI
        self.create_widgets()
        self.update_task_list()
        
    def load_config(self):
        with open("config.json") as f:
            return json.load(f)
    
    def save_tasks_to_file(self):
        with open(self.task_file, "w") as f:
            for task in self.task_list.get_all():
                f.write(f"{task.name}|{task.state}\n")
        messagebox.showinfo("Informasi", "Tugas berhasil disimpan")
    
    def load_tasks_from_file(self, filepath):
        task_list = TaskList()
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
    
    def create_widgets(self):
        # Frame untuk input dan tombol
        input_frame = tk.Frame(self.root, bg="#f0f0f0", pady=15)
        input_frame.pack(fill=tk.X, padx=20)
        
        # Label dan Entry untuk input tugas
        tk.Label(input_frame, text="Nama Tugas:", bg="#a5d6a7", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.task_entry = tk.Entry(input_frame, width=30, font=("Arial", 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        # Tombol untuk menambah tugas - PERBAIKAN: Warna cerah dengan teks gelap untuk kontras lebih baik
        add_button = tk.Button(input_frame, text="Tambah Tugas", command=self.add_task, 
                            bg="#a5d6a7", fg="black", font=("Arial", 10, "bold"), 
                            padx=10, relief=tk.RAISED)
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Frame untuk tabel tugas
        table_frame = tk.Frame(self.root, bg="white", pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Scrollbar untuk tabel
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview untuk menampilkan daftar tugas
        self.task_tree = ttk.Treeview(table_frame, columns=("Nama Tugas", "Status"), show="headings", 
                                    yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_tree.yview)
        
        self.task_tree.heading("Nama Tugas", text="Nama Tugas")
        self.task_tree.heading("Status", text="Status")
        
        self.task_tree.column("Nama Tugas", width=400)
        self.task_tree.column("Status", width=100)
        
        # Konfigurasi warna tabel
        self.task_tree.tag_configure('evenrow', background='white')
        self.task_tree.tag_configure('oddrow', background='#f0f0f0')
        
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame untuk tombol-tombol aksi
        button_frame = tk.Frame(self.root, bg="#f0f0f0", pady=15)
        button_frame.pack(fill=tk.X, padx=20)
        
        # PERBAIKAN: Tombol dengan warna cerah dan teks gelap untuk kontras yang lebih baik
        button_style = {
            'font': ('Arial', 10, 'bold'),
            'relief': tk.RAISED,
            'padx': 10,
            'pady': 5,
            'borderwidth': 2
        }
        
        # Tombol untuk memperbarui status tugas - biru muda dengan teks hitam
        update_button = tk.Button(button_frame, text="Ubah Status", command=self.update_task_status, 
                                bg="#64b5f6", fg="black", **button_style)
        update_button.pack(side=tk.LEFT, padx=5)
        
        # Tombol untuk menghapus tugas - merah muda dengan teks hitam
        delete_button = tk.Button(button_frame, text="Hapus Tugas", command=self.delete_task, 
                                bg="#ef9a9a", fg="black", **button_style)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Tombol untuk menyimpan tugas - oranye muda dengan teks hitam
        save_button = tk.Button(button_frame, text="Simpan", command=self.save_tasks_to_file, 
                            bg="#ffcc80", fg="black", **button_style)
        save_button.pack(side=tk.LEFT, padx=5)
        
        # Tombol untuk keluar dari aplikasi - abu-abu muda dengan teks hitam
        exit_button = tk.Button(button_frame, text="Keluar", command=self.exit_program, 
                            bg="#e0e0e0", fg="black", **button_style)
        exit_button.pack(side=tk.LEFT, padx=5)
    
    def update_task_list(self):
        # Hapus semua item di treeview
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Tambahkan tugas ke treeview dengan warna bergantian
        for i, task in enumerate(self.task_list.get_all()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.task_tree.insert("", tk.END, values=(task.name, task.state), tags=(tag,))
    
    def add_task(self):
        task_name = self.task_entry.get().strip()
        if task_name:
            task = Task(task_name)
            self.task_list.add(task)
            messagebox.showinfo("Informasi", f"Tugas '{task_name}' ditambahkan")
            self.task_entry.delete(0, tk.END)  # Clear the entry
            self.update_task_list()
        else:
            messagebox.showwarning("Peringatan", "Nama tugas tidak boleh kosong")
    
    def update_task_status(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            item_index = self.task_tree.index(selected_item)
            task = self.task_list.get_all()[item_index]
            fsm = TaskStateMachine(task)
            fsm.next_state()
            messagebox.showinfo("Informasi", f"Status tugas '{task.name}' diperbarui menjadi [{task.state}]")
            self.update_task_list()
        else:
            messagebox.showwarning("Peringatan", "Pilih sebuah tugas terlebih dahulu")
    
    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            item_index = self.task_tree.index(selected_item)
            task = self.task_list.get_all()[item_index]
            confirm = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus tugas '{task.name}'?")
            if confirm:
                self.task_list.get_all().pop(item_index)
                messagebox.showinfo("Informasi", f"Tugas '{task.name}' telah dihapus")
                self.update_task_list()
        else:
            messagebox.showwarning("Peringatan", "Pilih sebuah tugas terlebih dahulu")
    
    def exit_program(self):
        confirm = messagebox.askyesno("Konfirmasi", "Simpan tugas sebelum keluar?")
        if confirm:
            self.save_tasks_to_file()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Konfigurasikan style untuk ttk
    style = ttk.Style()
    style.theme_use('default')  # Menggunakan tema default yang lebih terang
    
    # Mengatur warna treeview dan heading
    style.configure("Treeview", 
                    font=('Arial', 10),
                    background="white", 
                    fieldbackground="white",
                    foreground="black")
    
    style.configure("Treeview.Heading", 
                    font=('Arial', 10, 'bold'),
                    background="#d9d9d9", 
                    foreground="black")
    
    # Menghilangkan border fokus yang bisa membuat teks sulit dibaca
    style.map('Treeview', background=[('selected', '#0078d7')], 
              foreground=[('selected', 'white')])
    
    # Ubah warna tema sistem untuk tombol dengan warna yang lebih kontras
    # Menggunakan teks hitam pada latar belakang terang untuk kontras yang lebih baik
    root.option_add("*Button.Background", "#ffeb3b")  # Kuning cerah
    root.option_add("*Button.Foreground", "black")    # Teks hitam
    root.option_add("*Button.Relief", "raised")
    root.option_add("*Button.BorderWidth", 2)
    
    app = TodoListGUI(root)
    root.mainloop()
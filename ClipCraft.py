"""Aplikasi clipboard sederhana untuk menyimpan dan menyusun potongan teks.

Tkinter menyediakan antarmuka, SQLite menyimpan daftar modul teks, dan
pyperclip menyalin teks ke clipboard sistem operasi.
"""
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.scrolledtext as scrolledtext
import pyperclip


class ClipboardApp:
    """Mengelola jendela, daftar modul, editor teks, dan clipboard."""

    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard App")

        # Path relatif ini sengaja dipertahankan agar lokasi database tetap
        # mengikuti perilaku versi awal: modules.db di direktori kerja aktif.
        self.conn = sqlite3.connect("modules.db")
        self.cursor = self.conn.cursor()

        # Buat tabel hanya bila belum tersedia, sehingga database lama tetap
        # dapat digunakan tanpa migrasi skema.
        self.cursor.execute("CREATE TABLE IF NOT EXISTS modules (name TEXT)")
        self.conn.commit()

        # Setiap bagian GUI dibuat melalui metode terpisah agar lebih mudah
        # dibaca, diuji, dan dimodifikasi tanpa mengubah seluruh jendela.
        self.create_app_title()
        button_frame = self.create_button_frame()
        self.create_module_dropdown()
        self.create_new_module_entry()
        self.create_add_module_button(button_frame)
        self.create_delete_module_button(button_frame)
        self.create_clipboard_text()
        self.create_load_from_db_button(button_frame)
        self.create_copy_button(button_frame)
        self.create_clear_button(button_frame)

        # Izinkan panel tombol menyesuaikan ruang ketika jendela diperbesar.
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)

        # Tutup koneksi database saat pengguna menutup jendela aplikasi.
        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

    def create_app_title(self):
        """Tampilkan judul aplikasi di bagian atas."""
        app_title = tk.Label(
            self.root, text="Clipboard App", font=("Helvetica", 18, "bold")
        )
        app_title.grid(row=0, column=0, columnspan=4, pady=10)

    def create_button_frame(self):
        """Buat wadah untuk tombol aksi."""
        button_frame = tk.Frame(self.root)
        button_frame.grid(
            row=1, column=3, rowspan=2, padx=10, pady=10, sticky="nsew"
        )
        return button_frame

    def create_module_dropdown(self):
        """Buat dropdown yang menampilkan nama modul dari database."""
        module_label = tk.Label(self.root, text="Choose:")
        module_label.grid(row=1, column=0)
        self.module_var = tk.StringVar()
        self.module_dropdown = ttk.Combobox(
            self.root, textvariable=self.module_var
        )
        self.module_dropdown["values"] = self.get_module_list()
        self.module_dropdown.grid(row=1, column=1)

    def create_new_module_entry(self):
        """Buat kolom input untuk nama atau potongan teks baru."""
        new_module_label = tk.Label(
            self.root, text="Add New:", font=("Helvetica", 12)
        )
        new_module_label.grid(row=2, column=0, pady=10)
        self.new_module_var = tk.StringVar()
        self.new_module_entry = tk.Entry(
            self.root, textvariable=self.new_module_var
        )
        self.new_module_entry.grid(row=2, column=1, padx=10, pady=10)

    def create_add_module_button(self, button_frame):
        """Hubungkan tombol Add ke fungsi add_module."""
        tk.Button(
            button_frame, text="Add", command=self.add_module,
            bg="brown", fg="white"
        ).pack(pady=5, fill="x")

    def create_delete_module_button(self, button_frame):
        """Hubungkan tombol Delete ke fungsi delete_module."""
        tk.Button(
            button_frame, text="Delete", command=self.delete_module,
            bg="brown", fg="white"
        ).pack(pady=5, fill="x")

    def create_clipboard_text(self):
        """Buat editor teks dengan scrollbar vertikal."""
        tk.Label(
            self.root, text="Clipboard:", font=("Helvetica", 12, "bold")
        ).grid(row=3, column=0, pady=10)
        self.clipboard_text = scrolledtext.ScrolledText(
            self.root, height=20, width=80
        )
        self.clipboard_text.grid(
            row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew"
        )

    def create_load_from_db_button(self, button_frame):
        """Buat tombol untuk menambahkan modul terpilih ke editor."""
        tk.Button(
            button_frame, text="Load", command=self.load_from_database,
            bg="brown", fg="white"
        ).pack(pady=5, fill="x")

    def create_copy_button(self, button_frame):
        """Buat tombol untuk menyalin teks editor ke clipboard sistem."""
        tk.Button(
            button_frame, text="Copy", command=self.copy_to_clipboard,
            bg="brown", fg="white"
        ).pack(pady=5, fill="x")

    def create_clear_button(self, button_frame):
        """Buat tombol untuk mengosongkan editor, bukan database."""
        tk.Button(
            button_frame, text="Clear", command=self.clear_clipboard,
            bg="brown", fg="white"
        ).pack(pady=5, fill="x")

    def get_module_list(self):
        """Baca semua nama modul untuk mengisi pilihan dropdown."""
        self.cursor.execute("SELECT name FROM modules")
        return [row[0] for row in self.cursor.fetchall()]

    def refresh_module_dropdown(self):
        """Perbarui daftar dropdown setelah modul ditambah atau dihapus."""
        self.module_dropdown["values"] = self.get_module_list()

    def add_module(self):
        """Simpan modul baru, lalu perbarui pilihan dropdown."""
        # Hapus spasi di awal/akhir dan tolak input kosong agar tidak ada
        # modul yang namanya hanya terdiri dari spasi.
        new_module = self.new_module_var.get().strip()
        if not new_module:
            messagebox.showwarning(
                "Input belum diisi", "Masukkan nama modul terlebih dahulu.",
                parent=self.root
            )
            return

        # Placeholder SQL (?) memisahkan data input dari perintah SQL.
        self.cursor.execute(
            "INSERT INTO modules (name) VALUES (?)", (new_module,)
        )
        self.conn.commit()
        self.refresh_module_dropdown()
        self.new_module_var.set("")

    def delete_module(self):
        """Hapus modul yang sedang dipilih dari database."""
        selected_module = self.module_var.get()
        if not selected_module:
            messagebox.showwarning(
                "Belum ada pilihan", "Pilih modul yang ingin dihapus.",
                parent=self.root
            )
            return

        # Parameter query menghindari penggabungan langsung input ke SQL.
        self.cursor.execute(
            "DELETE FROM modules WHERE name = ?", (selected_module,)
        )
        self.conn.commit()
        self.refresh_module_dropdown()
        self.module_var.set("")

    def copy_to_clipboard(self):
        """Salin semua isi editor ke clipboard sistem operasi."""
        clipboard_text = self.clipboard_text.get("1.0", "end-1c")
        try:
            pyperclip.copy(clipboard_text)
        except pyperclip.PyperclipException as error:
            # pyperclip dapat gagal bila lingkungan desktop tidak menyediakan
            # mekanisme clipboard yang didukung.
            messagebox.showerror(
                "Gagal menyalin",
                f"Teks tidak dapat disalin ke clipboard.\n{error}",
                parent=self.root
            )

    def load_from_database(self):
        """Tambahkan nama modul terpilih di akhir editor teks."""
        selected_module = self.module_var.get()
        if not selected_module:
            messagebox.showwarning(
                "Belum ada pilihan", "Pilih modul yang ingin dimuat.",
                parent=self.root
            )
            return

        self.cursor.execute(
            "SELECT name FROM modules WHERE name = ?", (selected_module,)
        )
        module_data = self.cursor.fetchone()

        # Periksa hasil query karena data mungkin sudah dihapus atau berubah.
        if module_data:
            module_name = module_data[0]
            current_text = self.clipboard_text.get("1.0", "end-1c")
            # Pertahankan isi lama dan pisahkan tambahan dengan baris baru.
            new_text = (
                f"{current_text}\n{module_name}" if current_text else module_name
            )
            self.clipboard_text.delete("1.0", "end")
            self.clipboard_text.insert("1.0", new_text)

    def clear_clipboard(self):
        """Kosongkan editor tanpa menghapus modul yang tersimpan."""
        self.clipboard_text.delete("1.0", "end")

    def close_application(self):
        """Tutup cursor dan koneksi SQLite sebelum jendela dihancurkan."""
        try:
            self.cursor.close()
            self.conn.close()
        finally:
            self.root.destroy()


if __name__ == "__main__":
    # Entry point ini hanya berjalan ketika file dieksekusi langsung.
    root = tk.Tk()
    app = ClipboardApp(root)
    root.mainloop()

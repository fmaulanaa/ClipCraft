import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import pyperclip
import sqlite3

class ClipboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard App")

        self.conn = sqlite3.connect('modules.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS modules (name TEXT)''')
        self.conn.commit()

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

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)

    def create_app_title(self):
        app_title = tk.Label(self.root, text="Clipboard App", font=("Helvetica", 18, "bold"))
        app_title.grid(row=0, column=0, columnspan=4, pady=10)

    def create_button_frame(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=3, rowspan=2, padx=10, pady=10, sticky="nsew")
        return button_frame

    def create_module_dropdown(self):
        module_label = tk.Label(self.root, text="Choose:")
        module_label.grid(row=1, column=0)
        self.module_var = tk.StringVar()
        self.module_dropdown = ttk.Combobox(self.root, textvariable=self.module_var)
        self.module_dropdown['values'] = self.get_module_list()
        self.module_dropdown.grid(row=1, column=1)

    def create_new_module_entry(self):
        new_module_label = tk.Label(self.root, text="Add New:", font=("Helvetica", 12))
        new_module_label.grid(row=2, column=0, pady=10)
        self.new_module_var = tk.StringVar()
        self.new_module_entry = tk.Entry(self.root, textvariable=self.new_module_var)
        self.new_module_entry.grid(row=2, column=1, padx=10, pady=10)

    def create_add_module_button(self, button_frame):
        add_module_button = tk.Button(button_frame, text="Add", command=self.add_module, bg="brown", fg="white")
        add_module_button.pack(pady=5, fill='x')

    def create_delete_module_button(self, button_frame):
        delete_module_button = tk.Button(button_frame, text="Delete", command=self.delete_module, bg="brown", fg="white")
        delete_module_button.pack(pady=5, fill='x')

    def create_clipboard_text(self):
        clipboard_label = tk.Label(self.root, text="Clipboard:", font=("Helvetica", 12, "bold"))
        clipboard_label.grid(row=3, column=0, pady=10)
        self.clipboard_text = scrolledtext.ScrolledText(self.root, height=20, width=80)  # Lebar teks diperbesar
        self.clipboard_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def create_load_from_db_button(self, button_frame):
        load_from_db_button = tk.Button(button_frame, text="Load", command=self.load_from_database, bg="brown", fg="white")
        load_from_db_button.pack(pady=5, fill='x')

    def create_copy_button(self, button_frame):
        copy_button = tk.Button(button_frame, text="Copy", command=self.copy_to_clipboard, bg="brown", fg="white")
        copy_button.pack(pady=5, fill='x')

    def create_clear_button(self, button_frame):
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_clipboard, bg="brown", fg="white")
        clear_button.pack(pady=5, fill='x')

    def get_module_list(self):
        self.cursor.execute("SELECT name FROM modules")
        modules = [row[0] for row in self.cursor.fetchall()]
        return modules

    def add_module(self):
        new_module = self.new_module_var.get()
        if new_module:
            self.cursor.execute("INSERT INTO modules (name) VALUES (?)", (new_module,))
            self.conn.commit()
            self.module_dropdown['values'] = self.get_module_list()
            self.new_module_var.set("")

    def delete_module(self):
        selected_module = self.module_var.get()
        if selected_module:
            self.cursor.execute("DELETE FROM modules WHERE name=?", (selected_module,))
            self.conn.commit()
            self.module_dropdown['values'] = self.get_module_list()
            self.module_var.set("")

    def copy_to_clipboard(self):
        clipboard_text = self.clipboard_text.get("1.0", "end-1c")
        pyperclip.copy(clipboard_text)

    def load_from_database(self):
        selected_module = self.module_var.get()
        if selected_module:
            self.cursor.execute("SELECT name FROM modules WHERE name=?", (selected_module,))
            module_data = self.cursor.fetchone()
            if module_data:
                module_name = module_data[0]
                current_text = self.clipboard_text.get("1.0", "end-1c")
                if current_text:
                    new_text = current_text + "\n" + module_name
                else:
                    new_text = module_name
                self.clipboard_text.delete("1.0", "end")
                self.clipboard_text.insert("1.0", new_text)

    def clear_clipboard(self):
        self.clipboard_text.delete("1.0", "end")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardApp(root)
    root.mainloop()

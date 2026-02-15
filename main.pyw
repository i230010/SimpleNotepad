import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path

def main():
    class SimpleNotepad(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Untitled - SimpleNotepad")
            self.geometry("700x700")
            self.menubar = tk.Menu()
            self.file_menu = tk.Menu(tearoff=False)
            self.file_menu.add_command(label="New", command=self.new)
            self.file_menu.add_command(label="Open", command=self.open)
            self.file_menu.add_command(label="Save", command=self.save)
            self.file_menu.add_command(
                label="Save As",
                command=self.save_as
            )
            self.menubar.add_cascade(menu=self.file_menu, label="File")
            self.config(menu=self.menubar)
            self.text = tk.Text()
            self.text.pack(expand=True, fill=tk.BOTH)
            self.current_file = None
            self.filetypes = (
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            )
            self.protocol("WM_DELETE_WINDOW", self.close)

        def close(self) -> None:
            if not self.can_continue():
                return
            self.destroy()

        def set_current_file(self, current_file):
            self.current_file = current_file
            self.title(self.current_file.name + " - SimpleNotepad")

        def can_continue(self):
            if self.text.edit_modified():
                result = messagebox.askyesnocancel(
                    title="Unsaved Changes",
                    message="Do you want to save changes?"
                )
                cancel = result is None
                save_before = result is True
                if cancel:
                    return False
                elif save_before:
                    self.save()
                return True
            return True
            
        def new(self) -> None:
            if not self.can_continue():
                return
            self.text.delete("1.0", tk.END)
            self.current_file = None
            self.title("Untitled - SimpleNotepad")

        def open(self):
            filename = filedialog.askopenfilename(filetypes=self.filetypes)
            if not filename or not self.can_continue():
                return
            self.text.delete("1.0", tk.END)
            file = Path(filename)
            self.text.insert("1.0", file.read_text("utf8"))
            self.text.edit_modified(False)
            self.set_current_file(file)

        def save_current_file(self) -> None:
            if self.current_file is None:
                return
            self.current_file.write_text(self.text.get("1.0", tk.END), "utf8")

        def save(self) -> None:
            if self.current_file is None:
                self.save_as()
                return
            self.save_current_file()

        def save_as(self) -> None:
            filename = filedialog.asksaveasfilename(
                filetypes=self.filetypes
            )
            if not filename:
                return
            self.set_current_file(Path(filename))
            self.save_current_file()

    app = SimpleNotepad()
    app.mainloop()


if __name__ == "__main__":
    main()

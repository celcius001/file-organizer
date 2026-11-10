import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


class FileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Downloads File Organizer")
        self.root.geometry("720x800")
        self.root.minsize(650, 600)

        self.folders = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx"],
            "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv"],
            "Music": [".mp3", ".wav", ".aac", ".flac"],
            "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
            "Scripts": [".py", ".js", ".html", ".css", ".sh", ".ps1"],
            "Executables": [".exe", ".msi", ".bat", ".app"],
            "Others": []
        }

        self.selected_folder = tk.StringVar()
        self.category_vars = {}
        self.is_organizing = False

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)

        # Header
        ttk.Label(
            main,
            text="FILE ORGANIZER",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")

        ttk.Label(
            main,
            text="Organize files into folders automatically.",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(0, 20))

        # Folder selection
        folder_frame = ttk.LabelFrame(
            main, text="Select Folder", padding=12
        )
        folder_frame.pack(fill="x", pady=5)

        folder_row = ttk.Frame(folder_frame)
        folder_row.pack(fill="x")

        self.folder_entry = ttk.Entry(
            folder_row,
            textvariable=self.selected_folder,
            state="readonly"
        )
        self.folder_entry.pack(
            side="left", fill="x", expand=True, padx=(0, 10)
        )

        ttk.Button(
            folder_row,
            text="Browse",
            command=self.browse_folder
        ).pack(side="right")

        # Categories
        category_frame = ttk.LabelFrame(
            main, text="File Categories", padding=12
        )
        category_frame.pack(fill="x", pady=12)

        controls = ttk.Frame(category_frame)
        controls.pack(fill="x", pady=(0, 10))

        ttk.Button(
            controls,
            text="Select All",
            command=lambda: self.select_all(True)
        ).pack(side="left", padx=(0, 5))

        ttk.Button(
            controls,
            text="Deselect All",
            command=lambda: self.select_all(False)
        ).pack(side="left")

        grid = ttk.Frame(category_frame)
        grid.pack(fill="x")

        for index, name in enumerate(self.folders):
            var = tk.BooleanVar(value=True)
            self.category_vars[name] = var

            ttk.Checkbutton(
                grid,
                text=name,
                variable=var
            ).grid(
                row=index // 4,
                column=index % 4,
                sticky="w",
                padx=10,
                pady=7
            )

        # Progress
        progress_frame = ttk.LabelFrame(
            main, text="Progress", padding=12
        )
        progress_frame.pack(fill="x", pady=5)

        self.status_label = ttk.Label(
            progress_frame,
            text="Ready to organize."
        )
        self.status_label.pack(anchor="w", pady=(0, 8))

        self.progress = ttk.Progressbar(
            progress_frame,
            mode="determinate"
        )
        self.progress.pack(fill="x")

        # Activity Log
        log_frame = ttk.LabelFrame(
            main, text="Activity Log", padding=10
        )
        log_frame.pack(fill="both", expand=True, pady=10)

        self.log = tk.Text(
            log_frame,
            height=10,
            font=("Consolas", 9),
            state="disabled",
            wrap="word"
        )
        self.log.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            log_frame,
            command=self.log.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.log.configure(yscrollcommand=scrollbar.set)

        # Bottom Buttons
        button_frame = ttk.Frame(main)
        button_frame.pack(fill="x", pady=(5, 0))

        self.organize_button = ttk.Button(
            button_frame,
            text="Organize Files",
            command=self.organize_files
        )
        self.organize_button.pack(
            side="left", fill="x", expand=True, padx=(0, 5)
        )

        ttk.Button(
            button_frame,
            text="Clear Log",
            command=self.clear_log
        ).pack(side="right")

    def browse_folder(self):
        folder = filedialog.askdirectory(
            title="Select Folder to Organize"
        )

        if folder:
            self.selected_folder.set(folder)
            self.write_log(f"Selected folder: {folder}")

    def select_all(self, value):
        for var in self.category_vars.values():
            var.set(value)

    def write_log(self, message):
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def get_unique_path(self, path):
        """Prevent overwriting existing files."""
        if not path.exists():
            return path

        counter = 1

        while True:
            new_path = path.with_name(
                f"{path.stem} ({counter}){path.suffix}"
            )

            if not new_path.exists():
                return new_path

            counter += 1

    def organize_files(self):
        if self.is_organizing:
            return

        folder = self.selected_folder.get()

        if not folder:
            messagebox.showwarning(
                "No Folder Selected",
                "Please select a folder first."
            )
            return

        downloads = Path(folder)

        if not downloads.is_dir():
            messagebox.showerror(
                "Invalid Folder",
                "The selected folder does not exist."
            )
            return

        selected = [
            name for name, var in self.category_vars.items()
            if var.get()
        ]

        if not selected:
            messagebox.showwarning(
                "No Categories",
                "Please select at least one category."
            )
            return

        files = [
            file for file in downloads.iterdir()
            if file.is_file()
        ]

        if not files:
            messagebox.showinfo(
                "No Files",
                "There are no files to organize."
            )
            return

        if not messagebox.askyesno(
            "Confirm Organization",
            f"Organize {len(files)} files in:\n\n{folder}?"
        ):
            return

        self.is_organizing = True
        self.organize_button.configure(state="disabled")

        self.progress["value"] = 0
        self.progress["maximum"] = len(files)

        moved_count = 0
        skipped_count = 0
        error_count = 0

        for index, file in enumerate(files, start=1):
            ext = file.suffix.lower()

            category = next(
                (
                    name for name in selected
                    if ext in self.folders[name]
                ),
                None
            )

            if category is None and "Others" in selected:
                category = "Others"

            if category is None:
                skipped_count += 1
                self.write_log(f"Skipped: {file.name}")
                continue

            try:
                target_folder = downloads / category
                target_folder.mkdir(exist_ok=True)

                target = self.get_unique_path(
                    target_folder / file.name
                )

                shutil.move(str(file), str(target))

                moved_count += 1
                self.write_log(
                    f"Moved: {file.name} -> {category}"
                )

            except OSError as error:
                error_count += 1
                self.write_log(
                    f"ERROR: {file.name} - {error}"
                )

            self.progress["value"] = index
            self.status_label.configure(
                text=f"Processing {index} of {len(files)} files..."
            )

            self.root.update_idletasks()

        self.status_label.configure(
            text="Organization completed!"
        )

        self.is_organizing = False
        self.organize_button.configure(state="normal")

        self.write_log("--------------------------------")
        self.write_log(f"Successfully moved: {moved_count}")
        self.write_log(f"Skipped: {skipped_count}")
        self.write_log(f"Errors: {error_count}")
        self.write_log("--------------------------------")

        messagebox.showinfo(
            "Organization Complete",
            f"Successfully moved: {moved_count}\n"
            f"Skipped: {skipped_count}\n"
            f"Errors: {error_count}\n\n"
            f"Location: {folder}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizer(root)
    root.mainloop()

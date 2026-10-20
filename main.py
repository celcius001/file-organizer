import shutil
from pathlib import Path

downloads = Path.home() / "Downloads"
folders = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Scripts": [".py", ".js", ".html", ".css", ".sh"],
    "Executables": [".exe", ".msi", ".bat", ".app"],
    "Others": []
}

for name in folders:
    (downloads / name).mkdir(exist_ok=True)
for file in list(downloads.iterdir()):
    ext = file.suffix.lower()
    for name, exts in folders.items():
        if file.is_file() and ext in exts:
            target =downloads / name / file.name
            shutil.move(str(file), str(target))

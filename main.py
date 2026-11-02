import shutil
from pathlib import Path

print("===================================")
print("       DOWNLOADS FILE ORGANIZER")
print("===================================")

input("\nPress ENTER to start organizing your Downloads folder...")

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

print("\nOrganizing files...\n")

# Create folders
for name in folders:
    (downloads / name).mkdir(exist_ok=True)

# Organize files
moved_count = 0

for file in list(downloads.iterdir()):
    if file.is_file():
        ext = file.suffix.lower()

        for name, exts in folders.items():
            if ext in exts:
                target = downloads / name / file.name
                shutil.move(str(file), str(target))
                moved_count += 1
                break

print("===================================")
print("       ORGANIZATION COMPLETE!")
print("===================================")
print(f"\nFiles successfully organized: {moved_count}")
print(f"Location: {downloads}")

input("\nPress ENTER to exit...")

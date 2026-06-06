import os
import shutil


FILE_TYPES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "Docs": {
        ".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"
    },
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm"},
}


def get_category(filename):
    """Return the folder category for a filename, or None if unsupported."""
    extension = os.path.splitext(filename)[1].lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category

    return None


def get_unique_path(destination_folder, filename):
    """Return a destination path that will not overwrite an existing file."""
    name, extension = os.path.splitext(filename)
    destination_path = os.path.join(destination_folder, filename)
    counter = 1

    while os.path.exists(destination_path):
        new_filename = f"{name}_{counter}{extension}"
        destination_path = os.path.join(destination_folder, new_filename)
        counter += 1

    return destination_path


def organize_files(directory_path):
    """Organize supported files in directory_path into Images, Docs, and Videos."""
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"Directory not found: {directory_path}")

    moved_files = 0

    for filename in os.listdir(directory_path):
        source_path = os.path.join(directory_path, filename)

        if not os.path.isfile(source_path):
            continue

        category = get_category(filename)
        if category is None:
            continue

        destination_folder = os.path.join(directory_path, category)
        os.makedirs(destination_folder, exist_ok=True)

        destination_path = get_unique_path(destination_folder, filename)
        shutil.move(source_path, destination_path)
        moved_files += 1
        print(f"Moved: {filename} -> {category}/")

    print(f"\nDone. Organized {moved_files} file(s).")
    return moved_files


if __name__ == "__main__":
    folder = input("Enter the directory path to organize: ").strip()
    organize_files(folder)
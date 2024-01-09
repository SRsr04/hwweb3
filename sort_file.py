import sys
from pathlib import Path
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor
import logging
from time import sleep

CATEGORIES = {
    "Audio": [".mp3"],
    "Video": [".mp4"],
    "Docs": [".txt", ".docx", ".pdf"],
    "Images": [".jpg", ".png", ".gif"],
    "Archives": [".zip", ".rar"],
    "Other": [".csv", ".html", ".exe", ".log"]
}

def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
        return "Other"
        

def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
    new_file_path = target_dir.joinpath(file.name)
    
    if not new_file_path.exists():
        file.rename(new_file_path)
    else:
        count = 1
        while True:
            new_name = f"{file.stem}_{count}{file.suffix}"
            new_file_path = target_dir.joinpath(new_name)
            if not new_file_path.exists():
                file.rename(new_file_path)
                break
            count += 1

def extract_archive(file: Path, extraction_dir: Path):
    
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(extraction_dir)

def sort_folder(path: Path) -> None:
    
    with ThreadPoolExecutor() as executor:
        futures = []
        for item in path.glob("**/*"):
            if item.is_file():
                category = get_categories(item)
                futures.append(executor.submit(move_file, item, category, path))
            elif item.is_dir(): 
                futures.append(executor.submit(item.rmdir))

        # Wait for all threads to complete
        for future in futures:
            future.result()
            
def main() -> str:
    
    try:
        path = Path("/шлях/до/папки")
        if not path.exists():
            return "Folder does not exist"

        sort_folder(path)

        return "All done"
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    print(main())


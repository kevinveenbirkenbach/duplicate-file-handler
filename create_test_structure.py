import os
import shutil
import hashlib
import random
import string

def create_test_directory(base_dir, num_files=5, duplicate_files=2):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Erstelle eine Liste von eindeutigen Dateinamen
    file_names = [f"file_{i}.txt" for i in range(num_files)]

    # Erstelle einige Dateien mit zufälligem Inhalt
    for file_name in file_names:
        with open(os.path.join(base_dir, file_name), 'w') as f:
            content = ''.join(random.choices(string.ascii_lowercase, k=20))
            f.write(content)

    # Erstelle Duplikate
    for i in range(duplicate_files):
        original = os.path.join(base_dir, file_names[i])
        duplicate = os.path.join(base_dir, f"dup_{file_names[i]}")
        shutil.copyfile(original, duplicate)

def create_file_structure():
    # Basisverzeichnisse erstellen
    base_dirs = ['test_dir1', 'test_dir2']
    for base_dir in base_dirs:
        create_test_directory(base_dir)

    # Erstelle eine Datei im ersten Verzeichnis und dupliziere sie im zweiten
    with open(os.path.join('test_dir1', 'unique_file.txt'), 'w') as f:
        f.write("This is a unique file.")

    shutil.copyfile(os.path.join('test_dir1', 'unique_file.txt'),
                    os.path.join('test_dir2', 'unique_file.txt'))

    # Erstelle eine zusätzliche einzigartige Datei im zweiten Verzeichnis
    with open(os.path.join('test_dir2', 'another_unique_file.txt'), 'w') as f:
        f.write("This is another unique file.")

    print("Test file structure created.")

if __name__ == "__main__":
    create_file_structure()

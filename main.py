import os
import sys
import hashlib
from collections import defaultdict
from filecmp import dircmp

def md5sum(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_duplicates(directory):
    hashes = defaultdict(list)
    for root, dirs, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            file_hash = md5sum(path)
            hashes[file_hash].append(path)
    return {file_hash: paths for file_hash, paths in hashes.items() if len(paths) > 1}

def print_diff(files):
    print("Text file differences:")
    for i in range(len(files) - 1):
        os.system(f"diff {files[i]} {files[i+1]}")

def delete_file(file_path):
    confirm = input(f"Do you want to delete this file? {file_path} [y/N] ")
    if confirm.lower() in ["y", "yes"]:
        os.remove(file_path)
        print(f"Deleted {file_path}")

def handle_duplicates(duplicates):
    for file_hash, files in duplicates.items():
        print(f"Duplicate files for hash {file_hash}:")
        for file in files:
            print(file)
        if "text" in os.popen(f"file -b --mime-type '{files[0]}'").read():
            print_diff(files)
        else:
            for file in files:
                print(f"File: {file}")
                print("Duplicate(s) of this file:")
                [print(duplicate) for duplicate in files if duplicate != file]
                delete_file(file)

def main(directory):
    if not directory:
        print("Directory path not provided")
        return

    duplicates = find_duplicates(directory)
    if not duplicates:
        print("No duplicates found.")
        return

    handle_duplicates(duplicates)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python3 script.py <directory>")

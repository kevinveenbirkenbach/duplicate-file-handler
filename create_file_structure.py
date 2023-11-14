import os
import shutil
import hashlib
import random
import string

def create_test_directory(base_dir, num_files=5, duplicate_files=2, depth=1):
    os.makedirs(base_dir, exist_ok=True)
    subdirs = [os.path.join(base_dir, f"subdir_{i}") for i in range(depth)]
    for subdir in subdirs:
        os.makedirs(subdir, exist_ok=True)

    for dir in [base_dir] + subdirs:
        file_names = [f"file_{i}.txt" for i in range(num_files)]
        for file_name in file_names:
            with open(os.path.join(dir, file_name), 'w') as f:
                content = ''.join(random.choices(string.ascii_lowercase, k=20))
                f.write(content)

        for i in range(min(duplicate_files, num_files)):
            original = os.path.join(dir, file_names[i])
            for dup_num in range(1, duplicate_files+1):
                duplicate = os.path.join(dir, f"dup_{dup_num}_{file_names[i]}")
                shutil.copyfile(original, duplicate)

def copy_directory_contents(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def create_file_structure(depth, num_files, duplicate_files):
    base_dirs = ['test_dir1', 'test_dir2']
    for base_dir in base_dirs:
        create_test_directory(base_dir, num_files, duplicate_files, depth)

    copy_directory_contents('test_dir1', 'test_dir3')

    print("Test file structure created.")

if __name__ == "__main__":
    create_file_structure(depth=2, num_files=5, duplicate_files=3)

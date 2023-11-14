import os
import argparse
import hashlib
from collections import defaultdict

def md5sum(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_duplicates(directories):
    hashes = defaultdict(list)
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                path = os.path.join(root, filename)
                file_hash = md5sum(path)
                hashes[file_hash].append(path)
    return {file_hash: paths for file_hash, paths in hashes.items() if len(paths) > 1}

def handle_modification(files, modification, mode, apply_to):
    if mode == 'preview':
        if modification == 'show':
            print("Would show the following duplicate files:")
            for file in files:
                if file.startswith(tuple(apply_to)):
                    print(file)
    elif mode == 'act':
        if modification == 'delete':
            for file in files:
                if file.startswith(tuple(apply_to)):
                    print(f"Deleting {file}")
                    os.remove(file)
        elif modification == 'hardlink':
            # Implement hardlink logic here
            pass
        elif modification == 'symlink':
            # Implement symlink logic here
            pass
    elif mode == 'interactive':
        for file in files:
            if file.startswith(tuple(apply_to)):
                answer = input(f"Do you want to {modification} this file? {file} [y/N] ")
                if answer.lower() in ['y', 'yes']:
                    # Implement deletion, hardlink or symlink logic here
                    pass

def main(args):
    directories = args.directories
    apply_to = args.apply_to or directories
    duplicates = find_duplicates(directories)
    
    if not duplicates:
        print("No duplicates found.")
        return
    
    for file_hash, files in duplicates.items():
        if args.mode == 'preview' or (args.mode == 'interactive' and args.modification == 'show'):
            print(f"Duplicate files for hash {file_hash}:")
            [print(file) for file in files if file.startswith(tuple(apply_to))]
        else:
            handle_modification(files, args.modification, args.mode, apply_to)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and handle duplicate files.")
    parser.add_argument('directories', nargs='*', default=['./'], help="Directories to scan for duplicates.")
    parser.add_argument('--apply-to', nargs='*', help="Directories to apply modifications to.")
    parser.add_argument('--modification', choices=['delete', 'hardlink', 'symlink', 'show'], default='show', help="Modification to perform on duplicates.")
    parser.add_argument('--mode', choices=['act', 'preview', 'interactive'], default='preview', help="How to apply the modifications.")
    
    args = parser.parse_args()
    
    if args.apply_to and args.modification not in ['delete', 'hardlink', 'symlink']:
        parser.error("--apply-to requires --modification to be 'delete', 'hardlink', or 'symlink'.")
    if not args.apply_to and args.modification != 'show':
        parser.error("Without --apply-to only 'show' modification is allowed.")
    
    main(args)

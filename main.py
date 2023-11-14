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

def handle_file_modification(file, modification):
    if modification == 'delete':
        print(f"Deleting {file}")
        os.remove(file)
    elif modification == 'hardlink':
        # Find the first file that is not the same as `file` to link to
        original_file = next((f for f in files if f != file), None)
        if original_file:
            os.remove(file)
            os.link(original_file, file)
            print(f"Replaced {file} with a hardlink to {original_file}")
    elif modification == 'symlink':
        original_file = next((f for f in files if f != file), None)
        if original_file:
            os.remove(file)
            os.symlink(original_file, file)
            print(f"Replaced {file} with a symlink to {original_file}")

def handle_modification(files, modification, mode, apply_to):
    for file in files:
        if file.startswith(tuple(apply_to)):
            if mode == 'preview':
                print(f"Would perform {modification} on {file}")
            elif mode == 'act':
                handle_file_modification(file, modification)
            elif mode == 'interactive':
                answer = input(f"Do you want to {modification} this file? {file} [y/N] ")
                if answer.lower() in ['y', 'yes']:
                    handle_file_modification(file, modification)

def main(args):
    directories = args.directories
    apply_to = args.apply_to or directories
    duplicates = find_duplicates(directories)
    
    if not duplicates:
        print("No duplicates found.")
        return
    
    for file_hash, files in duplicates.items():
        print(f"Duplicate files for hash {file_hash}:")
        [print(file) for file in files if file.startswith(tuple(apply_to))]
        handle_modification(files, args.modification, args.mode, apply_to)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and handle duplicate files.")
    parser.add_argument('directories', nargs='*', help="Directories to scan for duplicates.")
    parser.add_argument('--apply-to', nargs='*', help="Directories to apply modifications to.")
    parser.add_argument('--modification', choices=['delete', 'hardlink', 'symlink', 'show'], default='show', help="Modification to perform on duplicates.")
    parser.add_argument('--mode', choices=['act', 'preview', 'interactive'], default='preview', help="How to apply the modifications.")

    args = parser.parse_args()
    
    if not args.directories:
        parser.print_help()
        parser.exit()

    if args.apply_to and args.modification not in ['delete', 'hardlink', 'symlink']:
        parser.error("--apply-to requires --modification to be 'delete', 'hardlink', or 'symlink'.")
    if not args.apply_to and args.modification != 'show':
        parser.error("Without --apply-to only 'show' modification is allowed.")

    main(args)

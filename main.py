import os
import argparse
import hashlib
from collections import defaultdict, Counter
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def md5sum(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def file_hashing_job(path):
    file_hash = md5sum(path)
    if file_hash:
        return file_hash, path

def find_duplicates(directories, file_type):
    with ProcessPoolExecutor() as executor:
        futures = []
        for directory in directories:
            for root, dirs, files in tqdm(os.walk(directory, followlinks=False), desc=f"Indexing files of {directory}", unit="directory"):
                for filename in files:
                    if file_type and not filename.endswith(file_type):
                        continue
                    path = os.path.join(root, filename)
                    if not os.path.islink(path):
                        futures.append(executor.submit(file_hashing_job, path))

        hashes = defaultdict(list)
        for future in tqdm(futures, desc="Processing files", unit="file"):
            result = future.result()
            if result:
                file_hash, path = result
                hashes[file_hash].append(path)

    return {file_hash: paths for file_hash, paths in hashes.items() if len(paths) > 1}

def handle_file_modification(original_file, duplicate_file, modification):
    if modification == 'delete':
        print(f"Deleting {duplicate_file}")
        os.remove(duplicate_file)
    elif modification == 'hardlink':
        os.remove(duplicate_file)
        os.link(original_file, duplicate_file)
        print(f"Replaced {duplicate_file} with a hardlink to {original_file}")
    elif modification == 'symlink':
        os.remove(duplicate_file)
        os.symlink(original_file, duplicate_file)
        print(f"Replaced {duplicate_file} with a symlink to {original_file}")
        
def handle_modification(files, modification, mode, apply_to):
    original_file = next((f for f in files if not f.startswith(tuple(apply_to))), files[0])
    for duplicate_file in files:
        if duplicate_file != original_file:
            if duplicate_file.startswith(tuple(apply_to)):
                if mode == 'preview' and modification != 'show':
                    print(f"Would perform {modification} on {duplicate_file}")
                elif mode == 'act':
                    handle_file_modification(original_file, duplicate_file, modification)
                elif mode == 'interactive':
                    answer = input(f"Do you want to {modification} this file? {duplicate_file} [y/N] ")
                    if answer.lower() in ['y', 'yes']:
                        handle_file_modification(original_file, duplicate_file, modification)
            else:
                print(f"Duplicate file (unmodified): {duplicate_file}")
        elif modification != 'show':
            print(f"Original file kept: {original_file}")
    print()


def main(args):
    directories = args.directories
    apply_to = args.apply_to or directories
    duplicates = find_duplicates(directories,args.file_type)
    
    if not duplicates:
        print("No duplicates found.")
        return
    
    for file_hash, files in duplicates.items():
        print(f"Duplicate files for hash {file_hash}:")
        [print(file) for file in files if file.startswith(tuple(directories))]
        handle_modification(files, args.modification, args.mode, apply_to)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and handle duplicate files.")
    parser.add_argument('directories', nargs='*', help="Directories to scan for duplicates.")
    parser.add_argument('--apply-to', nargs='*', help="Filter directories to apply modifications to.")
    parser.add_argument('--modification', choices=['delete', 'hardlink', 'symlink', 'show'], default='show', help="Modification to perform on duplicates.")
    parser.add_argument('--mode', choices=['act', 'preview', 'interactive'], default='preview', help="How to apply the modifications.")
    parser.add_argument('-f', '--file-type', help="Filter by file type (e.g., '.txt' for text files).", default=None)

    args = parser.parse_args()
    
    if not args.directories:
        parser.print_help()
        parser.exit()

    if args.apply_to and args.modification not in ['delete', 'hardlink', 'symlink']:
        parser.error("--apply-to requires --modification to be 'delete', 'hardlink', or 'symlink'.")
    if not args.apply_to and args.modification != 'show':
        parser.error("Without --apply-to only 'show' modification is allowed.")

    main(args)

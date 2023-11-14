# Duplicate File Handler

This repository contains a Python script for identifying and handling duplicate files in a directory and its subdirectories based on their MD5 hash. It allows for filtering by file type and provides options for handling duplicates such as deletion, hard linking, or sym linking.

## Author
- Kevin Veen-Birkenbach
- Email: kevin@veen.world
- Website: [https://www.veen.world](https://www.veen.world)

This repository was enhanced with the help of [OpenAI's ChatGPT](https://chat.openai.com/share/825931d6-1e33-40b0-8dfc-914b3f852eeb).

## Setup 
To use the script, ensure you have Python installed on your system. No additional libraries are required as the script uses standard Python libraries.

## Usage

### Identifying and Handling Duplicates

`main.py` is a Python script to identify all duplicate files in the specified directories. It can also filter by file type and handle duplicates by deleting them or replacing them with hard or symbolic links.

```bash
python main.py [options] directories
```

#### Options
- `--apply-to`: Directories to apply modifications to.
- `--modification`: Action to perform on duplicates - `delete`, `hardlink`, `symlink`, or `show` (default).
- `--mode`: How to apply the modifications - `act`, `preview`, `interactive` (default: `preview`).
- `-f`, `--file-type`: Filter by file type (e.g., `.txt` for text files).

### Creating Test File Structure

`create_file_structure.py` is a utility script to create a test file structure with duplicate files for testing purposes.

```bash
python create_file_structure.py
```

## Example

To preview duplicate `.txt` files in `test_dir1` and `test_dir2`:

```bash
python main.py --file-type .txt --mode preview test_dir1 test_dir2
```

To interactively delete duplicates in `test_dir2`:

```bash
python main.py --apply-to test_dir2 --modification delete --mode interactive test_dir1 test_dir2
```

## License

This project is licensed under the terms of the [MIT License](LICENSE).
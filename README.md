# Duplicate File Handler

This repository contains two bash scripts for handling duplicate files in a directory and its subdirectories.

The scripts may need to be modified depending on the specific requirements of your system or the specific use case. They currently operate by comparing the MD5 hash of files to find duplicates, which is a common but not foolproof method.

## Author

**Kevin Veen-Birkenbach**
- Email: kevin@veen.world
- Website: [https://www.veen.world](https://www.veen.world)

This repository was created with the help of [OpenAI's ChatGPT](https://openai.com/research/chatgpt) (Link to the conversation).

## Setup 
These scripts will help you manage duplicate files in your directories. Please make sure to adjust permissions on the scripts to be executable with `chmod +x list_duplicates.sh delete_duplicates.sh` before running. 

## Usage

### 1. List Duplicate Files

`list_duplicates.sh` is a script to list all duplicate files in a specified directory and its subdirectories. For text files, it will also display the diffs.

```bash
./list_duplicates.sh /path/to/directory
```

### 2. Delete Duplicate Files

`delete_duplicates.sh` is a script to find and delete duplicate files in a specified directory and its subdirectories. It will ask for confirmation before deleting each file and display the paths of its duplicates.

```bash
./delete_duplicates.sh /path/to/directory
```

## License

This project is licensed under the terms of the [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.de.html).

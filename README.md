# Duplicate File Handler (dufiha) 🔍
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-blue?logo=github)](https://github.com/sponsors/kevinveenbirkenbach) [![Patreon](https://img.shields.io/badge/Support-Patreon-orange?logo=patreon)](https://www.patreon.com/c/kevinveenbirkenbach) [![Buy Me a Coffee](https://img.shields.io/badge/Buy%20me%20a%20Coffee-Funding-yellow?logo=buymeacoffee)](https://buymeacoffee.com/kevinveenbirkenbach) [![PayPal](https://img.shields.io/badge/Donate-PayPal-blue?logo=paypal)](https://s.veen.world/paypaldonate)


[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](./LICENSE) [![GitHub stars](https://img.shields.io/github/stars/kevinveenbirkenbach/duplicate-file-handler.svg?style=social)](https://github.com/kevinveenbirkenbach/duplicate-file-handler/stargazers)

Duplicate File Handler is a Python CLI tool for identifying and handling duplicate files within one or more directories based on their MD5 hashes. With flexible file-type filtering and multiple action modes, you can efficiently delete duplicates or replace them with hard or symbolic links.

---

## 🛠 Features

- **Duplicate Detection:** Computes MD5 hashes for files to find duplicates.
- **File Type Filtering:** Process only files with a specified extension.
- **Multiple Modification Options:** Choose to delete duplicates, replace them with hard links, or create symbolic links.
- **Flexible Modes:** Operate in preview, interactive, or active mode to suit your workflow.
- **Parallel Processing:** Utilizes process pooling for efficient scanning of large directories.

---

## 📥 Installation

Install Duplicate File Handler via [Kevin's Package Manager](https://github.com/kevinveenbirkenbach/package-manager) under the alias `dufiha`:

```bash
package-manager install dufiha
```

This command installs the tool globally, making it available as `dufiha` in your terminal. 🚀

---

## 🚀 Usage

Run Duplicate File Handler by specifying one or more directories to scan for duplicates:

```bash
dufiha [options] directory1 directory2 ...
```

### Options

- **`--apply-to`**: Directories to which modifications should be applied.
- **`--modification`**: Action to perform on duplicates:
  - `delete` – Delete duplicate files.
  - `hardlink` – Replace duplicates with hard links.
  - `symlink` – Replace duplicates with symbolic links.
  - `show` – Only display duplicate files (default).
- **`--mode`**: How to apply modifications:
  - `act` – Execute changes immediately.
  - `preview` – Preview changes without making any modifications.
  - `interactive` – Ask for confirmation before processing each duplicate.
- **`-f, --file-type`**: Filter by file type (e.g., `.txt` for text files).

### Example Commands

- **Preview duplicate `.txt` files in two directories:**

  ```bash
  dufiha --file-type .txt --mode preview test_dir1 test_dir2
  ```

- **Interactively delete duplicates in a specific directory:**

  ```bash
  dufiha --apply-to test_dir2 --modification delete --mode interactive test_dir1 test_dir2
  ```

- **Show duplicates without modifying any files:**

  ```bash
  dufiha --mode show test_dir1
  ```

---

## 🧑‍💻 Author

Developed by **Kevin Veen-Birkenbach**  
- 📧 [kevin@veen.world](mailto:kevin@veen.world)  
- 🌐 [https://www.veen.world](https://www.veen.world)

This project was enhanced with assistance from [OpenAI's ChatGPT](https://chat.openai.com/share/825931d6-1e33-40b0-8dfc-914b3f852eeb).

---

## 📜 License

This project is licensed under the **GNU Affero General Public License, Version 3, 19 November 2007**.  
See the [LICENSE](./LICENSE) file for details.

---

## 🤝 Contributions

Contributions are welcome! Please feel free to fork the repository, submit pull requests, or open issues to help improve Duplicate File Handler. Let’s make file management smarter and more efficient! 😊

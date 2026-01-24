# Project Context Extractor

A smart Python utility to condense an entire project folder into a single text file. It generates a visual tree of the hierarchy and appends the source code, optimized specifically for **LLM context sharing**.

## Features
- **Visual Tree View:** Generates a clean hierarchy of your project structure.
- **Auto-Logic Detection:** If no extensions are specified, it automatically includes all source files while skipping locks (`poetry.lock`, `package-lock.json`), documentation (`README`, `LICENSE`), and git files.
- **Smart Filtering:** Automatically excludes hidden folders (like `.git`, `.pytest_cache`, `.vscode`, `.idea`) and common heavy directories (`node_modules`, `venv`, `env`).
- **Media & Size Safety:** Skips the content of images, videos, and audio files by default. It also ignores files larger than 500KB to save tokens.
- **Git Friendly:** Automatically adds the output file to `.gitignore` to prevent accidental commits (unless overridden).

---

## Usage

### 1. Basic Usage (Recommended for LLMs)
To grab all relevant code logic while automatically skipping binary files, hidden folders, and heavy locks:

```bash
python resume.py -path "/path/to/your/project"
```

### 2. Selective Extensions
If you only want specific file types:

```bash
python resume.py -path "/path/to/your/project" -extensions py js html
```

### 3. Advanced Options
- `-max-kb`: Change the file size limit (default 500KB).
- `-read-media`: Force the script to read the content of media files (binary data).
- `-track`: Prevent the script from adding the output file to `.gitignore`.
- `-exclude-dirs`: Add specific folders to the exclusion list.

---

## Helper Tool: Discover Extensions

Use the helper script to list all unique file extensions present in the target folder:

```bash
python whichextensions.py -path "/path/to/your/project"
```

---

## Output
The script creates **`ResumeFolderInFile.txt`** in the target directory, containing:
1. The filtered project tree.
2. The content of each valid file, separated by clear headers.
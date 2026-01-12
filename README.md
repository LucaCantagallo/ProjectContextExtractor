# Project Context Extractor

A simple Python utility to condense a project folder into a single text file.  
It generates a visual tree of the relevant file hierarchy and appends the content of selected file types.

**Perfect for sharing context with LLMs for code analysis.**

## Features
- **Tree View:** Visual hierarchy of your project structure.
- **Content Aggregation:** Reads files and appends them to the output.
- **Smart Filtering:** Only includes extensions you specify.
- **Safe:** Read-only mode for source files.
- **Git Friendly:** Automatically adds the output file to `.gitignore` to prevent accidental commits (unless overridden).
- **Extension Discovery:** Includes a helper script (`whichextensions.py`) to quickly list all file types present in a project.

## Helper Tool: Discover Extensions

Not sure which extensions are in the project? Use the helper script to list all unique file extensions found in the target folder:

```bash
python whichextensions.py -path "/path/to/your/project"
```
This will output a clean list (e.g., **css**, **html**, **js**), which you can then copy into the main command.
---
## Usage

Run the script from your terminal:

```bash
python resume.py -path "/path/to/your/project" -extensions "py" "js" "html"
```

### Arguments
- **path:** The root directory of the project you want to summarize.
- **extensions:** Space-separated list of file extensions to include (e.g., **py js css**).
- **track (Optional):** If used, the output file will NOT be added to .gitignore. By default, the script adds **ResumeFolderInFile.txt** to **.gitignore** to keep your repo clean.

## Output
The script creates a file named ResumeFolderInFile.txt in the target root directory containing:
- The folder structure (Tree).
- The content of every matching file found.
import os
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Genera un file di testo con l'albero e il contenuto dei file di un progetto.")
    parser.add_argument("-path", required=True, help="Path della root del progetto")
    parser.add_argument("-extensions", nargs='+', required=True, help="Lista delle estensioni da includere (es. py js html)")
    parser.add_argument("-track", action="store_true", help="Se usato, NON aggiunge il file di output al .gitignore (permettendone il tracking)")
    return parser.parse_args()

def is_valid_file(filename, extensions):
    return any(filename.lower().endswith(f".{ext.lower()}") for ext in extensions)

def update_gitignore(root_path, filename):
    gitignore_path = os.path.join(root_path, ".gitignore")
    
    if not os.path.exists(gitignore_path):
        return

    try:
        with open(gitignore_path, "r") as f:
            lines = f.readlines()
        
        if any(line.strip() == filename for line in lines):
            return 

        with open(gitignore_path, "a") as f:
            prefix = "\n" if lines and not lines[-1].endswith("\n") else ""
            f.write(f"{prefix}{filename}\n")
        print(f"INFO: '{filename}' aggiunto a .gitignore.")
        
    except Exception as e:
        print(f"WARNING: Non sono riuscito ad aggiornare il .gitignore: {e}")

def generate_tree(dir_path, extensions, prefix=""):
    tree_str = ""
    try:
        entries = sorted(os.listdir(dir_path))
    except OSError:
        return ""

    entries = [e for e in entries if not e.startswith('.')]
    
    files = [e for e in entries if os.path.isfile(os.path.join(dir_path, e)) and is_valid_file(e, extensions)]
    dirs = [e for e in entries if os.path.isdir(os.path.join(dir_path, e))]

    filtered_dirs = []
    for d in dirs:
        sub_tree = generate_tree(os.path.join(dir_path, d), extensions, prefix)
        if sub_tree:
            filtered_dirs.append((d, sub_tree))

    if not files and not filtered_dirs:
        return ""

    for i, f in enumerate(files):
        is_last = (i == len(files) - 1) and not filtered_dirs
        connector = "└── " if is_last else "├── "
        tree_str += f"{prefix}{connector}{f}\n"

    for i, (d_name, sub_content) in enumerate(filtered_dirs):
        is_last = (i == len(filtered_dirs) - 1)
        connector = "└── " if is_last else "├── "
        tree_str += f"{prefix}{connector}{d_name}/\n"
        
        extension = "    " if is_last else "│   "
        sub_lines = sub_content.splitlines()
        for line in sub_lines:
            tree_str += f"{prefix}{extension}{line}\n"

    return tree_str

def main():
    args = get_args()
    root_path = os.path.abspath(args.path)
    extensions = [e.lstrip('.') for e in args.extensions]
    output_filename = "ResumeFolderInFile.txt"
    output_path = os.path.join(root_path, output_filename)

    if not args.track:
        update_gitignore(root_path, output_filename)

    valid_files_paths = []
    for root, _, files in os.walk(root_path):
        for file in files:
            if is_valid_file(file, extensions):
                if os.path.abspath(os.path.join(root, file)) != output_path:
                    valid_files_paths.append(os.path.join(root, file))

    tree_output = f"GERARCHIA (Root: {root_path})\n\n.\n" + generate_tree(root_path, extensions)

    try:
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write(tree_output)
            out_file.write("\n" + "="*50 + "\n\n")
            
            for file_path in valid_files_paths:
                rel_path = os.path.relpath(file_path, root_path)
                out_file.write(f"FILE: {rel_path}\n")
                out_file.write("-" * 20 + "\n")
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                        out_file.write(content)
                except Exception as e:
                    out_file.write(f"[ERRORE NELLA LETTURA DEL FILE: {e}]")
                
                out_file.write("\n\n" + "="*50 + "\n\n")
        
        print(f"SUCCESS: File creato in: {output_path}")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
import os
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Genera un file di testo con l'albero e il contenuto dei file di un progetto.")
    parser.add_argument("-path", required=True, help="Path della root del progetto")
    parser.add_argument("-extensions", nargs='*', default=[], help="Lista delle estensioni da includere. Se vuoto, include solo file di codice/logica.")
    parser.add_argument("-exclude-dirs", nargs='*', default=['node_modules', '__pycache__', 'venv', 'env', 'dist', 'build'], help="Ulteriori cartelle da escludere (oltre a quelle nascoste).")
    parser.add_argument("-max-kb", type=int, default=500, help="Dimensione massima in KB per leggere il contenuto del file (default: 500)")
    parser.add_argument("-read-media", action="store_true", help="Se usato, legge anche il contenuto di immagini e video")
    parser.add_argument("-track", action="store_true", help="Se usato, NON aggiunge il file di output al .gitignore")
    return parser.parse_args()

def is_media_file(filename):
    media_exts = {
        'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp', 'ico',
        'mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv',
        'mp3', 'wav', 'flac', 'm4a'
    }
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    return ext in media_exts

def is_ignored_by_default(filename):
    ignored_names = {
        'poetry.lock', 'package-lock.json', 'yarn.lock', '.gitignore', 
        'readme.md', 'license', 'changelog.md', 'contributing.md',
        'composer.lock', 'pnpm-lock.yaml'
    }
    return filename.lower() in ignored_names

def is_valid_file(filename, extensions):
    if not extensions:
        if is_ignored_by_default(filename):
            return False
        return True
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

def generate_tree(dir_path, extensions, exclude_dirs, prefix=""):
    tree_str = ""
    try:
        entries = sorted(os.listdir(dir_path))
    except OSError:
        return ""

    entries = [e for e in entries if not e.startswith('.')]
    files = [e for e in entries if os.path.isfile(os.path.join(dir_path, e)) and is_valid_file(e, extensions)]
    dirs = [e for e in entries if os.path.isdir(os.path.join(dir_path, e)) and e not in exclude_dirs]

    filtered_dirs = []
    for d in dirs:
        sub_tree = generate_tree(os.path.join(dir_path, d), extensions, exclude_dirs, prefix)
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
        extension_line = "    " if is_last else "│   "
        sub_lines = sub_content.splitlines()
        for line in sub_lines:
            tree_str += f"{prefix}{extension_line}{line}\n"
    return tree_str

def main():
    args = get_args()
    root_path = os.path.abspath(args.path)
    extensions = [e.lstrip('.') for e in args.extensions] if args.extensions else []
    exclude_dirs = args.exclude_dirs
    output_filename = "ResumeFolderInFile.txt"
    output_path = os.path.join(root_path, output_filename)

    if not args.track:
        update_gitignore(root_path, output_filename)

    valid_files_paths = []
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in exclude_dirs]
        for file in files:
            if is_valid_file(file, extensions):
                file_abs_path = os.path.abspath(os.path.join(root, file))
                if file_abs_path != output_path:
                    valid_files_paths.append(file_abs_path)

    tree_output = f"GERARCHIA (Root: {os.path.basename(root_path)})\n\n.\n" + generate_tree(root_path, extensions, exclude_dirs)

    try:
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write(tree_output)
            out_file.write("\n" + "="*50 + "\n\n")
            
            for file_path in valid_files_paths:
                rel_path = os.path.relpath(file_path, root_path)
                file_size_kb = os.path.getsize(file_path) / 1024
                
                out_file.write(f"FILE: {rel_path}\n")
                out_file.write("-" * 20 + "\n")
                
                is_media = is_media_file(file_path)
                
                if file_size_kb > args.max_kb:
                    out_file.write(f"[CONTENUTO IGNORATO: File troppo grande ({file_size_kb:.2f} KB)]")
                elif is_media and not args.read_media:
                    out_file.write("[CONTENUTO IGNORATO: File multimediale]")
                else:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                            out_file.write(f.read())
                    except Exception as e:
                        out_file.write(f"[ERRORE NELLA LETTURA DEL FILE: {e}]")
                
                out_file.write("\n\n" + "="*50 + "\n\n")
        
        print(f"SUCCESS: File creato in: {output_path}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
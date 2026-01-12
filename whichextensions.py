import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", required=True)
    return parser.parse_args()

def main():
    args = get_args()
    root_path = os.path.abspath(args.path)
    found_extensions = set()

    try:
        for root, dirs, files in os.walk(root_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if file.startswith('.'):
                    continue
                
                _, ext = os.path.splitext(file)
                if ext:
                    found_extensions.add(ext.lstrip('.').lower())

        if not found_extensions:
            print("Nessuna estensione trovata.")
        else:
            for ext in sorted(list(found_extensions)):
                print(ext)

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    main()
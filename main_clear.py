import os
import shutil

def clear_python_caches(root_dir="."):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "__pycache__" in dirnames:
            cache_path = os.path.join(dirpath, "__pycache__")
            print(f"Видаляю: {cache_path}")
            shutil.rmtree(cache_path)
            dirnames.remove("__pycache__")
        
        for filename in filenames:
            if filename.endswith(".pyc"):
                file_path = os.path.join(dirpath, filename)
                print(f"Видаляю: {file_path}")
                os.remove(file_path)

if __name__ == "__main__":
    clear_python_caches()
import os
import importlib
import inspect
from typing import Any, Callable

_plugins_cache = {}
def load_plugins(plugin: str):
    if plugin in _plugins_cache:
        return _plugins_cache[plugin]

    mods = []
    root_path = plugin.replace('.', os.sep)  # наприклад "plugins.messages" -> "plugins/messages"

    for root, _, files in os.walk(root_path):
        for f in files:
            if f.endswith('.py') and not f.startswith('__'):
                rel_path = os.path.relpath(root, root_path)
                parts = [plugin]  # базовий пакет

                if rel_path != '.':
                    parts += rel_path.replace(os.sep, '.').split('.')

                parts.append(f[:-3])  # ім'я модуля без .py

                module_name = '.'.join(parts)
                mod = importlib.import_module(module_name)
                mods.append(mod)

    _plugins_cache[plugin] = mods
    return mods

def get_plugins(plugin: str):
    global _plugins_cache
    if plugin not in _plugins_cache:
        _plugins_cache[plugin] = load_plugins(plugin)
    return _plugins_cache[plugin]

def get_methods(name: str, path: str, method: str):
    methods = []

    print(f"🟢 {name}")
    print(f"  🔷 {method}")
    print(f"  🔶 {path}")

    path_len = len(path)
    last_parts = []
    last_parts_len = 0

    for mod in get_plugins(path):
        method_obj = getattr(mod, method, None)
        if callable(method_obj):
            subfolder = mod.__name__[path_len:]
            subfolder = subfolder[1:] if subfolder.startswith('.') else subfolder
            parts = subfolder.split('.')
            folder_parts = parts[:-1]
            folder_parts_len = len(folder_parts)
            module_name = parts[-1]
            common_len = next((i for i, (a, b) in enumerate(zip(folder_parts, last_parts)) if a != b), min(folder_parts_len, last_parts_len))
            sig = inspect.signature(method_obj)

            for i in range(common_len, folder_parts_len):
                print(f"    {'  ' * i}🔸 {folder_parts[i]}")

            link = f"file://d:/tbot/{mod.__name__.replace('.', os.sep)}.py"
            clickable_text = f"\x1b]8;;{link} \x1b\\{module_name}\x1b]8;;\x1b\\"
            colored_text = f"\033[38;2;170;170;255m{clickable_text}\033[0m"

            print(f"  {'  ' * (folder_parts_len + 1)}🔹 {colored_text} {sig}")
            
            last_parts = folder_parts
            last_parts_len = folder_parts_len
            
            methods.append(method_obj)

    return methods

def call_plugins(name:str, path: str, method: str, fn: Callable[[Any], None]):
    for method  in get_methods(name, path, method):
        fn(method)


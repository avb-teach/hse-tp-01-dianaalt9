import os
import shutil
import sys

args = sys.argv[1:]
if len(args) == 2:
    input_dir, output_dir = args
    max_depth = None
elif len(args) == 4 and args[2] == "--max_depth":
    input_dir, output_dir = args[0], args[1]
    try:
        max_depth = int(args[3])
    except ValueError:
        sys.exit("Ошибка: max_depth должно быть числом.")
else:
    sys.exit("Использование: script.py <input_dir> <output_dir> [--max_depth N]")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def generate_unique_filename(folder, original_name):
    name, extension = os.path.splitext(original_name)
    counter = 1
    new_name = original_name
    while os.path.exists(os.path.join(folder, new_name)):
        new_name = f"{name}{counter}{extension}"
        counter += 1
    return os.path.join(folder, new_name)

def get_folder_depth(base, current):
    relative_path = os.path.relpath(current, base)
    return 0 if relative_path == '.' else relative_path.count(os.sep) + 1

for current_dir, subdirs, filenames in os.walk(input_dir):
    current_depth = get_folder_depth(input_dir, current_dir)
    if max_depth is not None and current_depth > max_depth:
        subdirs[:] = []
        continue

    for file in filenames:
        source_path = os.path.join(current_dir, file)
        destination_path = generate_unique_filename(output_dir, file)
        shutil.copy2(source_path, destination_path)


import os
import shutil
import sys

input_dir, output_dir = "", ""
max_depth = None

if len(sys.argv) == 3:
    _, input_dir, output_dir = sys.argv
elif len(sys.argv) == 5 and sys.argv[3] == "--max_depth":
    _, input_dir, output_dir, _, max_depth = sys.argv
    try:
        max_depth = int(sys.argv[4])
    except ValueError:
        sys.exit(1)
else:
    sys.exit(1)

os.makedirs(output_dir, exist_ok=True)

def get_unique_path(path):
    base, ext = os.path.splitext(path)
    i = 1
    new_path = f"{base}_{i}{ext}"
    while os.path.exists(new_path):
        i += 1
        new_path = f"{base}_{i}{ext}"
    return new_path

def get_depth(start_path, current_path):
    rel_path = os.path.relpath(current_path, start_path)
    if rel_path == ".":
        return 0
    return rel_path.count(os.sep) + 1

for root, dirs, files in os.walk(input_dir):
    depth = get_depth(input_dir, root)
    if max_depth is not None and depth > max_depth:
        dirs[:] = []
        continue

    rel_root = os.path.relpath(root, input_dir)
    target_root = os.path.join(output_dir, rel_root) if rel_root != "." else output_dir
    os.makedirs(target_root, exist_ok=True)

    for file in files:
        src_file = os.path.join(root, file)
        dst_file = os.path.join(target_root, file)

        if os.path.exists(dst_file):
            existing_dst_file_new_name = get_unique_path(dst_file)
            os.rename(dst_file, existing_dst_file_new_name)

        dst_file_final = get_unique_path(dst_file) if os.path.exists(dst_file) else dst_file
        shutil.copy2(src_file, dst_file_final)

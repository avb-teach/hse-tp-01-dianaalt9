import os
import shutil
import sys

input_dir, output_dir = "", ""
max_depth = None

if len(sys.argv) == 3:
    _, input_dir, output_dir = sys.argv
    max_depth = 1
elif len(sys.argv) == 5 and sys.argv[3] == "--max_depth":
    _, input_dir, output_dir, _, max_depth = sys.argv
    try:
        max_depth = int(sys.argv[4])
    except ValueError:
        sys.exit(1)
else:
    sys.exit(1)

os.makedirs(output_dir, exist_ok=True)

def get_tail(parts, n):
    if n > 1:
        return os.path.join(*parts[len(parts) - n:])
    else:
        return os.path.basename(parts[-1])

def get_path(f):
    rel_path = os.path.relpath(f, input_dir)
    parts = rel_path.split(os.sep)
    if max_depth is None or len(parts) <= max_depth:
        return rel_path
    else:
        return get_tail(parts, max_depth)

def get_unique(dst_path):
    base, ext = os.path.splitext(dst_path)
    counter = 1
    new_path = dst_path
    while os.path.exists(new_path):
        new_path = f"{base}_{counter}{ext}"
        counter += 1
    return new_path

for root, _, files in os.walk(input_dir):
    for file in files:
        abs_path = os.path.join(root, file)
        rel_path = get_path(abs_path)
        dst_path = os.path.join(output_dir, rel_path)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        final_path = get_unique(dst_path)
        shutil.copy2(abs_path, final_path)

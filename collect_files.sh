#!/bin/bash

if [ "$#" -eq 2 ]; then
    input_dir="$1"
    output_dir="$2"
    python3 collect_files.py "$input_dir" "$output_dir"
elif [ "$#" -eq 4 ] && [ "$3" = "--max_depth" ]; then
    input_dir="$1"
    output_dir="$2"
    max_depth="$4"
    python3 collect_files.py "$input_dir" "$output_dir" --max_depth "$max_depth"
else
    echo "Usage:"
    echo "  $0 /path/to/input_dir /path/to/output_dir"
    echo "  $0 /path/to/input_dir /path/to/output_dir --max_depth N"
    exit 1
fi

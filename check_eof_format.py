#!/usr/bin/env python3
"""Detect Python files with problematic endings."""

import glob
import os
import shlex
import sys


def count_blank_lines_at_end(data):
    count = 0
    lines = data.splitlines()

    for line in reversed(lines):
        if line.strip():
            break
        count += 1

    return count


def collect_files(patterns):
    files = set()
    for pattern in patterns:
        for name in glob.glob(pattern):
            if os.path.isfile(name):
                files.add(name)
    return sorted(files)


def get_patterns():
    if len(sys.argv) > 1:
        return sys.argv[1:]

    text = input("Check files or glob patterns: ").strip()
    return shlex.split(text)


def main():
    patterns = get_patterns()
    if not patterns:
        print("No input provided.")
        return 2

    files = collect_files(patterns)
    if not files:
        print("No files matched.")
        return 2

    missing = []
    trailing_spaces = []

    for filename in files:
        with open(filename, "rb") as file:
            data = file.read()

        if not data.endswith(b"\n"):
            missing.append(filename)

        trailing_line_count = count_blank_lines_at_end(data)
        if trailing_line_count:
            trailing_spaces.append((filename, trailing_line_count))

    if missing:
        print("[Missing final newline]")
        for filename in missing:
            print(filename)

    if trailing_spaces:
        if missing:
            print()
        print("[Trailing whitespace-only line]")
        for filename, line_count in trailing_spaces:
            print(f"{filename} ({line_count} trailing line(s))")
    print()
    print(f"Checked: {len(files)} file(s)")
    print(f"Missing final newline: {len(missing)} file(s)")
    print(f"Trailing whitespace-only line: {len(trailing_spaces)} file(s)")
    return 1 if missing or trailing_spaces else 0


if __name__ == "__main__":
    raise SystemExit(main())

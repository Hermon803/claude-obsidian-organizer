#!/usr/bin/env python3
"""Search vault notes by keyword. Returns file paths with matching context lines.

Usage:
    python3 search.py <vault_path> <keyword> [--limit N] [--type TYPE]

Output format:
    <relative_path>:<line_number>:<matched_line>
    --- separator between files ---
"""

import sys
import os
import re
import argparse

EXCLUDE_DIRS = {"templates", ".git", "__pycache__", ".organize"}
EXCLUDE_FILES = {"_index.md", "_tags.md", "_graph.md", "_directory-map.md", "CONVENTIONS.md"}


def search(vault_path, keyword, limit=20, note_type=None):
    results = []
    keyword_lower = keyword.lower()

    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        rel_root = os.path.relpath(root, vault_path)

        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            if fname in EXCLUDE_FILES:
                continue

            fpath = os.path.join(root, fname)
            rel_path = os.path.relpath(fpath, vault_path)

            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            except (IOError, UnicodeDecodeError):
                continue

            # Type filter: check frontmatter type field
            if note_type:
                frontmatter = ""
                in_fm = False
                for line in lines:
                    if line.strip() == "---":
                        in_fm = not in_fm
                    elif in_fm:
                        frontmatter += line
                if not re.search(rf"^type:\s*{re.escape(note_type)}\s*$", frontmatter, re.MULTILINE):
                    continue

            matched = False
            for i, line in enumerate(lines, 1):
                if keyword_lower in line.lower():
                    results.append(f"{rel_path}:{i}:{line.rstrip()}")
                    matched = True

            if matched:
                results.append("---")

            if len([r for r in results if r != "---"]) >= limit:
                break

        if len([r for r in results if r != "---"]) >= limit:
            break

    if not results:
        print("No matches found.")
        return

    for line in results:
        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search vault notes")
    parser.add_argument("vault_path", help="Path to the vault")
    parser.add_argument("keyword", help="Keyword to search")
    parser.add_argument("--limit", type=int, default=20, help="Max results")
    parser.add_argument("--type", help="Filter by note type (area/project/resource/idea/journal)")
    args = parser.parse_args()

    if not os.path.isdir(args.vault_path):
        print(f"Error: vault path '{args.vault_path}' not found", file=sys.stderr)
        sys.exit(1)

    search(args.vault_path, args.keyword, args.limit, args.type)

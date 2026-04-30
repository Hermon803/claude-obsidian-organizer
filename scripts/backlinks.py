#!/usr/bin/env python3
"""Find backlinks for a specific note.

Usage:
    python3 backlinks.py <vault_path> <note_title>

Note title is the filename without .md extension.
Output:
    backlinks:
      - path/to/note.md (title)
"""

import sys
import os
import re
import argparse

EXCLUDE_DIRS = {"templates", ".git", "__pycache__", ".organize"}
EXCLUDE_FILES = {"_index.md", "_tags.md", "_graph.md", "_directory-map.md", "CONVENTIONS.md"}


def backlinks(vault_path, note_title):
    results = []
    pattern = re.escape(note_title)

    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            if fname in EXCLUDE_FILES:
                continue

            fpath = os.path.join(root, fname)
            rel_path = os.path.relpath(fpath, vault_path)

            # Skip self
            if fname.replace(".md", "") == note_title:
                continue

            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
            except (IOError, UnicodeDecodeError):
                continue

            if re.search(r"\[\[" + pattern + r"\]\]", content):
                title = fname.replace(".md", "")
                results.append((rel_path, title))

    print(f"backlink_count: {len(results)}")
    print("backlinks:")
    for rel_path, title in sorted(results):
        print(f"  - {rel_path} ({title})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find backlinks for a note")
    parser.add_argument("vault_path", help="Path to the vault")
    parser.add_argument("note_title", help="Note title (filename without .md)")
    args = parser.parse_args()

    if not os.path.isdir(args.vault_path):
        print(f"Error: vault path '{args.vault_path}' not found", file=sys.stderr)
        sys.exit(1)

    backlinks(args.vault_path, args.note_title)

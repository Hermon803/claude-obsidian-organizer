#!/usr/bin/env python3
"""Find orphan notes — notes that have no incoming [[links]] from other notes.

Usage:
    python3 orphans.py <vault_path>

Output:
    orphan_count: N
    orphans:
      - path/to/note.md (title)
      - path/to/note2.md (title2)
"""

import sys
import os
import re
import argparse

EXCLUDE_DIRS = {"templates", ".git", "__pycache__", ".organize"}
EXCLUDE_FILES = {"_index.md", "_tags.md", "_graph.md", "_directory-map.md", "CONVENTIONS.md"}


def orphans(vault_path):
    all_notes = {}  # title -> rel_path
    incoming_links = {}  # title -> count

    # Collect all note titles and their paths
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            if fname in EXCLUDE_FILES:
                continue
            title = fname.replace(".md", "")
            rel_path = os.path.relpath(os.path.join(root, fname), vault_path)
            all_notes[title] = rel_path
            incoming_links[title] = 0

    # Collect all content and count incoming links
    all_content = ""
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            if fname in EXCLUDE_FILES:
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    all_content += f.read() + "\n"
            except (IOError, UnicodeDecodeError):
                continue

    for title in all_notes:
        pattern = re.escape(title)
        mentions = re.findall(r"\[\[" + pattern + r"\]\]", all_content)
        # Don't count self-references
        incoming_links[title] = len(mentions)

    orphan_list = [(title, path) for title, path in all_notes.items()
                   if incoming_links[title] == 0]

    print(f"orphan_count: {len(orphan_list)}")
    print("orphans:")
    for title, path in sorted(orphan_list):
        print(f"  - {path} ({title})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find orphan notes")
    parser.add_argument("vault_path", help="Path to the vault")
    args = parser.parse_args()

    if not os.path.isdir(args.vault_path):
        print(f"Error: vault path '{args.vault_path}' not found", file=sys.stderr)
        sys.exit(1)

    orphans(args.vault_path)

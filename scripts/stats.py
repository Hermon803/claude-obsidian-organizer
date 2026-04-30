#!/usr/bin/env python3
"""Vault statistics: note counts by type, tag frequency, link health.

Usage:
    python3 stats.py <vault_path>

Output format:
    total_notes: N
    types: area=N, project=N, resource=N, idea=N, journal=N
    total_tags: N
    orphan_notes: N
    broken_links: N
    untagged_notes: N
"""

import sys
import os
import re
import argparse

EXCLUDE_DIRS = {"templates", ".git", "__pycache__", ".organize"}
EXCLUDE_FILES = {"_index.md", "_tags.md", "_graph.md", "_directory-map.md", "CONVENTIONS.md"}


def parse_frontmatter(lines):
    """Extract frontmatter fields from markdown lines."""
    fm = {}
    in_fm = False
    content_start = 0

    for i, line in enumerate(lines):
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
            else:
                content_start = i + 1
                break

    if not in_fm:
        return fm, content_start

    for i in range(1, content_start - 1):
        line = lines[i].strip()
        m = re.match(r"^(\w+):\s*(.*)", line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip().strip('"').strip("'")
            fm[key] = val

    return fm, content_start


def count_links(text):
    """Count [[links]] and broken-looking links."""
    wiki_links = re.findall(r"\[\[([^\]]+)\]\]", text)
    return wiki_links


def stats(vault_path):
    type_counts = {}
    tag_set = set()
    all_notes = []
    total_links = 0
    broken_links = 0
    untagged = 0

    all_titles = set()

    # First pass: collect all note titles
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            if fname in EXCLUDE_FILES:
                continue
            title = fname.replace(".md", "")
            all_titles.add(title)

    # Second pass: analyze each note
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            if fname in EXCLUDE_FILES:
                continue

            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")
            except (IOError, UnicodeDecodeError):
                continue

            fm, _ = parse_frontmatter(lines)

            note_type = fm.get("type", "unknown")
            type_counts[note_type] = type_counts.get(note_type, 0) + 1

            tags_str = fm.get("tags", "")
            if tags_str and tags_str != "[]":
                tags = re.findall(r"[\w\-一-鿿]+", tags_str)
                tag_set.update(tags)
            else:
                untagged += 1

            # Count links and detect broken ones
            links = count_links(content)
            total_links += len(links)
            for link in links:
                link_clean = link.split("|")[0].strip()
                if link_clean not in all_titles:
                    broken_links += 1

            rel_path = os.path.relpath(fpath, vault_path)
            all_notes.append((rel_path, fm, content))

    # Orphan detection (notes with no incoming [[links]])
    orphan_count = 0
    all_content = ""
    for _, _, content in all_notes:
        all_content += content + "\n"

    for rel_path, fm, _ in all_notes:
        title_from_file = os.path.splitext(os.path.basename(rel_path))[0]
        # Skip if mentioned in any other note
        pattern = re.escape(title_from_file)
        mentions = re.findall(r"\[\[" + pattern + r"\]\]", all_content)
        # Filter out self-mentions
        other_mentions = [m for m in mentions if m != title_from_file]
        if not other_mentions:
            orphan_count += 1

    print(f"total_notes: {sum(type_counts.values())}")
    print(f"types: {', '.join(f'{k}={v}' for k, v in sorted(type_counts.items()))}")
    print(f"total_tags: {len(tag_set)}")
    print(f"orphan_notes: {orphan_count}")
    print(f"broken_links: {broken_links}")
    print(f"untagged_notes: {untagged}")
    print(f"total_links: {total_links}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vault statistics")
    parser.add_argument("vault_path", help="Path to the vault")
    args = parser.parse_args()

    if not os.path.isdir(args.vault_path):
        print(f"Error: vault path '{args.vault_path}' not found", file=sys.stderr)
        sys.exit(1)

    stats(args.vault_path)

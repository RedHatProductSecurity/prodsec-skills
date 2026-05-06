#!/usr/bin/env python3
"""Validate that skills paths declared in .claude-plugin/marketplace.json exist.

Each entry in the ``skills`` array is a path relative to the marketplace.json
file. This script resolves each path and checks that the directory exists,
catching broken references early (e.g. after a repo restructure).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

MARKETPLACE = Path(".claude-plugin/marketplace.json")


def main() -> None:
    if not MARKETPLACE.is_file():
        print(f"ERROR: {MARKETPLACE} not found", file=sys.stderr)
        sys.exit(1)

    data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    errors: list[str] = []

    for plugin in data.get("plugins", []):
        name = plugin.get("name", "<unnamed>")
        for skills_path in plugin.get("skills", []):
            resolved = (MARKETPLACE.parent / skills_path).resolve()
            if not resolved.is_dir():
                errors.append(
                    f"plugin '{name}': skills path '{skills_path}' resolves to "
                    f"'{resolved}' which does not exist"
                )

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print(f"\n{len(errors)} error(s) in marketplace path checks.", file=sys.stderr)
        sys.exit(1)

    total = sum(len(p.get("skills", [])) for p in data.get("plugins", []))
    print(f"All {total} skills path(s) in {MARKETPLACE} resolve correctly.")


if __name__ == "__main__":
    main()

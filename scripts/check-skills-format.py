#!/usr/bin/env python3
"""Validate YAML front matter for AgentSkills layout under module/skills/.

Each skill lives at ``module/skills/<skill_id>/SKILL.md`` (ADR-0002). Checks:

  - YAML front matter present (--- delimiters)
  - Required field: name (non-empty), matching ``skill_id`` for SKILL.md
  - Required field: description (non-empty)
  - Required fields on SKILL.md only: category, subcategory (non-empty scalars)
  - Supporting ``reference/*.md`` (and other nested .md): name matches stem,
    description non-empty; category/subcategory not required
"""

from __future__ import annotations

import sys
from pathlib import Path

MODULE_SKILLS = Path("module/skills")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Return scalar front matter fields, or None if absent/malformed.

    Handles plain scalars and YAML block scalars (> and |). Strips surrounding
    quotes from scalar values.
    """
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    lines = text[4:end].splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            key, _, raw = line.partition(":")
            value = raw.strip()
            if value in (">", "|", ">-", "|-"):
                parts: list[str] = []
                i += 1
                while i < len(lines) and lines[i].startswith(" "):
                    parts.append(lines[i].strip())
                    i += 1
                fields[key.strip()] = " ".join(parts)
                continue
            v = value.strip('"').strip("'")
            fields[key.strip()] = v
        i += 1
    return fields


def check(path: Path, *, skill_id: str, is_primary_skill: bool) -> list[str]:
    """Return a list of error strings for the given skill markdown file."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    if fm is None:
        return [f"{path}: missing or malformed YAML front matter"]

    name_val = fm.get("name", "")
    desc_val = fm.get("description", "")

    expected_stem = skill_id if is_primary_skill else path.stem

    if "name" not in fm or not name_val:
        errors.append(f"{path}: missing or empty required field 'name'")
    elif name_val != expected_stem:
        errors.append(
            f"{path}: name mismatch — front matter 'name: {name_val}'"
            f" but expected '{expected_stem}'"
        )

    if "description" not in fm or not desc_val:
        errors.append(f"{path}: missing or empty required field 'description'")

    if is_primary_skill:
        cat = fm.get("category", "").strip()
        sub = fm.get("subcategory", "").strip()
        if "category" not in fm or not cat:
            errors.append(f"{path}: missing or empty required field 'category'")
        if "subcategory" not in fm:
            errors.append(f"{path}: missing required field 'subcategory'")
        elif not sub:
            errors.append(f"{path}: subcategory must be non-empty")

    return errors


def collect_paths() -> list[tuple[Path, str, bool]]:
    """Return (path, skill_id, is_primary_skill) for every skill markdown file."""
    if not MODULE_SKILLS.is_dir():
        return []

    out: list[tuple[Path, str, bool]] = []
    for skill_dir in sorted(MODULE_SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_id = skill_dir.name
        primary = skill_dir / "SKILL.md"
        if not primary.is_file():
            out.append((primary, skill_id, True))  # produces missing-file errors
            continue
        out.append((primary, skill_id, True))
        for p in sorted(skill_dir.rglob("*.md")):
            if p == primary:
                continue
            out.append((p, skill_id, False))
    return out


def main() -> None:
    paths = collect_paths()
    if not paths:
        print(f"No skill files found under {MODULE_SKILLS}", file=sys.stderr)
        sys.exit(1)

    all_errors: list[str] = []
    for path, skill_id, is_primary in paths:
        if not path.is_file():
            all_errors.append(f"{path}: missing SKILL.md for skill '{skill_id}'")
            continue
        all_errors.extend(check(path, skill_id=skill_id, is_primary_skill=is_primary))

    if all_errors:
        for e in all_errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print(f"\n{len(all_errors)} error(s) in skill format checks.", file=sys.stderr)
        sys.exit(1)

    n_packages = sum(1 for _, _, is_primary in paths if is_primary)
    print(f"All {len(paths)} skill markdown files pass format checks ({n_packages} skill packages).")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate YAML front matter for skills under module/skills/ and ge-core/.

Each module skill lives at ``module/skills/<skill_id>/SKILL.md`` (ADR-0002).
Checks:

  - YAML front matter present (--- delimiters)
  - Required field: name (non-empty), matching ``skill_id`` for SKILL.md
  - Required field: description (non-empty)
  - Required fields on SKILL.md only: category, subcategory (non-empty scalars)
  - Supporting ``reference/*.md`` (and other nested .md): name matches stem,
    description non-empty; category/subcategory not required

GE Core skills at ``ge-core/<skill_id>/SKILL.md`` follow the agentskills.io
spec instead: only spec-defined top-level fields are allowed, and category /
subcategory live under ``metadata:`` (checked as ``metadata.category`` /
``metadata.subcategory``).
"""

from __future__ import annotations

import sys
from pathlib import Path

MODULE_SKILLS = Path("module/skills")
GE_CORE = Path("ge-core")

# Top-level frontmatter fields defined by the agentskills.io specification.
AGENTSKILLS_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Return scalar front matter fields, or None if absent/malformed.

    Handles plain scalars, YAML block scalars (> and |), and one level of
    nested mappings (flattened as ``parent.child``). Strips surrounding
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
            if not value:
                # Nested mapping: collect indented ``child: value`` lines.
                parent = key.strip()
                fields[parent] = ""
                i += 1
                while i < len(lines) and lines[i].startswith(" "):
                    sub = lines[i].strip()
                    if ":" in sub:
                        sub_key, _, sub_raw = sub.partition(":")
                        sub_val = sub_raw.strip().strip('"').strip("'")
                        fields[f"{parent}.{sub_key.strip()}"] = sub_val
                    i += 1
                continue
            v = value.strip('"').strip("'")
            fields[key.strip()] = v
        i += 1
    return fields


def check(
    path: Path, *, skill_id: str, is_primary_skill: bool, layout: str
) -> list[str]:
    """Return a list of error strings for the given skill markdown file.

    ``layout`` is ``"module"`` (ADR-0002: top-level category/subcategory) or
    ``"ge-core"`` (agentskills.io spec: category/subcategory under metadata).
    """
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

    if is_primary_skill and layout == "module":
        cat = fm.get("category", "").strip()
        sub = fm.get("subcategory", "").strip()
        if "category" not in fm or not cat:
            errors.append(f"{path}: missing or empty required field 'category'")
        if "subcategory" not in fm:
            errors.append(f"{path}: missing required field 'subcategory'")
        elif not sub:
            errors.append(f"{path}: subcategory must be non-empty")

    if is_primary_skill and layout == "ge-core":
        top_level = {k for k in fm if "." not in k}
        extra = top_level - AGENTSKILLS_FIELDS
        if extra:
            errors.append(
                f"{path}: non-standard top-level field(s) {sorted(extra)} — "
                "move them under 'metadata:' (agentskills.io spec)"
            )
        for field in ("metadata.category", "metadata.subcategory"):
            if not fm.get(field, "").strip():
                errors.append(f"{path}: missing or empty required field '{field}'")

    return errors


def collect_paths(root: Path, layout: str) -> list[tuple[Path, str, bool, str]]:
    """Return (path, skill_id, is_primary_skill, layout) for every skill file."""
    if not root.is_dir():
        return []

    out: list[tuple[Path, str, bool, str]] = []
    for skill_dir in sorted(root.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        skill_id = skill_dir.name
        primary = skill_dir / "SKILL.md"
        if not primary.is_file():
            out.append((primary, skill_id, True, layout))  # missing-file errors
            continue
        out.append((primary, skill_id, True, layout))
        for p in sorted(skill_dir.rglob("*.md")):
            if p == primary:
                continue
            out.append((p, skill_id, False, layout))
    return out


def main() -> None:
    paths = collect_paths(MODULE_SKILLS, "module") + collect_paths(GE_CORE, "ge-core")
    if not paths:
        print(
            f"No skill files found under {MODULE_SKILLS} or {GE_CORE}",
            file=sys.stderr,
        )
        sys.exit(1)

    all_errors: list[str] = []
    for path, skill_id, is_primary, layout in paths:
        if not path.is_file():
            all_errors.append(f"{path}: missing SKILL.md for skill '{skill_id}'")
            continue
        all_errors.extend(
            check(path, skill_id=skill_id, is_primary_skill=is_primary, layout=layout)
        )

    if all_errors:
        for e in all_errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print(f"\n{len(all_errors)} error(s) in skill format checks.", file=sys.stderr)
        sys.exit(1)

    n_packages = sum(1 for _, _, is_primary, _ in paths if is_primary)
    print(
        f"All {len(paths)} skill markdown files pass format checks"
        f" ({n_packages} skill packages)."
    )


if __name__ == "__main__":
    main()

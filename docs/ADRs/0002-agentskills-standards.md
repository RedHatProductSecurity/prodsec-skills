---
title: "2. Adopt AgentSkills.io Standards and AI Context Module Structure"
status: Accepted
relates_to:
  - "*"
topics:
  - agentskills
  - lola
  - module-structure
  - distribution
---

# 2. Adopt AgentSkills.io Standards and AI Context Module Structure

Date: 2026-04-15

## Status

Accepted

## Context

`prodsec-skills` is a security skills library providing 128 security guidance
files that AI assistants consume to apply security expertise during development.
As adoption expands across teams, aligning the repository structure with
established AI skill standards enables skills to be versioned, packaged, and
distributed through standard AI tooling rather than per-project integration.

**AgentSkills.io: the portable skill standard**

The [AgentSkills.io specification](https://agentskills.io/specification)
defines a portable, tool-agnostic format for AI skill files: a markdown file
(`SKILL.md`) with `name` and `description` YAML frontmatter, plus optional
supporting directories (`scripts/`, `reference/`, `assets/`). All curated
prodsec-skills already conform to this format. The existing
`check-skills-format.py` validator enforces both required fields. Explicitly
adopting this standard makes the repo's intent clear and ensures skills remain
consumable by any compliant AI tooling.

**AI Context Modules: a packaging layer for skill collections**

The [AI Context Module format](https://lobstertrap.org/lola/concepts/skills-and-modules/#ai-context-module)
builds on the AgentSkills.io standard to package multiple skills into a single
distributable unit. The key structural element is a `module/` directory that
establishes a clear package boundary — separating AI-facing content from
project tooling such as CI scripts, validation utilities, and architectural
documents:

```
prodsec-skills/
  module/                   # Package boundary — AI-facing content
    AGENTS.md               # AI Main Spec: module-level context for assistants
    skills/
      skill-a/
        SKILL.md
      skill-b/
        SKILL.md
    mcps.json               # MCP server configuration (reserved for future use)
  scripts/                  # Project tooling — outside the package boundary
  docs/
  .github/
```

The `module/AGENTS.md` — the AI Main Spec — provides module-level context
that applies across all skills. It is the unified guidance document AI
assistants receive after installation, describing what the module contains and
how to use it. This is distinct from the repo root `AGENTS.md`, which
documents the contributor workflow.

Adopting the AI Context Module standard makes the repository a first-class
participant in the AI skills ecosystem. As a result, the module becomes
distributable via AI package managers such as [Lola](https://github.com/LobsterTrap/lola)
to any supported AI assistant (Claude Code, Cursor, Gemini CLI, OpenCode):

```bash
lola mod add https://github.com/RedHatProductSecurity/prodsec-skills.git
lola install prodsec-skills --assistant claude-code
```

**Structural alignment**

The AI Context Module standard expects skills in a flat layout — one directory
per skill, each containing a `SKILL.md`:

```
module/skills/
  cargo-fuzz/
    SKILL.md
  hardening-remote/
    SKILL.md
```

The current prodsec-skills structure places skills two levels deep inside
category subdirectories (`skills/<category>/<subcategory>/<name>.md`).
Migrating to the standard layout is a one-time restructuring. After migration,
contributors add new skills at `module/skills/<name>/SKILL.md` directly — no
intermediate build step required.

**Name disambiguation**

The current hierarchical layout allows the same file stem to exist in different
subcategories. Seven pairs of skills share identical stems while covering the
same topic for different components. A naming rule is needed to ensure
uniqueness in the flat layout:

```
# Before — same stem in two subcategories
skills/secure_development/external-data-source/logging.md
skills/secure_development/model-registry/logging.md

# After — subcategory prefix disambiguates
module/skills/logging/SKILL.md                   # external-data-source
module/skills/model-registry-logging/SKILL.md    # model-registry
```

The convention `<subcategory>-<name>` is applied to the more specific
occurrence, with the `name` frontmatter field updated to match.

## Decision

Restructure `prodsec-skills` to adopt the AI Context Module format:

1. **Create `module/` as the package root.** All AI-facing content moves
   inside `module/`. Project tooling (scripts, CI, docs, ADRs) remains at the
   repository root, outside the package boundary.

2. **Migrate skills to `module/skills/<name>/SKILL.md`.** Move all curated skill
   files from `skills/<category>/<subcategory>/<name>.md` to the flat layout
   `module/skills/<name>/SKILL.md`. Category and subcategory metadata moves
   from directory paths to frontmatter fields (`category:`, `subcategory:`).
   The `skills/` directory at the repository root is removed.

3. **Add `module/AGENTS.md` — the AI Main Spec.** This document describes the
   module's purpose, the full skill inventory with trigger conditions, and how
   AI assistants should use the skills. It is the primary context document
   installed into AI tooling.

4. **Resolve the 7 name collision pairs.** Apply the `<subcategory>-<name>`
   convention to the more specific skill in each pair. Both the directory name
   and the `name` frontmatter field are updated to match.

5. **Add `module/mcps.json`.** An empty MCP configuration
   (`{"mcpServers": {}}`) reserves the position for future MCP server
   definitions without requiring structural changes later.

6. **Update tooling and indexes.** Update `check-skills-format.py` to scan
   `module/skills/` and validate `category:` and `subcategory:` frontmatter
   fields. Update `AGENTS.md`, `README.md`, and all skill index files to
   reflect the new paths.

## Consequences

- Skills become installable to any lola-supported AI assistant with a single
  command, enabling repeatable, versioned distribution across teams.
- The `module/` boundary cleanly separates AI package content from project
  tooling, making the repository's dual purpose — skills library and
  contributor workspace — explicit in its structure.
- `module/AGENTS.md` provides unified module-level context across all curated
  skills, giving AI assistants a single entry point rather than many isolated
  files.
- The `module/` structure is extensible: slash commands, sub-agents, and MCP
  servers can be added inside `module/` without further structural changes.
- Formally adopts AgentSkills.io as the normative skill format, making
  compliance explicit and tooling-enforced.
- One-time migration required: all skill files moved and renamed, all index files
  updated, validation scripts updated.
- Existing path-based skill references (e.g.,
  `skills/secure_development/mcp-server/hardening-remote.md`) break and must
  be updated in any documentation or tooling that uses them.
- Category and subcategory organization moves from directory structure to
  frontmatter; browsing skills by category in a file explorer requires
  filtering by frontmatter rather than navigating directories.
- Seven collision pairs receive new names during migration; these names diverge
  from the current `name` frontmatter values in those files.

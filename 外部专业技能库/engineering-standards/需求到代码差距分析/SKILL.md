---
name: prd-implementation-planner
description: Compares a product requirements document (PRD), spec or feature brief with the code, and reports a verdict per requirement (implemented, deviating, partial, missing or unverifiable) plus a build plan for the gaps. Reports only. Use when given a PRD with code or paths, or asked what is left to build.
license: MIT
metadata:
  pack: core
---

# PRD → Implementation Gap Analysis & Planning

Turns a PRD into a requirement-by-requirement verdict against the real codebase: **already correct**, **implemented but broken/deviating**, or **not built yet** — with a concrete plan for closing every gap. Never produce a generic summary of the PRD; the output must be traceable, one line of the PRD at a time, back to actual code.

## When this triggers

The user will typically paste a PRD (or reference one already in the conversation), then follow up with a list of reference file paths.

Treat a PRD + a labeled file list as a complete request even without an explicit "make me a plan" instruction — the file list IS the instruction to run the gap analysis against those files.

If the PRD was pasted in an earlier turn of this conversation, reuse it — don't ask the user to repaste it.

Distinguish two different "missing file" situations, because they have opposite handling:

- **Not provided** — a requirement needs a file the user never supplied (an entity, a DTO, a module, a shared pipe). Ask for it before verifying anything mapped to it; don't guess at file contents.
- **Provided but not found on disk** — the user gave a path and nothing is there. Do not conclude "not implemented" from a path alone; a typo would then produce a page of false verdicts. Search for the filename first (glob the repo for the basename, check sibling directories and a plausible feature folder). If it genuinely doesn't exist anywhere, report those requirements as **unverifiable — file not found**, not as ❌.

## Workflow

Before starting, size the work. If the PRD decomposes into more atomic requirements than can be audited in one pass, or the reference file list is too large to read completely, **say so up front and process it in named sections** (PRD section by PRD section), finishing each fully before moving on. Never silently sample the PRD or skim files to make the scope fit — a partial audit presented as complete is worse than an explicitly partial one.

### Step 1 — Decompose the PRD into atomic requirements

Read the PRD and break it into a flat, numbered checklist of individually verifiable requirements. Each item should be small enough to be unambiguously "done" or "not done" against code — not a whole section. Split by:

- Each field (name, type, required/optional, validation rule) in any spec table
- Each UI element or column
- Each conditional/business rule ("Archived projects excluded from the task form's project picker")
- Each state transition or lifecycle rule
- Each validation message / error string specified verbatim
- Each calculation/formula
- Each logging/audit requirement

Group the checklist under the PRD's own section headings so the final report stays navigable, but keep each requirement atomic underneath.

Do not skip "obvious" or small-sounding requirements (e.g. a single default value, a single tooltip string, a single sort order) — these are exactly what tends to be missed in real implementations and are cheap to check.

### Step 2 — Map requirements to reference files

For each requirement, identify which of the provided reference files is the right place to verify it (e.g. UI/column/badge requirements → frontend component; validation and calculation logic → backend service; route/status-code/versioning requirements → backend controller). Some requirements span multiple files (e.g. a filter that's rendered in the frontend but populated by a backend endpoint) — note all relevant files for those.

If a requirement clearly needs a file that wasn't provided, say so explicitly in the output rather than silently skipping the check — the user can supply it.

### Step 3 — Read every reference file in full

Read each referenced file completely before making any verdict — do not sample or infer from filenames/symbols alone.

If a file isn't at the given path, follow the "provided but not found on disk" handling above: search for it, and only if it genuinely doesn't exist report the requirements mapped to it as **unverifiable — file not found**. Absence of a file is never by itself evidence that a requirement is unimplemented; the code may live somewhere you weren't pointed at.

### Step 4 — Classify each requirement

For every atomic requirement, assign exactly one status:

- **✅ Implemented — matches PRD**: code satisfies the requirement as written, including edge cases and exact wording where the PRD specifies exact strings (toast messages, inline errors, tooltips).
- **⚠️ Implemented — deviates / has issues**: something exists that addresses the requirement, but differs from the PRD (wrong condition, missing edge case, wrong copy, wrong status code, wrong casing convention, off-by-one on a date rule, etc.). Describe the deviation precisely: what the code does vs. what the PRD says.
- **❌ Not Implemented**: no code addresses the requirement at all.
- **❓ Partially Implemented**: some but not all of a multi-part requirement exists (e.g. the field exists but validation doesn't; the column renders but the "-" fallback for empty values is missing). Break down exactly which part is missing.
- **🔍 Unverifiable**: the requirement's compliance cannot be determined from what was provided — the owning file wasn't supplied or wasn't found, or it depends on runtime/config state not visible in code. Say what would be needed to settle it.

Be skeptical of surface-level matches. A method or field with the right name is not automatically compliant — check the actual logic against the PRD's stated rule.

**Additionally, flag PRD defects with 🚩 alongside whatever status the requirement got.** The PRD is not automatically correct, and a plan built off a broken requirement inherits the break. Flag it when a requirement is:

- **Ambiguous** — two reasonable implementations satisfy the wording.
- **Self-contradictory** — it conflicts with another requirement in the same PRD (cite both).
- **In conflict with an established convention** — e.g. it specifies `snake_case` query parameters, an error shape other than the project's envelope, or a status code that contradicts the project's standard. Name the convention it collides with and let the user decide which wins; do not silently plan to either follow the PRD or override it.
- **Technically infeasible or unsafe as written** — e.g. it requires a value the system doesn't have at that point in the flow.

A 🚩 is a question for the user, not a verdict. Never resolve it silently.

### Step 5 — For implemented-but-deviating or partial items: describe the fix

For every ⚠️ and ❓ item, write a concrete, actionable fix description: what to change, in which file, and (if relevant) roughly where. This is a diagnosis, not a full patch — point at the exact logic/condition/string to correct.

### Step 6 — For not-implemented items: build the plan

For every ❌ item, and for missing pieces of ❓ items, produce an implementation plan entry with:
- **What to build** (in plain terms tied to the PRD's own language)
- **Where** (which file, or "new file" with a suggested path/pattern matching sibling files if evident from the reference files)
- **Dependencies** — note if it depends on another ❌ item being built first (e.g. the Status filter depends on the Status column/field existing)
- **Applicable standards.** Take naming, shape, and convention decisions from the project's existing code and from whichever standards skills are installed, rather than inventing a pattern or copying one out of the PRD's prose:
  - the framework pack's guidelines skill: route paths, versioning, parameter casing, file naming, feature folders, where logic belongs, and the project's framework version and architecture;
  - its API-contract skill: DTO shape, wire casing, pagination envelope, status codes, error envelope;
  - its forms, persistence, security, and accessibility skills: select vs autocomplete, constraints and migrations, authorization and tenant scoping on every new endpoint, WCAG 2.2 AA for new UI;
  - from core, `code-structure`, `code-hygiene`, and `commenting-standards`.

  When a rule drove a decision, cite it by skill name, section number, and rule title. Note every place where the PRD and a standard disagree (that's a 🚩).

Group related ❌ items that will likely be implemented together (e.g. all fields of one form section) into a single plan step so the plan reads as a sane build order, not 40 disconnected bullets — but keep the underlying atomic checklist traceable underneath each group.

### Step 7 — Produce the final report

Structure the output as:

1. **Audited against** — identify exactly what was compared: the PRD's title plus its version/date if it carries one (otherwise say it is undated, and where it came from — pasted in this conversation, or a file path), the reference files actually read, and the commit/branch if the repo state is known. A gap analysis without this anchor can't be re-checked later when the PRD moves.
2. **Summary** — counts by status (✅ / ⚠️ / ❓ / ❌ / 🔍) and a one-line overall verdict per major PRD section.
3. **Section-by-section detail** — following the PRD's own headings, list every atomic requirement with its status icon, a one-line verdict, and (for ⚠️/❓/❌) the fix or plan description from Steps 5–6.
4. **PRD issues needing a decision (🚩)** — every flag from Step 4, each with the two or more readings or the convention it collides with, and what you need from the user to proceed. Put this before the build order: these answers can change the plan.
5. **Suggested build/fix order** — a short ordered list sequencing the ❌ and ⚠️ items by dependency, not by PRD document order.
6. **Files referenced but not found / not provided** — call out anything Step 2/3 couldn't verify, with a note on what's needed to complete the audit, and whether the file was never supplied or was supplied-but-absent.

Keep verdicts factual and specific — cite the actual code condition or line's behavior, not a paraphrase of the PRD back at the user. If a requirement's compliance depends on something not visible in the provided files, mark it 🔍 rather than assuming compliance.

## Related Standards

| Concern | Skill | What it adds |
|---|---|---|
| Executing an approved plan with a tracked checklist | `plan-tracker-flow` | The plan-and-tracker workflow for building the ❌ items |
| Placing new shared logic | `code-structure` | Orchestration vs shared-mechanics layering for new code |
| Completeness once the code is written | `code-hygiene` | Acceptance-criteria traceability and residue checks before commit |

## Notes

- This skill produces a plan/report, not code changes — do not modify the referenced files. If the user then asks to implement a specific plan item, that's a separate follow-up task.
- The audit is only as current as the PRD it ran against. If the PRD changes after a report is produced, the report needs re-running, not patching.

---
name: plan-tracker-flow
description: A two-file workflow for multi-session work, with an approved plan document and a tracker updated after each chunk of work. Use when asked for a plan and tracker or a phased implementation plan, or for any feature, migration or refactor large enough to span sessions or drift from what was agreed.
license: MIT
metadata:
  pack: core
---

# Plan and Tracker Flow

Complex work is built from an approved plan and a live tracker, not from memory. Cite a step as "plan-tracker-flow §N, <step title>".

## 1. The Two Files

| File | Purpose | Who changes it, and when |
|---|---|---|
| `<feature>-plan.md` | Scope, locked decisions, phases, verification plan | Written once and approved by the user. Changed only by an agreed pivot, which is recorded in the tracker log. |
| `<feature>-tracker.md` | Status of every item, with notes, blockers, and a dated log | Updated after every logical chunk of work |

Place both where the project keeps planning documents (`docs/`, `tasks/`, or a folder the user names). If the plan holds internal detail that must not be published, put it in a location that version control ignores, and say so.

## 2. Write the Plan

The plan contains:

1. **Status and meta:** the feature name, status (Draft / Approved / Done), date, and a link to the tracker.
2. **Starting point:** what exists today, measured from the code rather than assumed.
3. **Target:** what will exist when the work is done.
4. **Locked decisions:** a numbered table of decision, rationale, and status, holding the choices that must not be re-argued mid-implementation. Mark any decision that needs the user's confirmation, and get it before work starts.
5. **Phases:** ordered, each with concrete items and an **exit criterion** that can be checked.
6. **Verification plan:** the automated checks (commands, tests, linters) and the manual checks that prove the feature is complete.
7. **Risks and out of scope:** what could go wrong and how it is mitigated; what is deliberately excluded.

## 3. Write the Tracker

The tracker contains:

1. **A link to the plan.**
2. **An overview table:** one row per phase, with status and exit-criteria state.
3. **Progress tables per phase:** columns `Item`, `Status`, `Notes`. Status is one of **Not Started**, **In Progress**, **Blocked**, **Done**.
4. **Blockers:** what is blocked, since when, and on what.
5. **Log:** dated entries for decisions, deviations, pivots, and surprises found during execution.

## 4. Get Approval Before Building

- Present the plan and the open decisions, and ask the user to approve them. Write no implementation code before approval.
- A request that already says "go ahead" counts as approval for the plan as written. Decisions marked as needing confirmation still need an answer.

## 5. Execute and Keep the Tracker True

- After each logical chunk of work, update the item's `Status` and `Notes` in the tracker.
- Mark an item **Done** only after it has been verified (tests run, checks passed, behaviour confirmed). An unverified item stays **In Progress**, with a note on what is left to check.
- Something that blocks progress becomes a **Blocked** row plus a blockers entry. Never leave it implied.
- Record every deviation from the plan in the log, with the reason.
- Change the plan only for a pivot the user has agreed to. Log the pivot in the tracker and note it at the top of the plan.

## 6. Resume From the Files, Not From Memory

- At the start of any new session on the feature, read the plan and the tracker before touching code. The tracker is the source of truth for what is done.
- If the code and the tracker disagree, check the code, correct the tracker, and log the correction.

## 7. Related Standards

| Concern | Skill | What it adds |
|---|---|---|
| Building the plan from a PRD or spec | `prd-implementation-planner` | A per-requirement gap analysis that feeds the plan's phases |
| Checking each completed item | `code-hygiene` | Acceptance-criteria traceability and residue checks before an item is marked Done |
| Describing each completed chunk | `commit-message` | A commit message per chunk of tracked work |

## 8. Output Structure

When creating the files, reply with:

1. The paths of the plan and the tracker.
2. A short summary of the target and the phases.
3. The decisions that need the user's confirmation, each with a recommended answer.
4. A request to approve the plan before implementation starts.

During execution, end each update with the tracker rows that changed.

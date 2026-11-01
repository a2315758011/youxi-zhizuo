---
name: refactor-checker
description: Investigates whether a file, function, class, component, provider or dependency you point to is dead or redundant, tracing references outward and grading confidence. Reports only and never edits or deletes. Use when asked whether code is unused, safe to delete or duplicated.
license: MIT
metadata:
  pack: core
---

# Refactor Audit: targeted dead-code and redundancy investigation

This skill answers one question at a time: **is this specific thing the person pointed to — dead, or redundant with something else?** It is not a repository-wide scanner, and it does not run a fixed sequence of tools. It starts from whatever the person referenced, works out what that thing actually is and where it sits, and traces outward through real references — expanding scope only when the evidence in hand isn't enough to answer confidently.

```
Referenced target → understand its context → inventory what's inside it →
trace references outward (expanding only as needed) → framework-aware pass →
check for redundancy nearby → report with confidence
```

**The analysis never edits, deletes, or merges code.** Every finding goes into a report for a human to act on. This isn't just caution about irreversible mistakes — it reflects a real epistemic limit: every method available here (`grep`, AST tools, compilers, linters) is a pattern-matcher over text or syntax, not a full model of runtime behavior. None of them can see string-built dynamic references, config-driven wiring, or a consumer in a part of the codebase nobody thought to check. Treat every finding as "here's the evidence, here's what it doesn't rule out" — not as proof.

## Step 1: Establish the target and its context

The person's reference is the anchor — a file path, a directory, a named function/class/component, or a symbol inside a file they showed you. Start there, not at the repo root.

1. **Resolve what the target actually is.** A single file → inventory its top-level declarations (Step 2). A directory → inventory the files in it and treat each as a candidate, or focus on whichever specific thing the person asked about if they named one. A named symbol inside a larger file → scope to that symbol, but still read the whole file for context (a symbol's neighbors often explain its purpose).
2. **Find the project the target belongs to.** Walk upward from the target to the nearest ancestor directory with a project manifest: `package.json` for JavaScript/TypeScript, or `pyproject.toml`, `setup.cfg`, `setup.py`, or `requirements*.txt` for Python. That directory is the project root. Note whether it sits inside a larger monorepo, which matters later for how far you're willing to expand (Step 3) and whether the target might be a shared export consumed elsewhere. Monorepo signs:
   - `nx.json`, `turbo.json`, or `pnpm-workspace.yaml`;
   - a root `package.json` with a `"workspaces"` array;
   - a `[tool.uv.workspace]` table;
   - several Python packages under one root;
   - sibling `apps/`, `packages/`, or `libs/` directories.
3. **Detect framework signals in that project**, without assuming any one framework. Check the manifest's dependencies and marker files:
   - `angular.json` / `@angular/core`
   - `nest-cli.json` / `@nestjs/core`
   - `react` / `react-dom`
   - `next`
   - `fastapi`
   - or others.

   If you find one of these, read `references/frameworks.md` for that framework's reference surfaces before continuing. Decorators, DI, templates, file-based routing, and registration calls all create real usage that a plain import search can't see, and guessing at them from general knowledge risks missing framework-specific wiring. Read its "Python" section for any Python project. If the project uses something not covered there, apply the general principle at the top of that file: find the project's own registration or wiring mechanism (a plugin manifest, a routing table, a DI container, a decorator-driven registry) and treat it as an additional reference surface beyond plain imports.
4. **State your assumed scope up front, briefly**, especially if the target is a large directory or the request is ambiguously broad ("check this file" is clear; "look at src/" in a large project is worth a one-line assumption before diving in) — so the person can redirect you before you spend a lot of effort in the wrong place. Don't silently balloon a single-file question into a directory sweep, or a directory sweep into a full-project audit.

## Step 2: Inventory what's inside the target

List the concrete things worth checking — don't just eyeball the file and guess. For a TypeScript/JavaScript file this means every top-level `export` (function, class, const, type), every declared component/provider/controller if a framework is in play, and every import at the top of the file (candidates for "unused import," the cheapest and most reliable category). For a Python module, it means every top-level `def`, `class`, and module-level assignment, the names in `__all__`, every route or dependency function a framework registers, and every import. For a directory, do this per file, prioritizing files the person seems to actually care about over exhaustively touching everything if the directory is large — if you have to sample rather than cover everything, say so.

## Step 3: Trace references outward — expand only as needed

This is the core of the investigation. For each candidate (an export, a component, a provider, an import), work outward in stages, stopping as soon as you have enough evidence to make a confident call — most candidates resolve at stage 1 or 2, and only genuinely ambiguous ones need to go further:

1. **Same file.** Is it used elsewhere in this file? (Covers plenty on its own — a private helper only used once nearby, a locally-shadowed import.)
2. **Same directory / immediate module.** Grep for the symbol's name across the files right around the target — the files that would naturally import from it (siblings, a parent feature module, an adjacent test file for context though not as proof of production use).
3. **The whole project** (per Step 1's project boundary). Grep project-wide, and reach for a sharper tool if the codebase is large enough that plain grep is noisy — see Step 4 for what's actually available and when each is worth the overhead.
4. **Sibling projects, only if the target is plausibly a shared export.** If the project you're in looks like a shared library (a `libs/`/`packages/`-style project, or the symbol is re-exported through a public `index.ts`/barrel), a project-only search will make a genuinely-used symbol look dead just because its consumers live in a different project. Check sibling projects in this case — but only this case; don't habitually search the whole monorepo for every candidate.
5. **Full repo-wide sweep — only on explicit request.** If none of the above resolved it and the person hasn't asked for a repo-wide audit, stop here and report it as "needs review — not found within \[scope actually checked\]," rather than either declaring it dead or silently expanding further. Say plainly what you did and didn't check.

At every stage, absence of a match is evidence, not proof. A clean grep across everything you checked supports a finding; it doesn't establish one on its own, because of exactly the blind spots named in the framework file and in "What NOT to flag" below (dynamic strings, config-driven wiring, a consumer outside what you searched). Say what you checked and let that scope stand behind the confidence level in the report — don't claim more certainty than the search actually earned.

## Step 4: Tools are optional evidence, not a pipeline

None of the tools below are mandatory, and there's no fixed order. Reach for whichever will actually move the needle on the specific candidate in front of you, and skip the rest — running every tool on every candidate wastes time and produces noise that obscures the real findings. A few notes earned through hard experience testing this skill, so you don't have to rediscover them mid-investigation:

- **`grep`/text search** — cheapest, always available, and usually sufficient. Start here for almost everything.
- **The TypeScript compiler (`tsc --noEmit --noUnusedLocals --noUnusedParameters`)** — precise for unused locals/imports *within a file's own scope* (error codes `TS6133`/`TS6192` specifically — every other diagnostic it prints is a type error unrelated to this audit and should be ignored, not reported as a finding). Filter the output before reading it: keep only the `TS6133`/`TS6192` lines for the target's files (pipe through `grep -E 'TS6133|TS6192'` and the target's path, or the shell's equivalent). On a real project the unfiltered output can run to thousands of lines. It does not tell you whether an *exported* symbol is used elsewhere; that needs a project-wide search. If you run it: pass `--tsBuildInfoFile <path outside the repo>` if the project's `tsconfig.json` has `"incremental"` or `"composite": true` — otherwise `tsc` can still write a `.tsbuildinfo` file into the repo's `outDir` despite `--noEmit` (confirmed while building this skill). Never write tool output or build artifacts inside the repo you're auditing.
- **ESLint, if the project already has it configured** — don't invent a config just for this. Run it on the target's files, not the whole project. A totally clean result can genuinely mean clean code, or it can mean the config's file-matching didn't cover the files you care about (a real, reproducible gap with flat-config setups that lack an explicit `files: ["**/*.ts"]` pattern). If a clean result looks surprising, cross-check with `--format json` on those same files and confirm the files you expected actually appear in the output before trusting the "no findings."
- **`ts-prune`** (via `npx ts-prune`, no install needed) — a candidate list for unused exports project-wide, not a reliable final answer on its own; it has a known blind spot around barrel/`index.ts` re-export chains. Its output covers every export in the project, so filter it to the target's path before reading it. Corroborate any hit with your own grep before reporting it.
- **`depcheck`** (via `npx depcheck`) — only relevant if the question is about an unused *package dependency*, not source code. False-positives on type-only imports, peer deps, and framework packages required implicitly at bootstrap.
- **`jscpd`** (via `npx jscpd`) — useful for redundancy checks (Step 5), scoped to the target's neighborhood, not the whole repo, unless asked. Its CLI flag names and supported format labels have changed across versions in practice — run `npx jscpd --list` first to see what this installed version actually supports rather than assuming `--format typescript` or `--languages typescript` is right, and don't hardcode either.
- **Python: `ruff check --select F401,F811,F841`** for unused imports, redefinitions, and unused local variables within a file. Like `tsc`, it says nothing about whether a module-level name is used by *other* modules.
- **Python: `vulture`** (`pipx run vulture <path>` or `uvx vulture <path>`) — a confidence-scored list of unused functions, classes, and variables across the paths you give it. Treat its output as candidates: it cannot see names used only through framework registration, pytest fixtures, or `getattr`, so corroborate every hit with your own search and the framework file before reporting it. Scope it to the target's directory or project, not the whole monorepo.
- **Python: `deptry`** — only for the question of an unused or missing *package dependency*. It has the same caveats as `depcheck`: implicit plugins and optional extras show up as false positives.
- **AST-aware search** (the TypeScript compiler API, Python's `ast` module, or reading the file directly) when grep's text matching is producing too many false hits — e.g. a common word being mistaken for a symbol reference.
- **Any tool invocation can fail** — a package that can't be resolved (network/registry issue), a rejected CLI flag, a crash — and this can look like "the tool ran and found nothing." Recognize the difference: an `npm error`, a stack trace, or a CLI usage/parse error means the tool didn't run, and that's not evidence the code is unused — it's a gap in your investigation to note in the report, not a clean result.

## Step 5: Redundancy — scoped to the target's neighborhood

Redundancy is a different question from dead code: not "is this referenced," but "does this duplicate something else." Default to comparing the target against its natural neighborhood — the same directory, the same feature module, files it imports or is imported by, or files with an obviously similar name/purpose — not the whole codebase, unless the person asks for a repo-wide duplication sweep.

- **True redundancy** — same logic, same reason, no sign it's meant to diverge. Worth naming as a consolidation candidate.
- **Coincidental similarity** — looks alike because the underlying logic is simple (a short null-check), not because it was copy-pasted. Don't recommend consolidating trivial code just because it resembles something else — an abstraction has its own cost.
- **Deliberate or emerging divergence** — started identical, shows signs of diverging (different edge-case handling, comments referencing different concerns). Flag as "was similar, may be diverging," not "safe to merge." Only claim git-history-based divergence if you actually ran `git log`/`git blame` and can point to what it showed — don't assert an age or history claim you didn't check.

For every redundancy finding, name every location involved, not just the first two — that changes whether consolidating is worth it. `jscpd`, scoped with a path argument to the target's directory (not the repo root), is useful here for literal/near-literal duplication; genuinely structural repeats (the same shape with renamed variables, the same wrapper pattern applied several times) usually need a manual read, since a tokenizer only catches so much.

## Confidence levels

Say plainly what was checked, and let the confidence label follow from that — don't default everything to one level out of habit.

- **High confidence**: the finding is a structural fact the language or framework itself enforces. Examples:
  - an unregistered NestJS controller, or a FastAPI router never passed to `include_router`, literally cannot receive requests;
  - code after an unconditional `return` literally cannot execute;
  - a `tsc` diagnostic like `TS6133`, or a `ruff` `F401`/`F841`, about a name within that same file. These don't get weaker no matter how far you searched, because they don't rest on the *absence* of something — they're true regardless.
- **Needs review**: the finding rests on *not finding* a reference within some bounded search (Step 3). This is the common case for "unused export," "unused component," "unused provider" — say exactly what scope was searched (same file / project / +sibling projects) and what wasn't (e.g., "not checked for dynamic/string-based references," "not checked cross-project"). A needs-review finding with a clearly stated scope is more useful than a false "high confidence."

## What NOT to flag

- **Names referenced through a string.** Dynamic `import()`, `require(variable)`, `importlib.import_module`, `getattr`, reflection, a router or plugin config built from strings, or a custom DI token. The absence of a static import doesn't mean the absence of use.
- **Published public API or SDK surface,** even with zero in-repo references. External consumers may depend on it.
- **Test code, even if unused today:**
  - test utilities, fixtures, and mocks;
  - anything under `__tests__`, `test`, `tests`, or `spec`;
  - `*.spec.ts`, `*.test.ts`, `test_*.py`, and `conftest.py`. Pytest fixtures are used by *parameter name*, not by import.
- **Entry points.** They look unreferenced to import-graph tools by definition:
  - `main.ts` and root modules or components;
  - `index.ts` or `__init__.py` at a package boundary;
  - names listed in `__all__`;
  - `[project.scripts]` / `[project.entry-points]` targets;
  - `if __name__ == "__main__":` modules;
  - migration files a migration tool loads by directory.
- **Error-handling and fallback branches** that haven't been exercised yet. Untested isn't the same as unreachable.
- **Framework patterns that look dead to a plain search but aren't.** See `references/frameworks.md`. The most common traps:
  - Angular's router-only and dynamically instantiated components;
  - `@Global()` NestJS modules;
  - Next.js file-based routes;
  - FastAPI dependencies used only through `Depends(...)`.
- Framework-generated or scaffolded boilerplate that's expected to look identical by convention — that's not redundancy.

If you're genuinely unsure whether something is dead versus subtly used, or whether two blocks are true redundancy versus coincidence, say so as "needs review" with the specific gap named, rather than either suppressing the finding or asserting a confidence the search doesn't support.

## Related Standards

| Concern | Skill | What it adds |
|---|---|---|
| Dead code and duplication at the level of a whole change | `code-hygiene` | No newly unreferenced code, true-vs-coincidental duplication, unused imports and dependencies |
| Where consolidated logic should live | `code-structure` | Orchestration vs shared-mechanics layering once a redundancy is confirmed |
| Whether a removal elsewhere lost a capability | `historical-regression-check` | Baseline comparison with a relocation check |

## Report format

Keep it proportional to what was actually investigated — a single-file check doesn't need the full template below, just its relevant pieces. For anything beyond a single quick answer, use this shape:

```
Refactor Audit — <target: file/directory/symbol referenced>
=====================================
Scope: <target> in project <project root>[, expanded to <sibling project(s)/reason> if applicable]
Not checked: <anything explicitly out of scope — e.g. "did not search sibling projects",
"did not run a repo-wide sweep" — so the person knows the edges of this investigation>

## Dead code candidates
- <file>:<line> — <symbol/import/component>: <finding>
  Evidence: <what was checked — same file / directory / project / +sibling projects,
  which tools if any, and their caveats>
  Confidence: <high | needs review — [what wasn't ruled out]>

## Redundancy candidates
- <pattern> — found in: <file>:<lines>, <file>:<lines> [all locations]
  Suggested approach: <e.g. "extract shared helper" — or "needs review, may be diverging">

---
Summary: <N> findings — <N> high confidence, <N> needs review.
```

If the answer is simple ("yes, this export is used in three places, here they are"), just say that — don't force the full template onto a quick, confidently-resolved question.

---
name: code-hygiene
description: Checks that a change does what was asked and leaves the code clean, in any language. Covers acceptance criteria traced to code, exhaustive enum handling, date and money correctness, dead code, duplication, type strictness, magic values and debug residue. Use before commit, when finishing a change, or when reviewing one.
license: MIT
metadata:
  pack: core
---

# Code Hygiene and Change Completeness

Two questions apply to every change: **does it actually do what was asked**, and **does it leave the codebase cleaner than it found it**. Cite a rule by section number and title, for example "code-hygiene §4.2, abstractions must earn their existence".

**Precedence.** When a formal review is running (a pull request, a commit, a branch diff), the framework pack's code-review skill owns the process and the output shape, or the core `code-review` skill where no framework pack applies, and this skill supplies criteria it cites. Use this skill directly when finishing your own work.

## 1. Scope

These rules hold in any language. Where a check needs a language-specific tool, both TypeScript and Python forms are given. Framework-specific hygiene (naming, member order, template and component conventions, the idiomatic mechanism for derived state) lives in the framework pack's guidelines skill.

Each rule carries its tags: `*[engineering classification] · Source: [strength]*`.

## 2. Requirement-to-Implementation Traceability

### 2.1 Every Acceptance Criterion Maps to Code
*[universal] · Source: [proposed engineering convention — no external source]*

- Every acceptance criterion in the linked ticket or spec maps to an identifiable code path in the change. A criterion with no implementation is either declared out of scope in writing or carries a tracked TODO (§6.1).
- **Verify:** list the stated criteria. For each one, name the file and symbol that implements it. Report criteria with no locatable implementation as gaps, never as passing. A criterion deferred behind a tracked TODO or a written out-of-scope note is reported as deferred, with its reference, and is not a gap. Each criterion should also trace to at least one test whose name states the behaviour.

### 2.2 No Partial Implementation Behind a Complete-Looking UI
*[universal] · Source: [proposed engineering convention — no external source]*

- A UI control that is rendered and enabled is wired to a working handler. A button or menu item bound to an empty method, a bare `return`, or a handler that only logs is removed, disabled with a stated reason, or completed.
- The same holds outside the UI. A function, handler or job whose body does nothing, or that reports success whatever the outcome, is completed, removed or marked unimplemented.
  - ❌ A `send()` whose body is `pass` under a docstring that says it delivers the message.
  - ❌ An "Export" button whose handler is `exportAll() {}`
- **Verify:** for each interactive binding in changed templates or components, follow the handler to a terminal effect: a service call, a state change, or a navigation. Flag terminals that do nothing, and functions whose stated effect (a send, a save, a charge) is never performed or is reported as done whatever the outcome. A control disabled on purpose communicates why, and exposes that state programmatically, not by opacity alone.

### 2.3 Exhaustive Handling of Enumerated Business States
*[universal] · Source: [proposed engineering convention — no external source]*

- Any branch keyed on a domain enum or union handles every member, or has an explicit default that fails loudly (throws, or logs and reports). It never falls through silently.

```ts
switch (task.status) {
  case TaskStatus.Open: /* ... */ break;
  case TaskStatus.InProgress: /* ... */ break;
  case TaskStatus.Done: /* ... */ break;
  case TaskStatus.Cancelled: /* ... */ break;
  default: {
    const unhandled: never = task.status; // compile error when a member is added
    throw new Error(`Unhandled task status: ${unhandled}`);
  }
}
```

```python
match task.status:
    case TaskStatus.OPEN: ...
    case TaskStatus.IN_PROGRESS: ...
    case TaskStatus.DONE: ...
    case TaskStatus.CANCELLED: ...
    case _:
        assert_never(task.status)  # typing.assert_never, Python 3.11+; typing_extensions before
```

  - ❌ Handling `OPEN` and `DONE` while `CANCELLED` silently renders nothing.
- **Verify:** compare each `switch`, `match`, or `if` chain (and any template switch) against the enum or union declaration; count members against branches. Enums that cross the wire carry stable string values that match member for member on both sides.

### 2.4 Date, Time, and Timezone Correctness
*[universal] · Source: [established industry practice — ISO 8601]*

- Timestamps cross the API as ISO 8601 with an offset (UTC). The server stores UTC in a timezone-aware column. Clients convert to local time only for display.
- No parsing of locale-formatted date strings, and no date-only value where an instant is meant.
  - ❌ `new Date('24/08/2026')`, manual `split('/')` parsing, or `toLocaleDateString()` output sent back to the API.
  - ❌ `datetime.now()` (naive) stored as an instant; use `datetime.now(timezone.utc)`.
- **Verify:** trace each date field from column type through the DTO or schema type and the client model to its display formatting. Flag text columns holding timestamps, naive datetimes, and hand-rolled parsing.

### 2.5 Money and Precise Numeric Values Never Use Floating Point
*[universal] · Source: [established industry practice]*

- Money, and quantities that must be exact, use `decimal`/`numeric` columns and cross the wire as strings or integer minor units, never as `float` or `double`. In Python, use `Decimal`, not `float`.
- A client-side floating-point sum is a display hint only, never an authoritative submitted value. The server recomputes totals.
  - ❌ `const total = rows.reduce((a, r) => a + r.amount, 0);` submitted as the invoice total.
  - ❌ `total = sum(float(line.amount) for line in invoice.lines)`
- **Verify:** inspect column types on money-like fields and their DTO or schema types. Flag client-computed currency totals that are submitted rather than only displayed.

### 2.6 Single Source of Truth for Derived State
*[universal] · Source: [established industry practice]*

- A value derivable from existing state is derived, not stored in a second field and kept in sync by hand.
- **Remedy:** a getter, computed property, or derivation in the one place that owns the source. The framework pack's guidelines skill names the idiomatic mechanism for its version.
- **Verify:** look for a field assigned from the same inputs in more than one place, or recomputed in several lifecycle hooks or event handlers, that one derivation would express once.

### 2.7 Defaults and Optional Chaining Do Not Hide a Meaningful Absence
*[universal] · Source: [proposed engineering convention — no external source]*

- A null-safe operator or a fallback value (`?.`, `??` and `||` defaults in TypeScript; `dict.get(key, default)` and `or` defaults in Python) is a defect only where it turns a **meaningful absence** into a value that flows downstream as if it were real data. A legitimate use, such as an optional display field, is not a finding.
- When a value is required for the operation (an owner id, a price, a tenant scope, an amount), its absence is an error to raise, not a default to substitute.
  - ❌ `const amountMinor = invoice.amountMinor ?? 0;`, which charges a missing amount as zero.
  - ❌ `assignee_id = payload.get("assigneeId", 0)`, which turns a missing assignee into the id `0`.
  - ✅ `if (invoice.amountMinor == null) throw new Error('Invoice has no amount');` · `if invoice.amount_minor is None: raise ValueError("Invoice has no amount")`
- A finding names the downstream consequence: what the substituted value feeds, and what state results.
- **Verify:** for each `?.`, `??`, `||` default, `.get(key, default)` and `or` default on a required value in the diff, trace where the result goes. Flag it only where the substitute reaches a write, a calculation, an authorization decision or an external call as if it were real data.

## 3. Dead Code and Duplication

### 3.1 Dead Code Investigation Follows the `refactor-checker` Procedure
*[universal] · Source: [proposed engineering convention — no external source]*

- Investigate suspected dead code with the `refactor-checker` procedure: targeted reference tracing, framework reference surfaces, confidence grading. Report it; never delete it silently.
- A single clean search does not prove something is dead. Each of these looks dead to a text search and isn't:
  - components reached only through router configuration;
  - providers registered by string or injection token;
  - dynamically registered entities and plugins;
  - barrel and `__init__.py` re-exports;
  - `__all__` lists;
  - decorator-based registries;
  - packaging entry points.
- **Verify:** follow that procedure. If it is unavailable, keep its core discipline: state the exact scope searched, and report a not-found result as "needs review within \[scope\]", not as proof.

### 3.2 The Change Introduces No Newly Unreferenced Code
*[universal] · Source: [proposed engineering convention — no external source]*

- Every symbol **added by this change** has at least one consumer added by the same change, or is an intentional public or API entry point stated as such. Speculative helpers, unused DTO fields, and unused component inputs are removed before merge.
- This is narrower and far more reliable than a repo-wide dead-code sweep, because the change is the whole search space.
- **Verify:** for each new export or member in the diff, search for a use within the diff, then within the project.

### 3.3 Duplication Is Consolidated Only When It Is True Duplication
*[universal] · Source: [established industry practice]*

- The same logic implemented at two or more sites **for the same reason** is extracted once.
- Do **not** consolidate coincidental similarity (a short null check, framework boilerplate) or code showing signs of deliberate divergence. An abstraction has its own cost.
- Copy-pasted code introduced **by this change** is always a finding.
- **Verify:** classify each candidate as true duplication, coincidental similarity, or emerging divergence. Name **every** location involved, not just the first two, because the count decides whether consolidating is worth it.

### 3.4 Unused Imports, Declarations, and Dependencies Are Removed
*[universal] · Source: [established industry practice]*

- The change leaves behind none of these:
  - an unused import;
  - an entry in a framework registration list (module declarations, provider arrays, router tables) pointing at a removed class;
  - a dependency added to `package.json` or `pyproject.toml` but never used.
- **Verify:**
  - **TypeScript:** `tsc --noEmit --noUnusedLocals --noUnusedParameters`. Only diagnostics `TS6133` and `TS6192` are hygiene findings. Write `.tsbuildinfo` outside the repository when the project sets `incremental` or `composite`.
  - **Python:** `ruff check --select F401` (or `pyflakes`) for unused imports.
  - **Registration lists and dependency manifests** need a manual check against the code that still exists.

## 4. Structure Smells

### 4.1 A Class With More Than One Reason to Change Is Split
*[universal] · Source: [established industry practice — single-responsibility principle (concept); proposed engineering convention (criteria)]*

- Split when any of these hold:
  - a service owns write logic for two or more unrelated entities or domains;
  - a component both orchestrates several unrelated data sources **and** owns substantial presentation logic;
  - one class mixes transport, business rules, and persistence.
- **Line count is not the criterion.** Where a style guide mentions a file or function size, cite it as a smell, never as a blocking limit.
- **Verify:** list the class's public responsibilities and the entities it writes, then name the specific pair of concerns that should separate.

### 4.2 Abstractions Must Earn Their Existence
*[universal] · Source: [proposed engineering convention — no external source]*

- Each of these is a finding unless a concrete second consumer or test seam is named:
  - an interface, abstract class, or protocol with exactly one implementation and no swap or test-seam need;
  - a service that only forwards to another service unchanged;
  - a wrapper around an ORM or HTTP client that adds no behaviour;
  - a generic "manager", "handler", or "helper" layer introduced for one call site.
- **Library default, for data access:** services use the ORM or data-access layer directly. A dedicated repository class is added only when an entity has complex query logic reused by two or more callers. A project that already uses a repository layer consistently keeps it.
- **Verify:** for each new interface, abstract class, protocol, or wrapper, count implementations and call sites. Indirection with one implementation and one caller is a finding.

## 5. Type Safety and Constants

### 5.1 Type-Checker Strictness Is Not Weakened
*[universal] · Source: [established industry practice]*

- **TypeScript:**
  - No `any`; use `unknown` plus narrowing.
  - No `@ts-ignore` or `@ts-expect-error` without a tracked reference.
  - No non-null assertion or `as` cast used to silence a value that is genuinely nullable or unvalidated.
  - No loosening of `tsconfig` strict flags.
    - ❌ `const row = response as TaskDto;` on an unvalidated payload.
    - ❌ `"strictNullChecks": false` added to make the build pass.
- **Python:**
  - No `Any` where the type is known.
  - No bare `# type: ignore` without an error code and a tracked reason.
  - No `cast()` used to silence an `Optional` that can really be `None`.
  - No loosening of mypy or pyright settings (`strict`, `ignore_errors`, new `ignore_missing_imports` entries) to make a change pass.
  - Public functions in a typed codebase keep their annotations.
- A nullable API field is optional on both sides of the wire, and handled rather than asserted away.
- A project with no type checker configured: this rule applies only to not weakening what exists.
- **Verify:** search the diff for `: any`, `as any`, `!.`, `@ts-ignore`, `Any`, `# type: ignore`, and `cast(`. Check diffs of `tsconfig*.json`, `mypy.ini`, `pyproject.toml`, and `pyrightconfig.json` for relaxed settings.

### 5.2 Domain Values Are Named Constants, Not Literals
*[universal] · Source: [established industry practice]*

- Status strings, role names, thresholds, debounce intervals, minimum query lengths, page sizes, and retry counts are declared constants or enum members shared with their consumers. They are not literals repeated across files.
  - ✅ `export const SEARCH_DEBOUNCE_MS = 300;` · `SEARCH_DEBOUNCE_SECONDS = 0.3`
  - ❌ The same `300` written inline at four call sites.
- **Verify:** flag literals repeated in two or more places, and any domain-meaningful number inline in a changed file.

## 6. Residue

### 6.1 Deferred Work Is Tracked, Not Commented
*[universal] · Source: [established industry practice — e.g. the TODO format in Google's style guides]*

- Deferred behaviour is recorded only as a TODO naming a tracked issue, in the project's reference format: `// TODO(PROJ-123): …` or `# TODO(#42): …`. Untracked TODOs, "not implemented yet" prose, and commented-out attempts are not records.
- **Verify:** search the diff for `TODO`, `FIXME`, and `XXX` with no issue reference. This rule gives §2.1's gap reporting a legal landing place; the full comment style is owned by `commenting-standards`.

### 6.2 No Commented-Out Code and No Debug Residue
*[universal] · Source: [established industry practice]*

- Committed code contains none of these:
  - commented-out code blocks;
  - debugger statements;
  - ad-hoc console output;
  - temporary hard-coded test values.
- Deliberate logging goes through the project's logger and never writes a credential, token, or personal data.
- **Verify:** search the diff for multi-line comment blocks containing code syntax, and for:
  - **TypeScript:** `console.`, `debugger`, `alert(`.
  - **Python:** `print(`, `breakpoint()`, `pdb.set_trace()`, `import pdb`.

### 6.3 Generated and Vendored Files Are Not Hand-Edited
*[universal] · Source: [established industry practice]*

- These files are never hand-modified in a feature change:
  - lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `poetry.lock`, `uv.lock`);
  - generated API clients;
  - migration snapshots a tool produced;
  - build output.
- Changes go through the generator or the dependency tool.
- **Verify:** flag manual edits inside generated-file markers, and any `dist/`, `build/`, `node_modules/`, `__pycache__/`, or virtual-environment path in the diff.

## 7. Related Standards

Every rule above is actionable from this file alone. These adjacent concerns have their own skills.

| Concern | Skill | What it adds |
|---|---|---|
| Dead-code and redundancy investigation, and its tool caveats | `refactor-checker` | The procedure behind §3.1 |
| Where shared logic belongs once duplication is confirmed | `code-structure` | Orchestration vs shared-mechanics layering |
| Comment and docstring style, banned vocabulary, the exact TODO form | `commenting-standards` | Comment rules behind §6.1 |
| Framework naming, member order, templates, the derived-state mechanism | The framework pack's guidelines skill | Framework-specific hygiene |
| Nullability, enum wire values, column types for money and time, test levels | The framework pack's contract, persistence, and testing skills | The wire, storage, and test detail behind §2.3–§2.5 |

## 8. Pre-Commit / Pre-Save Verification Checklist

- [ ] Every acceptance criterion maps to a named file and symbol; gaps are reported, not assumed covered.
- [ ] No rendered, enabled control is wired to an empty or log-only handler.
- [ ] Every branch on a domain enum or union is exhaustive, or fails loudly by default.
- [ ] Dates cross the wire as ISO 8601 UTC; no locale-string parsing; no naive or free-text timestamps.
- [ ] Money uses decimal types and string or minor-unit transport; no client-computed total is submitted as authoritative.
- [ ] No derived value is stored twice and kept in sync by hand.
- [ ] No default value or null-safe operator turns a missing required value into data that flows downstream as real.
- [ ] Suspected dead code was investigated with a stated search scope and reported, never deleted on a single search.
- [ ] Every symbol added by this change has a consumer added by this change, or is a declared entry point.
- [ ] Duplication introduced here is consolidated; existing similarity was classified, with every location named.
- [ ] No unused import, stale registration entry, or added-but-unused dependency remains.
- [ ] No class was left owning two unrelated reasons to change; any size observation is stated as a smell, not a limit.
- [ ] Every new interface, protocol, wrapper, or indirection layer has a named second consumer or test seam.
- [ ] Type-checker strictness is not weakened in code or configuration.
- [ ] Domain values and tuning numbers are named constants shared with their consumers.
- [ ] Every deferred item is a TODO with a tracked reference; no commented-out code or debug residue.
- [ ] No hand-edited lockfile, generated client, or build output.

If any item fails, fix it before proceeding — don't leave a partially-compliant change in place.

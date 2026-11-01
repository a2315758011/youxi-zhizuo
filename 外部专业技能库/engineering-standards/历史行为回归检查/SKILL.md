---
name: historical-regression-check
description: Compares a whole change (PR, branch commits, staged and working-tree edits) with the implementation before the work began, to find lost validation, weakened authorization, dropped query conditions and new failure modes. Reports only. Use when reviewing before merge, auditing a refactor, or asking whether a change broke something.
license: MIT
metadata:
  pack: core
---

# Historical Regression Check and Code Archaeology

A standard diff review asks, "Is this new code written correctly?" A historical regression check asks the deeper question: **"Did something that used to work stop working, or did a refactor or optimization silently break a business rule or add a new failure mode?"** Cite a step as "historical-regression-check §N, <step title>".

The unit of comparison is **capability and business intent, not raw text**. The textual diff is only the starting point. The goal is to understand what the old code and the new code actually do.

## 1. When to Run

- **PR and feature-branch review:** before merging a feature, refactor, or query optimization.
- **Work in progress:** when uncommitted or staged changes sit on top of branch commits.
- **Refactor and optimization audits:** after query tuning, caching, batching, or deduplication, to confirm business logic was not altered.
- **Baseline comparison:** when comparing the working directory with a baseline branch, or with a separate baseline folder.

## 2. Establish the Cumulative Scope and the True Baseline

**Avoid the single-commit trap.** Never review only the latest commit. A regression can be introduced five commits back in the same branch, or sit uncommitted in the working tree. Compare the state **immediately before the work began** with the current working tree.

### 2.1 Current State: Branch Commits, Staged, and Working Tree

```bash
git status -s                   # uncommitted and staged modifications
git diff HEAD --stat            # everything not yet committed, against HEAD, as files and line counts
git diff HEAD -- <file-path>    # then one file at a time
```

### 2.2 Baseline

- **PR or feature branch:** the merge base with the branch it targets. Find the default branch rather than assuming its name:
  ```bash
  git symbolic-ref --short refs/remotes/origin/HEAD     # e.g. origin/main
  git merge-base origin/main HEAD
  ```
- **A ticket or issue id** (e.g. `PROJ-123`): the parent of the first commit that mentions it.
  ```bash
  git log --format='%H %s' --grep='PROJ-123' --reverse
  git rev-parse <first-commit-sha>^
  ```
- **A separate baseline folder** (e.g. `../project-baseline`): compare directories directly. This works outside a repository too:
  ```bash
  git diff --no-index ../project-baseline/src ./src
  ```

### 2.3 Cumulative Diff

```bash
git diff <baseline-sha> --stat             # baseline vs the working tree, unstaged edits included: files and line counts
git diff <baseline-sha> -- <file-path>     # then one file at a time
```

Start from the file list and read the diff one file at a time, for every file that carries logic: source, tests, schemas, migrations and configuration. Judge lockfiles, generated code and build output from their line counts, and open one only when the counts raise a question. A full diff read at once can be dominated by a regenerated lockfile.

State the scope and the baseline at the top of the report (§7). A finding without its baseline cannot be re-checked.

## 3. Rule Out Relocation Before Calling Anything Removed

A deleted line is not a lost capability until you have looked for where it went. Before reporting a removal, search for the capability's new home:

- moved to another function, file, or module (search for the distinctive condition, constant, or message text, not just the old symbol name);
- moved into a shared layer: middleware, interceptor, guard or dependency, decorator, base class, validation schema;
- moved into the database: a constraint, default, trigger, or view;
- replaced by an equivalent mechanism: a schema validator instead of a hand-written check, a query predicate instead of an in-memory filter.

Report a removal as a regression only when no relocated or equivalent form exists. Name the places you searched.

## 4. The Archaeology Questions

Apply these to every modified file or method before judging it.

### 4.1 What Is the Business and Operational Domain?

- How does the feature work from the end user's side: views, forms, buttons, imports, dialogs?
- What are the formulas, state transitions, and data relationships underneath?

### 4.2 What Was the Original Developer's Mental Model?

- What was the original code trying to achieve?
- What happy path or operational assumptions did it encode? For example, did it assume entries are always created forward in time, or that spreadsheet dates always arrive as text?

### 4.3 Why Didn't It Break in Production Before?

If the old code had a bug or limitation, why did users not report it? Identify the conditions that let it survive:

- Users rarely edited an entry in the middle of a sequence.
- The UI filtered on a different field than the one that was wrong.
- Uploads stayed small enough to finish inside the server timeout.

### 4.4 What Is the New Code's Intent?

- A **bug fix** repairing a broken invariant?
- A **performance change**: batching, lazy loading, caching, in-memory aggregation?
- A **contract or strictness change**: new validation, new authorization checks?

### 4.5 Could the New Code Introduce New Failure Modes?

Run a boundary scenario matrix on the new implementation:

| Scenario | Question |
|---|---|
| **A. First / minimum** | What if the record is the very first entry, or the minimum allowed value? |
| **B. Nominal** | What happens during normal forward progression? |
| **C. Last / maximum** | What if the record is the latest, with nothing after it? |
| **D. Empty / zero / null** | What if records are missing, empty, or zeroed? |
| **E. Cross-tenant / cross-entity** | Could data from another tenant, owner, or account leak into this result? |

### 4.6 What Is the Blast Radius?

- If a shared service, utility, or UI component changed, find **every consumer**:
  ```bash
  git grep -n '<SymbolName>'
  ```
- Did the change alter shared lifecycle behaviour, default parameter values, or the inputs a component accepts?
- Do guards keep the change from affecting callers it was not meant for?

## 5. Capability Comparison Matrix

Walk the baseline against the current code for each category:

| Category | Compare in baseline vs current | Lost or weakened patterns |
|---|---|---|
| **Input validation** | Schema and DTO validation, parsing, format checks, range checks | Dropped validation; unparsed text accepted; missing negative or range checks |
| **Authorization and scope** | Tenant filters, ownership and hierarchy checks, role checks | A tenant or owner predicate removed from a query's `where` clause; the caller's identity no longer passed to the data layer |
| **Business formulas** | Calculations, running balances, cascading updates | Off-by-one; a carried-forward balance reset to zero; an inverted sign |
| **Data and transactions** | Batching, transactional atomicity, locking, relation loading | A multi-step write losing its transaction; batched queries replaced by queries in a loop (N+1) |
| **State handling** | Loading indicators, subscription and listener teardown, in-place updates | Missing teardown; UI state not refreshed after background updates |
| **API contracts** | Route paths, HTTP methods, parameter names, status codes, response shape | A renamed parameter (`start_date` → `startDate`) without checking mobile or third-party consumers |

## 6. Classify Every Difference

1. **Intentional and verified:** a bug fix or optimization.
   - It corrects a real shortcoming or removes a bottleneck, and the scenario matrix (§4.5) shows no new failure mode.
   - *Action:* record it as cleared. **An intentional change is never reported as a regression.**
2. **Confirmed regression:** a working capability, validation, authorization predicate, or state handling was removed or weakened, with no relocation (§3) and no stated justification.
   - *Action:* assign a severity, **🔴 BLOCKER** or **🟠 HIGH** (🟡 MEDIUM for a narrow edge case). Quote the baseline and the current code, and state the exact runtime consequence.
3. **Needs review:** a contract or strictness change, such as a request that used to be accepted now returning `400`, or a renamed parameter.
   - *Action:* mark it **❓ NEEDS REVIEW**, and name the consumers (mobile apps, integrations, other services) that must be confirmed.

## 7. Related Standards

| Concern | Skill | What it adds |
|---|---|---|
| Is a removed symbol really dead, or still referenced elsewhere? | `refactor-checker` | Evidence-graded reference tracing |
| Did the change implement what was asked? | `code-hygiene` | Acceptance-criteria traceability for the change itself |
| Running this as part of a full review | `code-review`, or the framework pack's code-review skill | Loads this check as a separate pass and reports it in its own section |

## 8. Output Structure

```markdown
# Historical Regression Check

**Scope:** <branch / PR / working tree>
**Baseline:** `<baseline-sha>` or `<baseline-branch>` (state before the work began)
**Files compared:** <n>

## 1. Domain Overview
[What the module does: user workflows, key actions, core formulas]

## 2. Change-by-Change Analysis

### `<function or method>` in `<file-path>`
1. **What the code does as a whole:** [end-to-end flow]
2. **Original mental model:** [what the old code assumed]
3. **Why it did not break before:** [the conditions it survived under]
4. **New intent:** [bug fix, optimization, refactor, or hardening]
5. **Boundary matrix:** A [pass/fail and why] · B [...] · C [...] · D [...] · E [...]
6. **Relocation check:** [where a removed capability was searched for, and what was found]

## 3. Blast Radius
[Shared services, components, or DTOs changed; every consumer; whether guards prevent collateral effects]

## 4. Contract and Compatibility
[Parameter names, status codes, response shapes, and which external consumers depend on them]

## 5. Summary
- 🔴 BLOCKER / 🟠 HIGH / 🟡 MEDIUM **Confirmed regressions:** [none, or each with baseline vs current]
- ✅ **Cleared (intentional and verified):** [each improvement checked]
- ❓ **Needs review:** [contract or strictness changes needing the author's sign-off]
```

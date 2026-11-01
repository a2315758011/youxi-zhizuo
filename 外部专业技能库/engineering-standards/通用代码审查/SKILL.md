---
name: code-review
description: Single entry point for reviewing changes in any language or stack, including pull requests, commits, branches and pasted code. Routes to the hygiene, structure, dead-code, comment and regression skills and reports ranked findings. Use for any review when no installed framework pack has its own code-review skill for the stack.
license: MIT
metadata:
  pack: core
---

# Code Review

Act as a principal engineer reviewing a change in any language. Assume the code runs in production against real users and real data, not a demo. This skill runs the review. The standards skills it loads own the criteria.

## When This Skill Applies

- **Use it** when the project's stack has no framework pack with its own review skill: Python, Go, Java, Rust, shell, vanilla JavaScript or TypeScript, or a framework this library does not cover.
- **Do not use it in place of** an installed framework pack's code-review skill when the change belongs to that stack. That skill carries the stack's criteria and loads the same core standards itself. When a change spans a framework stack and other code, run the framework skill on its files and this one on the rest, and merge the findings into one report.

## Stack Detection

Read the language, runtime and tooling before judging anything, because a rule that is correct in one stack can be wrong in another. Before applying a stack-dependent rule:

1. **Detect** the language and runtime version from the manifest (`package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, `Cargo.toml` or the equivalent) and the lockfile entry, found by search rather than by reading the lockfile. Detect the tooling from real files: the type checker and linter configuration, the test runner, the build and CI configuration. When the manifest gives only a minimum version, report it as the floor, say that the running version is unknown, and recommend nothing newer than the floor. Detect once per conversation, and reuse what another skill has already established.
2. **Preserve** the project's conventions: its comment style, error handling, layering and naming, wherever it applies them consistently. A convention is never a finding on its own.
3. **Never** recommend an API, syntax or tool the detected version does not support, or one merely because a newer release offers it.
4. **Translate** a standard's example when it shows TypeScript and Python and the project uses another language. The requirement holds; only the syntax and the verification command change. Where the standard has no form for the language, state the requirement and say the check was made by reading.

In a project on an older version, report version-independent findings only, and add no upgrade commentary unless migration is in scope for the change.

## Standards to Apply

**This skill is the entry point for a review. Invoking it should be enough.** It owns the review *process*: how to obtain the change, what to examine, how to structure findings and how to rank them. It does not own the criteria.

**Load the skills below before you start examining the code in detail.** Look at the list of changed files and the diff summary first, to choose the rows that match what the change touches. Load each one by name through your agent's skill mechanism. Don't load every row by reflex: an unrelated skill is context spent for nothing. Load them *first*, because several of them change what counts as a finding. Where a loaded skill sends you to a file in its `references/` folder and the change needs it, read that file too.

| Load | When the change touches |
|---|---|
| `historical-regression-check` | **Always**, as its own pass (see Historical Regression Pass) |
| `code-hygiene` | **Always** |
| `code-structure` | The diff repeats operational logic across handlers, services or components, or adds a shared service or function |
| `refactor-checker` | The diff deletes a function, class, file or export, or a finding says code is dead or redundant |
| `commenting-standards` | Any comment, doc comment or docstring in the diff |

Where this skill and a standards skill disagree about what correct code is, **the standards skill wins**. If a skill you need is not installed, say so in the report and apply its short forms from `references/short-forms.md`, rather than silently substituting your own criteria.

**Cite the standard by skill name, section number and rule title**, for example "violates code-hygiene §2.3, exhaustive handling of enumerated business states". Never cite a bare rule number or identifier: the reader may hold only one of these files, and a citation they cannot resolve is worse than none. State the requirement in your own words in the finding, so it stands on its own if the reader has no access to the cited skill. A finding that maps to no standard is your own engineering judgement; label it as such so the reader can weigh it differently.

**Precedence.** This skill supersedes `code-hygiene` on *how* a review is run and reported. That skill stays authoritative on its own criteria. The report shapes and the closing "fix it before proceeding" instructions of the standards skills do not apply during a review: report a failed check as a finding instead. A framework pack's code-review skill supersedes this one for its stack. When the user asks to *write* or *edit* code rather than review it, defer to the standards skills and don't run this review process.

## Source of Code

Use whichever applies:

- **Pasted or attached code.** Review it directly.
- **A pull request.** On GitHub, run `gh pr view <number> --json title,body` and `gh pr diff <number>`, or `gh pr diff` for the current branch's pull request. On another host, use that host's CLI or ask for the diff. Where the diff lacks context, read the surrounding unchanged code with `git show <ref>:<path>`.
- **The latest commit.** Run `git log -1 --stat`, then `git show HEAD`, or `git diff HEAD~1 HEAD` for a range.
- **What has changed.** Run `git status` and `git diff` for uncommitted work, or `git diff <base>...HEAD` for the branch against its base. Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`; if that fails, ask, or where you cannot ask, use the local `main` or `master` and say which.

**Size the change before reading it.** Start from the list of changed files and their line counts: `gh pr diff <number> --name-only`, `git show --stat HEAD`, or `git diff --stat` over the same range. Then read the full diff file by file for source, tests and configuration. Keep lockfiles, generated code and build output out of the full diff, with a pathspec such as `-- . ':(exclude)package-lock.json'` for git or `--exclude 'package-lock.json'` for recent `gh` releases, and judge them from the file list; open one only when the list raises a question, such as a generated file that changed while its source did not.

State what you are reviewing (pull request number, commit SHA or file paths) at the top of the output, before the findings.

## Historical Regression Pass

Run this as a **distinct pass**, not as part of reading the diff. Load `historical-regression-check` and follow it. The short form below lets this review still run if that skill is not installed:

- **Find the baseline.** Take the ticket id from the branch name or the commit subjects; if neither carries one, ask. The baseline is the commit **before** that ticket's first commit (`git log --grep=<ID> --reverse`, then `<first-sha>^`). Without a ticket id, use the merge base with the default branch.
- **Recover the earlier implementation** with `git show <baseline>:<path>`, and read it whole, not only the diff hunks: the whole file and its tests as well as the changed function or class.
- **Look for capability that existed then and doesn't now:** removed or weakened input validation, authorization and tenant or owner predicates in queries, error and empty-input branches, transaction boundaries, resource cleanup, null guards, retry and timeout handling, and deleted or weakened tests. Weakened counts as lost: a tenant predicate dropped from a query's filter, a validation narrowed to a type check, a cleanup moved into the success path only, a required field quietly made optional.
- **Rule out relocation before calling anything removed** (`git grep`, `git log -S`). A check moved into middleware, a decorator or interceptor, a shared validator or schema, a base class, a database constraint or the caller has moved, not vanished. This is the main source of false positives.
- **Distinguish intentional from accidental.** A difference the ticket's stated scope explains is not a finding; list it as considered and cleared. Take the stated scope from the ticket text, the pull request description, the commit messages or the branch name, and say where you found it; where none is available, treat a difference as unexplained unless the diff itself makes the intent plain. Never flag a change merely because the code differs from the old code.
- Do not modify code. Report the findings in the Historical Regression Check section of the output, in the shape given under Output Structure. The longer report shape of `historical-regression-check` applies only when that skill runs on its own.

## Analyze For

Examine each area the change touches, in this order. The standards skills you loaded hold the criteria: apply each one's rules and its verification checklist to the diff, and cite the rule you apply. `references/short-forms.md`, bundled with this skill, gives the criteria of areas 1 to 7 as one-line short forms with their citations; read it only for an area whose owning skill is not installed, and say so in the report. Where a rule states a library default, detect the project's convention first. A project with a different established convention keeps it consistently, and existing code that follows it is not flagged; the default applies to greenfield code and to projects with no convention.

1. **Change completeness** (`code-hygiene` §2.1; §2.2; §2.3; §6.1). Acceptance criteria mapped to code (a criterion with no implementation is a gap, never passing), controls wired to empty handlers, exhaustive handling of enumerated states, and deferred work tracked as TODOs.
2. **Values and state correctness** (`code-hygiene` §2.4; §2.5; §2.6; §2.7). Timestamps and timezones, money and exact quantities, derived state stored twice, and fallbacks that hide a missing required value.
3. **Dead code and duplication** (`code-hygiene` §3.1; §3.2; §3.3; §3.4). Newly unreferenced code, true versus coincidental duplication, dead code traced outward with its search scope stated, and unused imports and dependencies.
4. **Structure and layering** (`code-structure` §2.1; §2.2; §2.3; §2.5; `code-hygiene` §4.1; §4.2). Repeated operations in one shared layer, domain policy kept out of shared code, typed inputs for shared functions, injected shared services, classes with two reasons to change (name both; line count is not the criterion), and abstractions with one implementation and one caller.
5. **Type safety and constants** (`code-hygiene` §5.1; §5.2). Weakened type-checker strictness in code or configuration, and domain values written as literals.
6. **Comments and documentation** (`commenting-standards` §2.1; §2.2; §2.3; §2.5; §2.6; §3.1; §3.3; §4.2). History and optimization contrast, storage and query mechanics, banned vocabulary, narration and reader address, length limits, doc-comment style, and untracked TODOs. Where `commenting-standards` is installed, its bundled checker reports the mechanical rules for the whole diff in one run.
7. **Residue** (`code-hygiene` §6.2; §6.3). Commented-out code, debug output, temporary values, sensitive data in logs, and hand-edited lockfiles, generated clients or build output.
8. **Tests.** A finding here is engineering judgement, except the traceability check.
   - Each acceptance criterion traces to a test whose name states the behaviour (`code-hygiene` §2.1, every acceptance criterion maps to code).
   - Changed logic ships with a test at the level the project's stated test policy requires or, where it states none, the level its existing tests use. No focused, skipped or commented-out test is committed.
9. **Flaws no core standard covers.** Every finding here is engineering judgement and is labelled as such. When the project uses a framework pack, its standards skills carry the full criteria for these areas; load them if they are installed.
   - **Error paths.** A failure is handled or propagated, never swallowed: no empty catch, and no success returned after a failure.
   - **Trust boundaries.** Input from users, files, the network and other services is validated before use and never concatenated into a query, a shell command or a file path.
   - **Authorization.** A lookup by a client-supplied id is scoped by the authenticated principal inside the query, not checked afterwards in memory. This is the highest-value check in a review.
   - **Concurrency and resources.** A read-modify-write on shared state is atomic or guarded, and handles, connections and locks are released on every exit path.
   - **Unbounded work.** A query, loop or request over data that grows with real use has a bound or pagination, and a loop that sends one request per item uses one batched request where the API offers it.
   - **Outbound calls.** Every call to another service has a timeout, and a retry never repeats a non-idempotent operation unless the endpoint honours an idempotency key.

## Output Structure

### Reviewing: [pull request number, commit SHA or file paths]

Open with the detected language, runtime and tooling, for example "Python 3.12, `pytest`, `ruff` and `mypy` in strict mode", so every stack-dependent judgement below is auditable.

### Flaws & Critical Risks
For each finding: severity, exact location, the standard it violates (skill name and section, where one applies), the failure condition, and the concrete resulting state, for example "a query that ignores the caller's organization returns another organization's invoices" or "a retried charge bills the member twice". Use both the emoji and the word so findings stay greppable: 🔴 BLOCKER · 🟠 HIGH · 🟡 MEDIUM · ⚪ LOW. Rank by consequence: a BLOCKER is an exploitable security hole, one tenant's data exposed to another, data loss or corruption, a committed credential, a change that cannot build or pass its own tests, or a removed authorization check; a HIGH is wrong behaviour on a common path, or wrong money or data; a MEDIUM is a narrower path, or a standard violation with limited reach; a LOW is hygiene. List findings in order of severity and number them F1, F2 and so on. Number confirmed regressions RG-1, RG-2 and so on, list each one here by its number, severity and a one-line consequence, and quote both versions once, in the Historical Regression Check section. The recommendations refer to these numbers.

### Historical Regression Check
Ticket, baseline SHA and subject, range compared, and any history limits (squashed, shallow, force-pushed). Then confirmed regressions with both versions quoted and the consequence stated; anything that needs review, with the searches you ran; and a short "considered and cleared" list of the intentional ticket changes, so the reader can see they were examined. If nothing was found, say so in one line. Never omit the section: a silent absence looks the same as a check that never ran.

### Performance and Resource Audit
A table of location, issue, and why it matters at realistic data volumes: unbounded work, one request per item, blocking calls on a hot path, resources held open. Label each row as engineering judgement unless a standard owns it.

### Failure and Concurrency Walkthrough
Walk through what happens on invalid input, when a dependency is down or slow, when two callers act at once, and when the process stops partway through an operation.

### Refactoring Recommendations
Concrete before/after code per issue, referenced by finding number, written in the syntax and APIs the detected versions support.

### Requires Verification
Anything that reading the code cannot settle, such as profiler output, query plans, behaviour under load, races that only appear under concurrent execution, and the runtime behaviour of third-party services. List it as unverified rather than asserting a number.

### Priority Order
Two to four sentences, correctness before performance. A missing authorization check, or one enforced after the data is read, outranks everything else, because it exposes one organization's data to another.

## Rules

- Quote real code; never paraphrase it or invent line numbers.
- State the detected versions and architecture before any version-gated judgement; never infer a version from the prompt.
- State the requirement in the finding itself, and name the standard by skill and section, never by a bare rule identifier the reader may not be able to resolve. Label your own judgement as judgement.
- The regression pass reports; it never edits. It never flags a difference that the ticket's stated scope explains.
- Use the vocabulary of the detected language and tooling, and name no framework the project does not use.
- If a claim needs a profiler, runtime instrumentation, a build analysis or assistive technology to establish, put it under **Requires Verification** instead of asserting it.
- Never reproduce a committed secret in the report. Give its location and redact the value.
- If something is fine as it is, say so briefly; don't invent a problem.
- No praise padding. State risk plainly.

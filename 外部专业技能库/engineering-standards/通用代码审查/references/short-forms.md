# Code Review: Short Forms

The fallback criteria for `code-review`. Read this file only for an area whose owning skill is not installed, and say so in the report; when the owning skill is loaded, apply its rule instead. Each item is a short form: the requirement in one line, and the standard that owns its full treatment. Where a short form states a library default, detect the project's convention first. A project with a different established convention keeps it consistently, and existing code that follows it is not flagged; the default applies to greenfield code and to projects with no convention.

The numbers match the areas under Analyze For in `SKILL.md`.

1. **Change completeness.**
   - Every acceptance criterion of the linked ticket or spec maps to a named file and symbol; a criterion with no implementation is reported as a gap, never as passing (`code-hygiene` §2.1, every acceptance criterion maps to code).
   - No rendered, enabled control is wired to an empty or log-only handler (`code-hygiene` §2.2, no partial implementation behind a complete-looking UI).
   - Every branch on a domain enum or union handles every member, or fails loudly by default (`code-hygiene` §2.3, exhaustive handling of enumerated business states).
   - A deferred item is a TODO that names a tracked issue, never prose or commented-out code (`code-hygiene` §6.1, deferred work is tracked, not commented).

2. **Values and state correctness.**
   - Timestamps cross the API as ISO 8601 with an offset, are stored as UTC, and are never parsed from locale-formatted strings (`code-hygiene` §2.4, date, time, and timezone correctness).
   - Money and exact quantities use decimal types, never floating point, and the server recomputes totals (`code-hygiene` §2.5, money and precise numeric values never use floating point).
   - A value derivable from other state is derived, not stored a second time and kept in sync by hand (`code-hygiene` §2.6, single source of truth for derived state).
   - A fallback value or null-safe operator never turns a missing required value into data that flows downstream as real (`code-hygiene` §2.7, defaults and optional chaining do not hide a meaningful absence).

3. **Dead code and duplication.**
   - Every symbol the change adds has a consumer the change adds, or is a stated entry point (`code-hygiene` §3.2, the change introduces no newly unreferenced code).
   - Logic copied by this change is extracted once; coincidental similarity is left alone (`code-hygiene` §3.3, duplication is consolidated only when it is true duplication).
   - Suspected dead code is traced outward from the target, reported with the scope searched, and never deleted on one clean search (`code-hygiene` §3.1, dead code investigation follows the `refactor-checker` procedure).
   - No unused import, stale registration entry or unused dependency remains (`code-hygiene` §3.4, unused imports, declarations, and dependencies are removed).

4. **Structure and layering.**
   - An operation performed by two or more callers lives once in a shared layer; logic with one caller stays where it is (`code-structure` §2.1, extract only repeated operational logic).
   - Shared code performs no authorization check, user-facing error, status transition or UI decision (`code-structure` §2.2, domain policy stays in the orchestration layer).
   - A shared function takes explicit typed inputs, never a request, response or session object (`code-structure` §2.3, shared functions take explicit typed inputs and return structured results).
   - A shared service is injected, not constructed by its caller (`code-structure` §2.5, shared mechanics are injected, not constructed by the caller).
   - A class with more than one reason to change is split, and the finding names the two concerns; line count is not the criterion (`code-hygiene` §4.1, a class with more than one reason to change is split).
   - An interface, wrapper or layer with one implementation and one caller is a finding unless a second consumer or a test seam is named (`code-hygiene` §4.2, abstractions must earn their existence).

5. **Type safety and constants.**
   - Type-checker strictness is not weakened in code or in configuration: no untyped escape hatch, no unexplained suppression, no loosened compiler setting (`code-hygiene` §5.1, type-checker strictness is not weakened).
   - Status strings, role names, thresholds, intervals and page sizes are named constants shared with their consumers (`code-hygiene` §5.2, domain values are named constants, not literals).

6. **Comments and documentation.**
   - A comment states what the code is and does now, in business language, and stays true if the file's history is deleted: no change history, no optimization contrast, no table, column or query mechanics (`commenting-standards` §2.2, no change history or optimization contrast; §2.3, no storage or query mechanics).
   - No comment uses the banned vocabulary, narrates obvious code or addresses the reader (`commenting-standards` §2.1, banned vocabulary; §2.5, no narration of obvious code; §2.6, no reader-address filler).
   - Each comment fits its type's length limit, and the doc-comment style matches the project's (`commenting-standards` §3.1, each comment type has a length limit; §3.3, documentation-comment style matches the project).
   - A TODO carries a tracked reference (`commenting-standards` §4.2, TODOs only with a tracked reference).

7. **Residue.**
   - No commented-out code, debugger statement, ad hoc console or print output or temporary hard-coded test value; logging goes through the project's logger and never writes a credential, token or personal data (`code-hygiene` §6.2, no commented-out code and no debug residue).
   - Lockfiles, generated clients and build output are not hand-edited (`code-hygiene` §6.3, generated and vendored files are not hand-edited).

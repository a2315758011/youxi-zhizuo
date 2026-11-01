---
name: code-structure
description: Decides where logic belongs when features share mechanics, splitting the orchestration layer (handlers, controllers, container components) from shared services and functions. Use when two or more handlers, services or components duplicate operational logic, or when deciding whether code belongs in a controller or a shared service.
license: MIT
metadata:
  pack: core
---

# Code Structure: Orchestration vs Shared Mechanics

How to split code so that a fix to one operation reaches every flow that uses it. Cite a rule as "code-structure §N.N, <rule title>".

## 1. The Two Layers

| Layer | Where it lives | What it owns |
|---|---|---|
| **Orchestration** | HTTP handlers (controllers, route functions, views), orchestration services, UI container components | What an action *means*: authorization and ownership checks, request validation, status transitions, failure classification, user-facing errors, UI decisions (confirmations, notifications, navigation) |
| **Shared mechanics** | Injectable services, modules, plain functions | *How* to perform an operation reliably: query building, external API and SDK calls, file and PDF generation, notification dispatch, formatting and mapping, calculations, typed HTTP client calls |

**Rule of thumb:** "what this means for the user or the business" stays in orchestration; "how to do this operation reliably" moves to shared mechanics.

The framework pack's guidelines skill covers the framework-specific placement: module registration, provider scope, and where services are declared.

## 2. Rules

### 2.1 Extract Only Repeated Operational Logic
*[universal] · Source: [established industry practice]*

- Extract an operation into the shared layer when two or more callers perform it. Logic with exactly one caller stays where it is.
  - ✅ The same "tasks due in a date range" query used by the task list and the weekly report becomes one shared function.
  - ❌ A new shared service whose only caller is the handler it was extracted from.
- **Verify:** for each shared function or service added in the diff, find at least two call sites. For each operational block the diff adds, search for an existing shared equivalent before accepting a second copy.

### 2.2 Domain Policy Stays in the Orchestration Layer
*[universal] · Source: [established industry practice]*

- Shared mechanics never:
  - perform authorization or ownership checks;
  - raise HTTP-level or user-facing errors;
  - decide status transitions;
  - show dialogs or notifications, or navigate.
- They do the operation and report the outcome. The caller decides what it means.
  - ✅ `invoicePdf.render(invoice)` returns the document bytes; the handler decides who may download it and what to return when rendering fails.
  - ❌ A shared query helper that checks the caller's role or throws a 403.
- **Verify:** search the shared-layer files in the diff for HTTP exception types, role or permission checks, and router, dialog, or notification calls.

### 2.3 Shared Functions Take Explicit Typed Inputs and Return Structured Results
*[universal] · Source: [established industry practice]*

- Pass exactly the data the operation needs, as typed parameters: never the raw request, response, or session object.
- Return typed results: a projection rather than a raw ORM entity when the caller needs a subset, and never a swallowed error.

```ts
// ❌ Reads the request, returns an entity graph
async function dueTasks(req: Request) {
  return this.taskRepository.find({ where: { projectId: req.params.projectId }, relations: ['project', 'assignee'] });
}

// ✅ Explicit inputs, typed projection
async function findDueTasks(projectId: number, range: DateRange): Promise<DueTaskSummary[]> { /* ... */ }
```

```python
# ❌ Reads the request, returns ORM objects
def due_tasks(request):
    return session.scalars(select(Task).where(Task.project_id == request.path_params["project_id"])).all()


# ✅ Explicit inputs, typed projection
def find_due_tasks(project_id: int, date_range: DateRange) -> list[DueTaskSummary]:
    ...
```

- **Verify:** no shared function in the diff takes a request, response, or session parameter. Return types are declared.

### 2.4 One Consistent API Across the Shared Layer
*[universal] · Source: [established industry practice]*

- Methods of one shared service follow the same conventions. Inputs are either typed objects or explicit arguments, not a mix. Errors are either raised or returned as results, not both. Async style is the same throughout.
- **Verify:** compare each new shared method's signature, error handling, and async style with its siblings in the same service or module.

### 2.5 Shared Mechanics Are Injected, Not Constructed by the Caller
*[universal] · Source: [established industry practice — dependency injection]*

- Callers receive shared services through the framework's dependency-injection mechanism (constructor injection, provider registration, or dependency functions), or import plain module-level functions where the stack has no DI.
- A caller never constructs a service itself (`new InvoicePdfService()`). Doing so bypasses configuration and makes the dependency impossible to substitute in tests.
- **Verify:** search the diff for direct construction of service classes outside composition roots and test setup.

### 2.6 Each Endpoint Call on the Client Lives in One Service
*[universal] · Source: [established industry practice]*

- A UI component never builds request URLs or calls the HTTP client directly when the same endpoint is or will be used elsewhere. One client-side service owns the call and its request and response types.
- That service never owns confirmations, notifications, or navigation. Those are UI decisions and stay in the component.
- **Verify:** search component files in the diff for direct HTTP client calls and hand-built endpoint URLs.

### 2.7 Extract Incrementally
*[universal] · Source: [established industry practice — refactoring in small, verified steps]*

1. Write the flow in the orchestration layer first, where its behaviour is clearest.
2. Mark the operational chunks that repeat across callers.
3. Extract only those chunks into the shared layer.
4. Replace one caller, verify it, then replace the remaining callers.
5. Keep domain policy (§2.2) in the orchestration layer throughout.
6. Run the project's type checker, linter, and tests.

- **Verify:** the diff replaces callers of an extracted operation and leaves no stale copy behind. Tests cover at least one migrated caller.

## 3. Anti-Patterns

| Anti-pattern | Problem |
|---|---|
| **God service** | One huge service method hides the whole control flow of a feature |
| **Leaky service** | A shared service checks roles, raises user-facing errors, or changes status fields it should not own (§2.2) |
| **Fat handler** | Query building, PDF generation, or calculations written inline in a controller, route function, or component |
| **Inconsistent API** | Some shared methods take typed objects, others loose arguments or raw entities; error and async semantics differ (§2.4) |
| **Over-abstraction** | A shared service with exactly one caller (§2.1) |
| **Duplicated client calls** | The same endpoint called from several components instead of through one service (§2.6) |

## 4. Mental Model

```
New feature? → Write it in the orchestration layer first
             → Same operational logic in two or more callers?
                 → Extract it to a shared, injected service or module
             → No repetition?
                 → Keep it where it is
```

**In one sentence:** handlers and container components orchestrate domain rules (authorization, validation, status transitions, UI decisions), while injected shared services centralize reusable mechanics behind a consistent, explicitly typed API.

## 5. Related Standards

| Concern | Skill | What it adds |
|---|---|---|
| Is this specific code dead or truly duplicated? | `refactor-checker` | Evidence-based investigation before anything is consolidated or deleted |
| Duplication, god classes, and needless abstraction at the level of a whole change | `code-hygiene` | When duplication is real, when a class has too many reasons to change, when an abstraction earns its place |
| Documenting shared functions | `commenting-standards` | Doc-comment and docstring rules |

## 6. Pre-Commit / Pre-Save Verification Checklist

- [ ] Every new shared function or service has at least two callers (§2.1).
- [ ] No duplicated operational block where a shared equivalent already exists (§2.1).
- [ ] The shared layer performs no authorization, user-facing errors, status transitions, or UI decisions (§2.2).
- [ ] Shared functions take typed inputs (no request, response, or session objects) and declare their return types (§2.3).
- [ ] New shared methods match their siblings' input, error, and async conventions (§2.4).
- [ ] Services are injected, never constructed by callers (§2.5).
- [ ] No UI component calls the HTTP client directly for a shared endpoint (§2.6).
- [ ] Extracted operations have no stale copies left behind (§2.7).

If any item fails, fix it before proceeding — don't leave a partially-compliant structure in place.

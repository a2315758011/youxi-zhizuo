# Framework-specific reference surfaces

A plain import/export graph only sees static `import`/`require` statements. Every framework below adds its own wiring — decorators, templates, routing tables, dependency injection — that creates real usage a text-only search can miss in either direction (something that looks used isn't, or something that looks dead genuinely isn't). Read the section for whatever framework(s) the project actually uses; skip the rest.

**The general principle, for a framework not covered here**: find that framework's own registration/wiring mechanism — a plugin manifest, a routing table, a DI container, a decorator that registers something with a runtime system — and treat it as an additional reference surface alongside plain imports. Most frameworks have *some* place where things get wired up outside of normal `import` statements (a config object, a decorator, a naming convention the framework's runtime uses to auto-discover files); find that place for the framework in front of you before concluding something is unused.

## Angular

- **Components/directives/pipes**: grep for the selector across `.html` files and inline templates — not just as an element tag. A directive selector is often applied as an attribute (`[appHighlight]`) or with a structural prefix (`*appHighlight`); search for the bare name with and without brackets/asterisk.
  - `NgModule.declarations` / standalone `imports` arrays are not evidence of use by themselves — only evidence Angular *could* instantiate it. Still require one of the surfaces below.
  - **Router configs** (`*-routing.module.ts`, `app.routes.ts`, any file with a `Routes` array): `component: SomeComponent` or lazy `loadComponent: () => import('./some.component').then(m => m.SomeComponent)` is real usage even with zero template hits and zero `declarations` entries. This is the single most common false positive for "unused Angular component" — always check route files.
  - **Dynamic instantiation**: `ViewContainerRef.createComponent(SomeComponent)`.
  - **`hostDirectives`** (Angular 15+): a directive applied via `hostDirectives: [SomeDirective]` in another component/directive's decorator, with no selector match anywhere.
- **`@Input()`/`@Output()` and their signal equivalents**: an aliased binding — `@Input('aliasName') propertyName` — means the *template* uses `aliasName`, not the property name; search for whichever is actually bound. The signal-based API (`input()`, `output()`, `model()`, Angular 17+) is functionally the same but won't be caught by a decorator-only search — grep for `= input(`/`= output(`/`= model(`. For `model()` specifically, also check the two-way `[(propName)]="value"` syntax, not just one-way `[propName]=`/`(propName)=`.
- **`NgModule` declarations/imports/exports** that reference an otherwise-unused class are the same finding as the class itself — report together, not separately.
- **Orphaned services**: a `@Injectable()` never named in a constructor parameter, `providers` array, or `inject()` call. Be conservative — `providedIn: 'root'` services can be injected far from where they're declared, so a *local* miss is weaker evidence than for a component.

## NestJS

- **Providers**: grep for the class as a constructor-parameter type or `@Inject(ClassName)` argument — **and** check for custom string/symbol tokens, since Nest supports `{ provide: 'SOME_TOKEN', useClass/useValue/useFactory: ... }` or `useExisting: OtherClass` (aliasing one token to an existing provider), with consumers injecting via `@Inject('SOME_TOKEN')`. The class name may never appear as an injection site anywhere despite being fully in use.
- **Dynamically-registered providers** (`forFeature()`/`forRoot()`/`forRootAsync()`): libraries like TypeORM register providers via `TypeOrmModule.forFeature([User])`, consumed via `@InjectRepository(User)` — the provider is synthesized at runtime under a generated token, so `User` never shows up as a constructor-parameter type. Grep for the class as an argument to `forFeature(`/`forRoot(` and to library-specific injection decorators (`@InjectRepository`, `@InjectModel`, etc.) before flagging an entity/model class as unused.
- **Controllers**: not registered in any module's `controllers` array → genuinely dead, Nest won't wire up its routes. This is a structural fact, not a judgment call — safe to call high confidence.
- **Modules**: not imported anywhere and not the bootstrap root → likely dead — **except** `@Global()` modules, whose providers are available everywhere without further imports by design. Check for `@Global()` before flagging a module as orphaned.
- **Guards/interceptors/pipes/filters**: check `@UseGuards()`/`@UseInterceptors()`/`@UsePipes()`/`@UseFilters()` decorator arguments, `APP_GUARD`/`APP_INTERCEPTOR`/`APP_PIPE`/`APP_FILTER` provider registrations, **and** `main.ts` for global registration via `app.useGlobalGuards()`/`app.useGlobalInterceptors()`/`app.useGlobalPipes()`/`app.useGlobalFilters()` — bootstrap-level registration is common and easy to miss if only checking decorators.
- **DTOs**: a class not referenced as a type anywhere is a weaker finding than the others above — DTOs are sometimes kept deliberately for API-contract documentation or Swagger decorators. Default this to "needs review," not high confidence.

## React

- **Components**: grep for JSX usage (`<ComponentName`), `React.createElement(ComponentName`, and lazy-loaded usage via `React.lazy(() => import('./ComponentName'))` or a router's lazy-loading equivalent (e.g. React Router's `lazy: () => import(...)` route property). A component only ever rendered through a route config or a dynamic component map/registry (`{ home: HomeComponent, about: AboutComponent }` looked up by key) will show zero JSX hits and isn't actually dead — check route/registry definitions specifically before concluding it's unused.
- **Custom hooks**: grep for the hook being called (`useSomething(`) rather than just imported — a hook imported but never invoked is a stronger dead-code signal than one that's merely unexported.
- **Context**: `SomeContext.Provider` and `useContext(SomeContext)` (or a custom hook wrapping `useContext`) are both real usage; a context defined but never consumed via either form is a genuine candidate.
- **Higher-order components and render-prop patterns**: a component passed into `withSomething(Component)` or used as `<DataProvider render={...}>` won't show up as plain JSX usage of the wrapped component — check the HOC/wrapper's call sites too.
- **Connected/store-wired components** (Redux `connect(...)(Component)`, or a store's slice/reducer referenced only from the store's own configuration file): the component or reducer can look unused via plain import search if its only "reference" is inside a store-configuration object rather than a normal import elsewhere — check store/slice registration files specifically.
- **Barrel exports**: React component libraries commonly re-export through an `index.ts` — the same blind spot as `ts-prune`'s barrel limitation applies; corroborate with a project-wide grep for the component name, not just the barrel file's own export list.
- **Bundler globs**: Vite's `import.meta.glob('./widgets/*.tsx')` and webpack's `require.context(...)` load whole directories without naming any file. Check for them before flagging a file in such a directory.

### Next.js

- **File-based routing is usage.** Nothing imports these files, and Next.js loads every one by its path and name:
  - **App Router**, anywhere under `app/`: `page`, `layout`, `template`, `loading`, `error`, `not-found`, `default` and `route` files.
  - **Pages Router**: any file under `pages/`, including `pages/api/`.
  - **Root files**: `middleware.ts` and `instrumentation.ts`.
- **Special exports are read by the framework:** `metadata`, `generateMetadata`, `generateStaticParams`, `revalidate`, `dynamic`, `runtime`, and (Pages Router) `getServerSideProps`, `getStaticProps`, `getStaticPaths`. An unreferenced export with one of these names in a route file is not dead.
- **Server Actions** (`'use server'` functions) are often referenced only as a form's `action={createTask}` or passed to a client component as a prop. Search for the function name in JSX attributes, not only in import lines.

## FastAPI

- **Routers**: a route function decorated with `@router.get(...)`/`@app.post(...)` is reachable only if its `APIRouter` is passed to `app.include_router(...)` (directly or through a parent router). A router module never included is structurally dead — high confidence, like an unregistered NestJS controller. An included router's route functions are live even with zero call sites.
- **Dependencies**: a function used only as `Depends(get_current_member)` or `Security(...)` in parameter defaults or in `dependencies=[...]` is live. Search for the bare function name inside `Depends(` and `Security(`, not only for calls. `app.dependency_overrides[...]` in tests references the same functions.
- **App wiring outside routes**: `lifespan` passed to `FastAPI(lifespan=...)`, `@app.on_event(...)` handlers, `@app.exception_handler(...)` and `app.add_exception_handler(...)`, `@app.middleware("http")` and `app.add_middleware(...)`, and `app.mount(...)` all register code that nothing calls directly. Check the application factory and `main.py`.
- **Pydantic models** used only as a parameter annotation (a request body), in `response_model=`, or in `responses={...}` are live. Validators (`@field_validator`, `@model_validator`, and v1's `@validator`/`@root_validator`) are invoked by Pydantic itself — never flag them as unused.
- **SQLAlchemy models** register themselves on `Base.metadata` when imported. A model imported only for that side effect (in `models/__init__.py` or Alembic's `env.py` via `target_metadata`) still defines a table that migrations depend on. Relationships can name a model by string, as in `relationship("Task")`. Default an unqueried model to "needs review".
- **Alembic revisions** under `versions/` are loaded by Alembic through their revision chain. Never flag them.

## Python (any project)

- **Package surface**: names re-exported from `__init__.py` or listed in `__all__` are public API; treat them like a barrel file.
- **Entry points**: `[project.scripts]`, `[project.entry-points]` (and `setup.py`'s `entry_points`), and modules run as `python -m package.module` or guarded by `if __name__ == "__main__":`.
- **Pytest**: fixtures are used by **parameter name**, not by import. Search test files for the fixture name as a test-function parameter, check `conftest.py` files up the directory tree, and remember `autouse=True` fixtures and `pytest_plugins` lists apply without being named at all.
- **Decorator registries**: task queues (`@shared_task`, `@app.task`, called elsewhere by a string name), CLI frameworks (`@cli.command()`), signal and event receivers, and plugin hooks register functions that nothing calls directly.
- **Runtime-invoked members**: dunder methods (`__eq__`, `__hash__`, `__repr__`, `__enter__`/`__exit__`), `@property` accessors, and methods implementing an abstract base class or `Protocol` are called by the interpreter or the framework.
- **String-based access**: `getattr(obj, name)`, `importlib.import_module(path)`, and settings that name classes by dotted path (`"app.storage.S3Storage"`) — search for the name as a string, not only as an identifier.
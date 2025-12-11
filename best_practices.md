# 📘 Project Best Practices

## 1. Project Purpose
This repository contains multiple Python projects and examples. The primary substantial application is a Flask-based payroll/staff management app under `flask_project/peyroll`. It includes authentication, staff/department management, templates, and a SQLite-backed persistence layer. There are also several smaller scripts and modules (e.g., generators, CLI tools, examples) which are independent and serve as learning utilities.

## 2. Project Structure
- `/flask_project/`
  - `app.py`: Flask entrypoint (may delegate to the peyroll app factory)
  - `peyroll/`: Main application package
    - `__init__.py`: Flask app factory (`create_app`), blueprint registration, config loading, and DB init
    - `database.py`: DB connection and initialization helpers; CLI command `init-db`
    - `auth.py`: Authentication blueprint (login, register, logout, auth helpers)
    - `staff.py`: Staff CRUD blueprint (create, update, delete, list)
    - `departments.py`, `pages.py`: Pages/Departments blueprints and routes
    - `templates/`: Jinja templates organized by feature folders (auth, pages, staff)
    - `schema.sql`: Database schema used to initialize SQLite DB
    - `instance/`: Contains the SQLite database when running locally
  - `tests/`: Pytest suite for the Flask app (auth tests, fixtures, etc.)

- Other top-level folders (e.g., `files_monitor/`, `todo_project/`, `generator/`, `contacts/`, etc.) are separate experiments/apps with their own structures and purposes.

Key conventions:
- Blueprints for modular route organization
- App factory pattern for testability and configuration flexibility
- SQLite via `database.py` with `get_db()` and schema initialization

## 3. Test Strategy
- Framework: `pytest`
- Location: `flask_project/tests/`
  - `conftest.py`: Provides app/client fixtures, sets up a temporary SQLite database, and loads schema
  - `test_auth.py`: Covers registration, login, next-parameter handling, rate limiter logic, and logout
- Philosophy:
  - Prefer black-box tests via Flask test client
  - Use a temp DB and load `schema.sql` for integration-style tests
  - Keep tests idempotent and isolated (fresh DB per test session or per test where necessary)
- Mocking:
  - Favor real DB with temp files for CRUD flows; use mocks only where external services exist (currently none)
- Naming:
  - Test files start with `test_*.py`; test functions describe the behavior under test

## 4. Code Style
- Python 3.x, Flask idioms, Jinja templates
- Naming:
  - Modules: `snake_case.py`
  - Functions/variables: `snake_case`
  - Blueprints: module-level `bp`
- Docstrings/comments:
  - Prefer docstrings for modules like `database.py`
  - Add concise comments for non-obvious logic
- Imports:
  - Absolute or package-relative imports; avoid extra spaces and keep ordering logical (stdlib, third-party, local)
- Error/exception handling:
  - Wrap DB writes (INSERT/UPDATE/DELETE) in `try/except` and log with context
  - Return user-friendly flash messages with categories (`'error'`, `'success'`, `'warning'`)
- Security:
  - Use `login_required` decorator for protected routes
  - Avoid user enumeration by using generic auth error messages
  - Validate and normalize form inputs; use safe parsing helpers
  - Use CSRF protection (Flask-WTF recommended). Current code includes scaffolding; ensure templates include tokens.
- Formatting & Style:
  - 4 spaces for indentation; avoid tabs
  - Keep lines readable; follow PEP8 where applicable

## 5. Common Patterns
- App Factory Pattern:
  - `create_app()` builds the Flask instance with config, registers blueprints, and initializes DB
- Blueprint-based modularization:
  - `auth`, `staff`, `pages`, `departments` split responsibilities by domain
- Request lifecycle helpers:
  - `@bp.before_app_request` to load user from session and to ensure CSRF token exists
- Decorators:
  - `login_required` to guard routes and propagate `next` parameter for post-login redirects
- Validation utilities:
  - Safe parsing helpers for ints/floats; password validation in auth; FK validation for staff CRUD

## 6. Do's and Don'ts
- ✅ Do
  - Use the app factory to create configured app instances in production and tests
  - Register blueprints in `__init__.py` to keep routes modular
  - Initialize the DB from `schema.sql` and keep migrations scripted/automated when schema evolves
  - Validate all user inputs; normalize and enforce constraints server-side
  - Use flash categories and render them in templates for consistent UX
  - Protect state-changing routes with `login_required` and CSRF
  - Log failures and important actions with appropriate levels (info, warning, error)
  - Add tests for new routes, validation paths, and security/redirect flows

- ❌ Don't
  - Hard-code business identifiers (e.g., role IDs); query the DB instead
  - Expose sensitive routes without authentication if not explicitly intended
  - Return differing login errors that reveal account existence
  - Parse form fields with raw `int()`/`float()` without validation
  - Swallow exceptions silently; always log with context

## 7. Tools & Dependencies
- Flask: Web framework (blueprints, routing, request/response handling)
- SQLite3: Embedded database for local development/testing
- Click: CLI commands for DB initialization (`flask init-db`)
- Werkzeug: Security helpers (password hashing/verification)
- Pytest: Testing framework and fixtures
- Optional/Recommended:
  - Flask-WTF: CSRF protection and form handling
  - Flask-Limiter: Rate limiting for authentication endpoints
  - Black/Flake8/isort: Formatting and linting for consistent style

Setup:
- Create and configure the app via `create_app()` in `peyroll/__init__.py`
- Initialize the DB:
  - `export FLASK_APP=flask_project/peyroll`
  - `flask init-db`
- Run tests: `pytest -q`

## 8. Other Notes
- Templates should render flash messages with category awareness and include CSRF tokens in forms:
  ```html
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for category, message in messages %}
        <div class="flash {{ category }}">{{ message }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  ```
- The `auth` blueprint supports `next` for redirects; ensure any links to protected routes correctly propagate `next` when redirecting to `/auth/login`.
- When adding new blueprints, follow the established structure: create a module, define `bp`, add routes, and register in `create_app()`.
- Keep schema changes in sync with `schema.sql` and consider adopting a migration tool (Alembic/Flask-Migrate) as the project grows.

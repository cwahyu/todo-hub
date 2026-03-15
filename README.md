# todo-hub

`todo-hub` is a lightweight CLI tool that aggregates TODO tasks across multiple projects and presents them as a deadline-focused agenda.

It scans `TODO.md` files from different repositories and shows tasks grouped by urgency with a clean, colorized terminal view.

Perfect for developers managing many small projects.

## Features

- Scan TODO files across multiple projects
- Parse tasks written as Markdown checkboxes
- Detect deadlines using `@YYYY-MM-DD`
- Group tasks by urgency:
  - **Overdue**
  - **This week**
  - **Later**
  - **Unscheduled**
- Agenda-style weekly view
- Colorized terminal output
- Deterministic color for each project
- Simple configuration via `config.toml`
- Fast and dependency-light
- High test coverage (~88%)

## Installation

### Recommended (using pipx)

`pipx` installs CLI tools in isolated environments and makes them available globally.

```bash
pipx install todo-hub
```

Then run:

```
todo-hub
```

If pipx is not installed:

```
python -m pip install --user pipx
pipx ensurepath
```

### Using pip

You can also install with pip, although pipx is recommended for CLI tools.

```
pip install todo-hub
```

### Development Installation

For development or testing from the repository:

```
git clone https://github.com/cwahyu/todo-hub.git
cd todo-hub

pipx install -e .
```

## Usage

Run:

```
todo-hub
```

Example output:

```
Overdue:
  - [ ] fix parser @2026-03-10 (-4d) #mudita

This week:
  Today
  - [ ] finish CLI @2026-03-14 (0d) #todo-hub
  Tomorrow
  - [ ] improve parser @2026-03-15 (1d) #mudita
  Mar 16
  - [ ] refactor scanner @2026-03-16 (2d) #todo-hub

Later:
  - [ ] redesign module @2026-03-25 (11d) #todo-hub

Unscheduled:
  - [ ] research API #blog
```

## TODO Format

`todo-hub` scans Markdown files named:

```
TODO.md
todo.md
```

Tasks must follow this format:

```
- [ ] implement feature @2026-04-01
```

Deadline syntax:

```
@YYYY-MM-DD
```

Examples:

```
- [ ] finish CLI @2026-03-20
- [ ] refactor parser @2026-03-21
- [ ] improve documentation
```

Completed tasks are ignored:

```
- [x] finished task
```

## Configuration

Projects are defined in config.toml.

Example:

```
[[project]]
name = "mudita"
path = "~/projects/mudita"

[[project]]
name = "todo-hub"
path = "~/projects/todo-hub"
```

Each project path will be scanned recursively for TODO.md.

## Project Structure

```
todo-hub/
├── src/
│   └── todohub/
│       ├── main.py
│       ├── config.py
│       ├── scanner.py
│       ├── parser.py
│       ├── scheduler.py
│       ├── presenter.py
│       └── models.py
├── tests/
├── pyproject.toml
└── README.md
```

Architecture pipeline:

```
config → scan → parse → schedule → present
```

## Development

Install dependencies:

```
poetry install
```

Run the CLI:

```
poetry run todo-hub
```

Run tests:

```
pytest
```

Test coverage:

```
Required test coverage: 85%
Current coverage: ~88%
```

## Why todo-hub?

Many developers maintain multiple repositories with scattered TODO lists.

`todo-hub` provides a **single unified view of upcoming work** across all projects.

Instead of searching through repositories, you can simply run:

```
todo-hub
```

and immediately see what needs attention.

## Philosophy

`todo-hub` is designed around a few simple principles.

### Deadlines over task lists

Most TODO tools focus on managing tasks inside a single project.

`todo-hub` focuses on **deadlines across projects**.

The goal is to answer one question quickly:

> *What needs my attention today?*

Instead of browsing multiple repositories, `todo-hub` aggregates tasks into a single agenda-style view.

### Plain text first

Tasks are stored in simple Markdown files:

```
TODO.md
```

This keeps the workflow:

- transparent
- version-controlled
- editor-friendly
- portable across tools

No databases, no lock-in.

### Minimal syntax

`todo-hub` only requires two simple conventions:

```
task description @YYYY-MM-DD
```

Example:

```
implement CLI @2026-03-20
```

Everything else is optional.

### Works with existing repositories

`todo-hub` does not require special project setup.

It simply scans for:

```
TODO.md
todo.md
```

in configured project folders.

This makes it easy to adopt gradually across existing repositories.

### Fast feedback

The tool is designed for a quick daily check:

```
todo-hub
```

Output is grouped by urgency:

```
Overdue
This week
Later
Unscheduled
```

This makes it easy to see what requires attention immediately.

### Terminal-first workflow

`todo-hub` is designed for a simple, distraction-free terminal workflow.

Instead of interactive dashboards or complex interfaces, it produces clean,
linear output that can be scanned quickly in a terminal window.

The focus is on clarity and speed:

- fast startup
- minimal dependencies
- readable, plain-text output
- color used only to highlight urgency

The goal is to make it easy to run:

```
todo-hub
```

and immediately see what needs attention today.

### Small and maintainable

The project architecture is intentionally minimal:

```
config → scan → parse → schedule → present
```

Each module has a single responsibility, making the codebase easy to understand and extend.

## **License**

MIT License

# todo-hub

`todo-hub` is a lightweight CLI tool that aggregates TODO tasks across multiple projects and presents them as a deadline-focused agenda.

It scans `TODO.md` files from different repositories and shows tasks grouped by urgency in a clean, colorized terminal view.

Ideal for developers managing many small projects.

## Features

- Scan TODO files across multiple projects
- Parse Markdown checkbox tasks
- Detect deadlines using `@YYYY-MM-DD`
- Optional priority tags: `!high`, `!medium`, `!low`
- Support nested tasks (parent tasks are ignored)
- Agenda-style weekly view
- Deterministic color per project
- Simple `config.toml` configuration
- Fast and dependency-light

## Installation

### Recommended (pipx)

`pipx` installs CLI tools in isolated environments.
```bash
pipx install todo-hub
```

Run:
```
todo-hub
```

If `pipx` is not installed:
```
python -m pip install --user pipx
pipx ensurepath
```

### Using pip

```
pip install todo-hub
```

### Development install

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

Later:
  - [ ] redesign module @2026-03-25 (11d) #todo-hub

Unscheduled:
  - [ ] research API #blog
```

## Additional commands:

```
todo-hub today
todo-hub week
todo-hub projects
todo-hub doctor
```

## TODO Format

`todo-hub` scans Markdown files named:
```
TODO.md
todo.md
```

Tasks use Markdown checkboxes:
```
- [ ] task description
```

Optional metadata:
```
@YYYY-MM-DD     deadline
!high           priority
!medium
!low
```

Examples:
```
- [ ] ￼implement CLI @2026-03-20
- [ ] ￼fix production bug !high @2026-03-16
- [ ] ￼improve documentation
```

Nested tasks are supported:
```
- [ ] version 0.3.0
  - [ ] support indented tasks
  - [ ] priority tags !medium
```

Parent tasks without deadlines are ignored.

Completed tasks are skipped:
```
- [x] finished task
```

## Configuration

Projects are defined in `config.toml`.

Example:
```
[[project]]
name = "mudita"
path = "~/projects/mudita"

[[project]]
name = "todo-hub"
path = "~/projects/todo-hub"
```

Each project directory is scanned recursively for TODO files.

## Philosophy

`todo-hub` is designed around a few simple principles.

### Deadlines over task lists

Most task tools focus on managing tasks inside a single project.

`todo-hub` focuses on deadlines across projects.

The goal is to answer one question quickly:

>What needs my attention today?

### Plain text first

Tasks live in simple Markdown files:
```
TODO.md
```

This keeps the workflow:
- transparent
- version-controlled
- editor-friendly
- portable

No databases, no lock-in.

### Terminal-first workflow

`todo-hub` is intentionally simple and optimized for terminal use:
- fast startup
- minimal dependencies
- readable CLI output
- color used only to highlight urgency

Run:
```
todo-hub
```

and immediately see what needs attention.

### Small and maintainable

The architecture is intentionally minimal:
```
config → scan → parse → schedule → present
```

Each module has a single responsibility.

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

## License

MIT License

# todo-hub

`todo-hub` is a lightweight CLI tool that aggregates TODO tasks across multiple
projects and presents them as a deadline-focused agenda.

It scans `TODO.md` files from different repositories and shows tasks grouped by
urgency in a clean, colorized terminal view.

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

```bash
todo-hub
```

If `pipx` is not installed:

```bash
python -m pip install --user pipx
pipx ensurepath
```

### Using pip

```bash
pip install todo-hub
```

### Development install

```bash
git clone https://github.com/cwahyu/todo-hub.git
cd todo-hub
pipx install -e .
```

## Usage

Run:

```bash
todo-hub
```

Example output:

```text
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

## Additional commands

```bash
todo-hub today
todo-hub week
todo-hub projects
todo-hub doctor
```

## TODO Format

`todo-hub` scans Markdown files named:

```text
TODO.md
todo.md
```

Tasks use Markdown checkboxes:

```text
- [ ] task description
```

Optional metadata:

```text
@YYYY-MM-DD     deadline
!high           priority
!medium
!low
```

Examples:

```text
- [ ] implement CLI @2026-03-20
- [ ] fix production bug !high @2026-03-16
- [ ] improve documentation
```

Nested tasks are supported:

```text
- [ ] version 0.3.0
  - [ ] support indented tasks
  - [ ] priority tags !medium
```

Parent tasks without deadlines are ignored.

Completed tasks are skipped:

```text
- [x] finished task
```

## Configuration

Projects are defined in `config.toml`.

Example:

```toml
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

```text
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

```bash
todo-hub
```

and immediately see what needs attention.

### Small and maintainable

The architecture is intentionally minimal:

```text
config → scan → parse → schedule → present
```

Each module has a single responsibility.

## Development

Install dependencies:

```bash
uv sync --extra dev
```

Run the CLI:

```bash
uv run todo-hub
```

Run tests:

```bash
uv run pytest
```

## License

MIT License

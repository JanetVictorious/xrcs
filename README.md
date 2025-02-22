# 🏋️ xrcs (Exercise)

A minimalist, open-source training app built with Python and Kivy for tracking workouts and exercises.

## Features

- Create and manage your user profile
- Log workouts with exercises, sets, reps, and weights
- View workout history
- Track exercise history
- Simple and intuitive UI

## Installation

See the [contributing](./CONTRIBUTING.md#create-a-pull-request) guide step 1-4 on how to fork the repository and set up a working environment.

## Usage

Run the application:
```bash
make run
```

For debug mode:
```bash
make run-debug
```

## Development

This project uses several development tools:

- [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [MyPy](https://mypy.readthedocs.io/) for static type checking
- [Pylint](https://pylint.readthedocs.io/) for code analysis
- [Pre-commit](https://pre-commit.com/) for git hooks

Install development hooks:
```bash
make pre-commit-install
```

Run code checks:
```bash
make pre-commit
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](./LICENSE) file for details.

# xrcs (Exercise)

A minimalist, open-source training app built with Python and Kivy for tracking workouts and exercises.

## Features

- Create and manage your user profile
- Log workouts with exercises, sets, reps, and weights
- View workout history
- Track exercise history
- Simple and intuitive UI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/xrcs.git
cd xrcs
```

2. Set up a virtual environment and install dependencies:
```bash
make setup-venv
```

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

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run pre-commit checks (`make pre-commit`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](./LICENSE) file for details.

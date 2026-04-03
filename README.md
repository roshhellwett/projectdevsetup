# projectdevsetup

Automatic developer environment setup for beginners.

`projectdevsetup` is a beginner-friendly Python package that helps new developers prepare a coding environment for Python, C, C++, Java, HTML/CSS, JavaScript, Rust, and Go. It checks for connectivity, installs the selected tooling when possible, prepares starter files, and can open the result in VS Code.

## Installation

```bash
pip install projectdevsetup
```

You can then launch it with either:

```bash
projectdevsetup
```

or:

```bash
python -m projectdevsetup
```

## What it does

- Asks which language you want to set up.
- Installs the matching beginner tools when automation is supported.
- Installs or opens Visual Studio Code setup guidance.
- Creates starter files in `~/projectdevsetup_projects/<name>`.
- Creates a Python virtual environment and `requirements.txt` for Python projects.

## Supported languages

1. Python
2. C
3. C++
4. Java
5. HTML / CSS
6. JavaScript
7. Rust
8. Go
9. All languages

## Development

Run the test suite from the repository root with:

```bash
$env:PYTHONPATH="src"
python -m unittest discover -s tests
```

Build release artifacts with:

```bash
python setup.py sdist bdist_wheel
```

## Release checklist

- `python -m unittest discover -s tests`
- `python setup.py sdist bdist_wheel`
- Verify `dist/` contains both a source archive and a wheel
- Test install from the wheel in a clean environment

## License

MIT

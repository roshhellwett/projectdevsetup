# Contributing to projectdevsetup

Thank you for contributing to `projectdevsetup`.

This project is intended to help beginners set up a programming environment with less confusion and less manual work, so contributor changes should keep the experience simple, safe, and easy to understand.

## Goals for contributions

When contributing, please keep these goals in mind:

- Prefer beginner-friendly behavior and messages
- Avoid surprising or destructive system changes
- Keep installation steps as clear and reliable as possible
- Make failures understandable when automatic setup cannot continue
- Preserve cross-platform support where possible

## Project structure

Main package source:

- [`src/projectdevsetup`](/D:/projectdevsetup/src/projectdevsetup)

Important modules:

- [`src/projectdevsetup/wizard.py`](/D:/projectdevsetup/src/projectdevsetup/wizard.py)
  Interactive user flow
- [`src/projectdevsetup/installer.py`](/D:/projectdevsetup/src/projectdevsetup/installer.py)
  Language tool installation logic
- [`src/projectdevsetup/vscode.py`](/D:/projectdevsetup/src/projectdevsetup/vscode.py)
  VS Code installation and extension setup
- [`src/projectdevsetup/network.py`](/D:/projectdevsetup/src/projectdevsetup/network.py)
  Connectivity and download helpers
- [`src/projectdevsetup/permissions.py`](/D:/projectdevsetup/src/projectdevsetup/permissions.py)
  Permission and disk-space checks
- [`src/projectdevsetup/templates`](/D:/projectdevsetup/src/projectdevsetup/templates)
  Starter files created for users

Tests:

- [`tests`](/D:/projectdevsetup/tests)

## Development setup

### 1. Clone the repository

```bash
git clone https://github.com/zenith-open-source/projectdevsetup.git
cd projectdevsetup
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the package in editable mode

```bash
pip install -e .
```

## Running tests

From the repository root:

```bash
$env:PYTHONPATH="src"
python -m unittest discover -s tests
```

If you are on macOS or Linux:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Building release artifacts

To build the source distribution and wheel:

```bash
python setup.py sdist bdist_wheel
```

Expected output:

- [`dist/projectdevsetup-<version>.tar.gz`](/D:/projectdevsetup/dist)
- [`dist/projectdevsetup-<version>-py3-none-any.whl`](/D:/projectdevsetup/dist)

## What to test before opening a pull request

Please check as many of these as possible:

1. Unit tests pass
2. The package builds successfully
3. The CLI starts without a traceback
4. User-facing text is clear and beginner-friendly
5. New behavior has tests when practical
6. README or docs are updated when behavior changes

## Contributor guidelines

- Keep messages plain and friendly
- Avoid exposing raw exceptions to end users unless truly necessary
- Prefer safe fallbacks when automatic installation is not possible
- Keep changes focused and easy to review
- Do not add unnecessary dependencies
- Do not remove beginner-friendly behavior for the sake of cleverness

## Good contribution ideas

- Fix installation bugs on supported platforms
- Improve beginner-facing messages
- Add tests for setup flows and failure cases
- Improve README and contributor documentation
- Improve starter templates
- Improve reliability of detection and fallback behavior

## Pull request checklist

Before opening a pull request, please make sure:

- The code is working locally
- Tests pass
- Docs are updated if needed
- The change is small enough to review clearly
- The PR description explains what changed and why

## Reporting bugs

When reporting a bug, please include:

- Your operating system
- Python version
- The command you ran
- What you expected to happen
- What actually happened
- Any visible error message

## Code of conduct

Please be respectful and constructive.

This project exists to help beginners, so contributor discussions should also stay welcoming and patient.

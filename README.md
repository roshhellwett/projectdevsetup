![Repo Size](https://img.shields.io/github/repo-size/roshhellwett/projectdevsetup?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/roshhellwett/projectdevsetup?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/roshhellwett/projectdevsetup?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/roshhellwett/projectdevsetup?style=for-the-badge)
![Dev Setup](https://img.shields.io/badge/DevSetup-0A0A0A?style=for-the-badge&logo=linux&logoColor=white)

# PROJECT DEV SETUP

Beginner-friendly tool that sets up a coding environment for common programming languages. It is designed for people who want a guided setup experience instead of manually installing everything one by one.

![SAMPLEZERO](https://github.com/roshhellwett/projectdevsetup/blob/eaa8b3766acf15159386acfad8387925b0d3eb3e/sample/samplezero.png)

![SAMPLEONE](https://github.com/roshhellwett/projectdevsetup/blob/eaa8b3766acf15159386acfad8387925b0d3eb3e/sample/sampleone.png)

![SAMPLETWO](https://github.com/roshhellwett/projectdevsetup/blob/eaa8b3766acf15159386acfad8387925b0d3eb3e/sample/samplethree.png)

---

## What it does

The tool installs the language toolchain, sets up Visual Studio Code, and installs the recommended VS Code extensions — all in one guided flow. 

LINK - [ProjectDevSetup](https://www.piwheels.org/project/projectdevsetup/)


## Supported languages

1. Python
2. C
3. C++
4. Java
5. HTML / CSS
6. JavaScript
7. Rust
8. Go
9. All languages (installs everything)

## Installation

First, make sure Python is installed.

Then install the package with:

```bash
pip install projectdevsetup
```

## How to run it

You can start it with either command:

```bash
projectdevsetup
```

or:

```bash
python -m projectdevsetup
```

## How to use it

### 1. Start the tool

Run one of the commands above in your terminal.

### 2. Pick a language

The tool will show a menu like this:

```text
============================================================
  projectdevsetup - Zenith Open Source Projects
  Automatic Developer Environment Setup for Beginners
============================================================

  Which programming language do you want to set up?

  1. Python
  2. C
  3. C++
  4. Java
  5. HTML / CSS
  6. JavaScript
  7. Rust
  8. Go
  9. All Languages
```

Enter a number from `1` to `9`.

### 3. Let the setup finish

The tool then goes through these steps:

1. Installs the selected language tools
2. Sets up Visual Studio Code
3. Installs recommended VS Code extensions

### 4. Start coding

Once setup completes, open VS Code and start writing code in your chosen language.

## Important notes

- The tool needs internet access to install packages and editors.
- Some installs may require administrator or sudo permissions.
- Installation success depends on the operating system and external installers being available.
- If VS Code or a language tool cannot be installed automatically, the tool shows a manual fallback message.

## Development and testing

Run tests from the repository root with:

```bash
$env:PYTHONPATH="src"
python -m pytest tests/ -v
```

If you are on macOS or Linux:

```bash
PYTHONPATH=src python -m pytest tests/ -v
```

Build release artifacts with:

```bash
python -m build
```

---

© 2026 [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app/). All Rights Reserved. Zenith is a Open Source Project Idea's by @roshhellwett

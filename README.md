# PROJECT DEV SETUP

 Beginner-friendly tool that helps set up a coding environment for common programming languages. It is designed for people who want a guided setup experience instead of manually installing everything one by one.

---

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

### 3. Name your starter file

If you choose a single language, the tool asks for a file name.

Example:

```text
What do you want to name your file? (without extension)
Example: if you type 'hello', your file will be 'hello.py'
```

If your name contains special characters, the tool replaces them with underscores.

### 4. Let the setup finish

The tool then goes through these steps:

1. Installs the selected language tools
2. Sets up Visual Studio Code
3. Installs recommended VS Code extensions
4. Creates your starter file

For Python, it also creates:

- `.venv`
- `requirements.txt`

### 5. Open your project

Your project is created in:

```text
~/projectdevsetup_projects/<your-file-name>
```

On Windows, that is usually under your user home directory.

## Example output

For a Python project named `hello`, the tool will create something like:

```text
projectdevsetup_projects/
  hello/
    hello.py
    requirements.txt
    .venv/
```

## How to run your code later

### Python

```bash
python hello.py
```

### C

```bash
gcc hello.c -o program
./program
```

### C++

```bash
g++ hello.cpp -o program
./program
```

### Java

```bash
javac Hello.java
java Hello
```

### JavaScript

```bash
node hello.js
```

### Rust

```bash
rustc hello.rs
./hello
```

### Go

```bash
go run hello.go
```

### HTML / CSS

Open the generated HTML file in your browser or in VS Code.

## Important notes

- The tool needs internet access to install packages and editors.
- Some installs may require administrator or sudo permissions.
- Installation success depends on the operating system and external installers being available.
- If VS Code or a language tool cannot be installed automatically, the tool shows a manual fallback message.

## Development and testing

Run tests from the repository root with:

```bash
$env:PYTHONPATH="src"
python -m unittest discover -s tests
```

Build release artifacts with:

```bash
python setup.py sdist bdist_wheel
```

---

© 2026 [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app/). All Rights Reserved. Zenith is a Open Source Project Idea's by @roshhellwett

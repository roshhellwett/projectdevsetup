# projectdevsetup

**Automatic Developer Environment Setup for Beginners**

Made with love by [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app)

---

## What is projectdevsetup?

projectdevsetup is a beginner-friendly tool that automatically sets up your computer for coding. You don't need to know anything about programming or technical stuff - just run the tool and it will:

- Ask you which programming language you want to learn
- Install all the necessary software for that language
- Install Visual Studio Code (a code editor)
- Install helpful extensions for your language
- Create a starter file with example code
- Open everything ready for you to start coding!

---

## Who is this for?

**Complete beginners** who have never written a single line of code. You don't need to know:
- What a compiler is
- What PATH means
- How to install software
- Any technical jargon

If you can use a web browser and type on a keyboard, you can use this!

---

## Supported Programming Languages

| # | Language | What it can do |
|---|----------|---------------|
| 1 | **Python** | Websites, games, AI, data science |
| 2 | **C** | System programs, hardware programming |
| 3 | **C++** | Games, high-performance applications |
| 4 | **Java** | Android apps, enterprise software |
| 5 | **HTML/CSS** | Build websites |
| 6 | **JavaScript** | Websites, web apps |
| 7 | **Rust** | Safe and fast software |
| 8 | **Go** | Servers and cloud applications |

---

## Installation

### Step 1: Install Python (if not already installed)

Before installing projectdevsetup, you need Python on your computer.

**For Windows:**
1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.12"
3. Run the installer
4. **Important**: Check the box "Add Python to PATH"
5. Click "Install Now"

**For Mac:**
1. Open Terminal (press Cmd+Space, type "Terminal")
2. Type: `brew install python3`
3. Press Enter

**For Linux:**
1. Open Terminal
2. Type: `sudo apt update` then `sudo apt install python3`
3. Press Enter

### Step 2: Install projectdevsetup

Open your terminal/command prompt and type:

```bash
pip install projectdevsetup
```

Wait for it to install. That's it!

---

## How to Use

### Step 1: Run the tool

In your terminal, type:

```bash
python -m projectdevsetup
```

### Step 2: Follow the instructions

The tool will ask you questions. Here's what to expect:

```
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

>>  Enter a number (1-9):
```

**Type the number** of the language you want to learn and press Enter.

### Step 3: Name your file

```
What do you want to name your file? (without extension)
Example: if you type 'hello', your file will be 'hello.py'

>>  File name:
```

**Type a name** for your first file (like "hello" or "myfirstprogram") and press Enter.

### Step 4: Wait for installation

The tool will:
1. Check your internet connection
2. Install the programming language
3. Install Visual Studio Code
4. Install helpful extensions
5. Create your starter file

This may take a few minutes. Don't worry - it will tell you when it's done!

### Step 5: Start coding!

When it's done, Visual Studio Code will open with your file. You can start editing and running your code!

---

## How to Run Your Code

After the tool creates your file, here's how to run it:

### Python
```bash
python yourfilename.py
```

### C
```bash
gcc yourfilename.c -o program
./program
```

### C++
```bash
g++ yourfilename.cpp -o program
./program
```

### Java
```bash
javac YourFilename.java
java YourFilename
```

### JavaScript
```bash
node yourfilename.js
```

### Rust
```bash
rustc yourfilename.rs
./yourfilename
```

### Go
```bash
go run yourfilename.go
```

### HTML/CSS
Just open the file in your web browser!

---

## Troubleshooting

### "Command not found" error

If you see this error, try restarting your terminal/command prompt and try again.

### Installation failed

Make sure you have:
- Internet connection
- Enough space on your computer (at least 2GB free)
- Administrator rights (on Windows)

### Visual Studio Code didn't open

You can open it manually:
1. Search for "Visual Studio Code" in your apps
2. Open it
3. Go to File > Open Folder
4. Find the folder: `C:\Users\YourName\projectdevsetup_projects\YourFileName`

---

## What's Included in Your Project Folder

When you run the tool, it creates a folder with these files:

```
projectdevsetup_projects/
└── yourfilename/
    ├── yourfilename.py       (your code)
    ├── requirements.txt     (list of Python packages)
    └── .venv/               (virtual environment for Python)
```

---

## Want to Learn More?

Here are great resources for beginners:

### Python
- https://www.python.org/about/gettingstarted/
- https://www.freecodecamp.org/learn/python/

### JavaScript
- https://www.javascript.com/
- https://www.freecodecamp.org/learn/javascript/

### HTML/CSS
- https://www.w3schools.com/html/
- https://www.freecodecamp.org/learn/html-css/

---

## Uninstallation

If you want to remove projectdevsetup:

```bash
pip uninstall projectdevsetup
```

---

## Credits

**Developer**: roshhellwett  
**Email**: roshhellwett@icloud.com  
**Organization**: [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app)  
**Copyright**: (c) 2026 Zenith Open Source Projects

---

## License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## Need Help?

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Visit: https://github.com/zenith-open-source/projectdevsetup
3. Open an issue on GitHub

---

**Happy Coding!** 🚀
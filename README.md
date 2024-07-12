# PyVCS: Python Version Control System

PyVCS is a lightweight version control system implemented in Python. The aim with this project is to understand of how version control systems work under the hood and have fun implementing it in Python.

The goal is to peek underneath the abstraction and reimplement the abstraction from scratch, to gain deep understanding of what's being abstracted.

## Features

- Initialize a new repository
- Add files to version control
- Commit changes with messages
- View differences between current files and last commit


## Installation

Clone the repository:

```shell
git clone https://github.com/OmKharade/pyvcs.git
cd pyvcs
```

Install the package:
```shell
pip install -e .
```

## Usage

```shell
# Transform the current directory into a PyVCS repository:
pyvcs init

# Create an empty repository in a new subdirectory called ＜directory＞
pyvcs init <directory>

# Add a file to version control:
pyvcs add filename.txt

# Commit changes:
pyvcs commit "Commit Message"

# View differences:
pyvcs diff filename.txt
```

### Project Structure

```
pyvcs/
├── pyvcs/
│   ├── __init__.py
│   └── core.py
├── cli.py
├── setup.py
└── README.md
```

### Future Versions 

- Improve diff algorithm (line-by-line changes)
- Branching and Merging
- Remote Repositories

### Contributing

This is the very very early version of the project. I decided to push this to motivate myself and hold myself accountable to keep working on this

Having said, of course suggestions and discussions are welcome ! Feel free to open an issue or submit a PR

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### References

1. [Write Yourself a Git by Thibault Polge](https://wyag.thb.lt/) 
2. [Basics about Version Control Systems](https://rao-sithara.medium.com/version-control-system-and-git-commands-b05b6205ae40)
3. [Everything about Git Commands](https://www.atlassian.com/git/tutorials/setting-up-a-repository)

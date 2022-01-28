import os
from pathlib import Path

from repo_maker.resource import PYENV, GIT

from repo_maker.utils import FILES_DIR


def read_file(file):
    if not file.exists():
        raise FileNotFoundError(f"This file doesn't exist! {file}")

    with open(file, "r") as f:
        lines = f.readlines()

    return lines


def write_file(data, file):
    with open(file, "w") as f:
        if isinstance(data, list):
            for line in data:
                f.write(line)
        elif isinstance(data, str):
            f.write(data)
        else:
            raise InputError(f"Cannot write data type {type(data)}")


def create_module_name(repo_name: str):
    return repo_name.replace(" ", "_").replace("-", "_").lower()


class RepoAlreadyExistsError(Exception):
    pass


def create_repo(repo_name: str):
    cwd = Path.cwd()

    repo_root = cwd / repo_name

    if repo_root.exists():
        raise RepoAlreadyExistsError("The repo already exists.")

    repo_root.mkdir()

    os.chdir(repo_root)

    PIPENV().init_if_exists()

    GIT().init_if_exists()

    # Create files in the root
    files = ["README.md", ".gitignore", ".env.example", "Makefile"]
    for file in files:
        (repo_root / file).touch()

    sample_gitignore_lines = read_file(FILES_DIR / "gitignore")
    write_file(sample_gitignore_lines, repo_root / ".gitignore")

    module_name = create_module_name(repo_name)
    # Initialize all directories
    root_dirs = ["notebooks", module_name, "scripts", "tests", "data"]
    for root_dir in root_dirs:
        (repo_root / root_dir).mkdir()

    # Create files in the project directory
    files = ["__init__.py"]
    for file in files:
        (repo_root / module_name / file).touch()

    file_lines = read_file(FILES_DIR / "utils.py")
    write_file(file_lines, repo_root / module_name / "utils.py")

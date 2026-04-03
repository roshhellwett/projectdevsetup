"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

from setuptools import setup, find_packages

setup(
    name="projectdevsetup",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    py_modules=[
        "__init__",
        "__main__",
        "detector",
        "installer",
        "network",
        "path_manager",
        "permissions",
        "vscode",
        "wizard",
    ],
    package_data={
        "": ["templates/*"],
    },
)

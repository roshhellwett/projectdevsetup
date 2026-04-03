"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

from setuptools import setup, find_packages

setup(
    name="projectdevsetup",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "projectdevsetup": ["templates/*"],
    },
)

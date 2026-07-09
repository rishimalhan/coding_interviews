from setuptools import setup, find_packages

setup(
    name="chef_interview",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)

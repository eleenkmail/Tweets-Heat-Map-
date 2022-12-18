from pathlib import Path

from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

style_packages = ["black==22.8.0"]
analysis_packes = ["jupyterlab==3.4.6"]

# Define our package
setup(
    name="MLOps",
    version=1.0,
    description="a test project for MLOps",
    author="your name",
    author_email="your email",
    python_requires=">=3.7",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={
        "dev": style_packages + analysis_packes,
    },
)

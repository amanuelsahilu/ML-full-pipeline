
from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as f:
        requirements = f.read().strip().split('\n')[0]

    if "-e ." in requirements:
        requirements.pop(requirements.index("-e ."))

setup(
    name='FirstMlProject',
    version='0.1',
    packages=find_packages(),
    install_requires= get_requirements('requirements.txt'),
)
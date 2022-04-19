import os
from setuptools import find_packages, setup


# Functions 'read' and 'get_version' are taken from:
# https://github.com/pypa/pip/blob/main/setup.py#L11
# https://packaging.python.org/en/latest/guides/single-sourcing-package-version/#single-sourcing-the-version
def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


# For more details on setup, see:
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
long_description = read("README.md")

setup(
    name='BuildME',
    version=get_version("BuildME/__init__.py"),
    description="Framework to calculate building material & energy expenditures.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',  # copyright = 'Niko Heeren 2019',
    classifiers=[  # See https://pypi.org/classifiers/ for full list
                'Development Status :: 3 - Alpha',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 3',
                'Private :: Do Not Upload',  # Prevents upload to PyPI
    ],
    url='https://github.com/nheeren/BuildME',
    project_urls={
        'Documentation': '',  # TODO(cbreton026): Add link to official docs
        'Source': 'https://github.com/nheeren/BuildME',
        'Tracker': 'https://github.com/nheeren/BuildME/issues',
    },
    author='Niko Heeren',
    author_email='niko.heeren@gmail.com',
    packages=find_packages(
        where='BuildME',
        exclude=[''],
    ),
    python_requires='',  # TODO(cbreton026): What is the req. Python version? https://pypi.org/project/vermin/
)

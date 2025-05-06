import io
import os
import re

from setuptools import setup

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open("earthreach/version.py", encoding="utf_8_sig").read(),
).group(1)


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "requirements.txt")) as f:
    requirements = f.read().splitlines()

setup(
    name="earthreach",
    version=__version__,
    description="Alt text generation for earthkit-plots.",
    include_package_data=True,
    install_requires=requirements,
)
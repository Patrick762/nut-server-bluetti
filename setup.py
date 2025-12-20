"""Setup for pypi package"""

import os
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.1"
DESCRIPTION = "NUT Server Bluetti"

# Setting up
setup(
    name="nut-server-bluetti",
    version=VERSION,
    author="Patrick762",
    author_email="<pip-nut-server-bluetti@hosting-rt.de>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Patrick762/nut-server-bluetti",
    packages=find_packages(),
    install_requires=[
        "asyncio",
        "nut-definitions",
    ],
    keywords=[],
    entry_points={
        "console_scripts": [
            "bluetti-nut = nut_server_bluetti.scripts.server:start",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)

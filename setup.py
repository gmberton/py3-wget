from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Get version from __version__.py
version = {}
with open(os.path.join(here, "py3_wget", "__version__.py")) as f:
    exec(f.read(), version)

# Setting up
setup(
    name="py3_wget",
    version=version["__version__"],
    author="Gabriele Berton",
    author_email="bertongabri@gmail.com",
    description="A tool to download files. It supports progress bar, cksum, timeout, retry failed download.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["tqdm"],
    keywords=["python", "download", "progress bar"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)

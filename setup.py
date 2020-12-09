from setuptools import setup
from os import path


def read(relpath):
    with open(path.join(path.dirname(__file__), relpath)) as f:
        return f.read()


setup(
    name="firefox-profile",
    version="0.0.1",
    description="Utility to access Firefox profile data.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/luismsgomes/firefox-profile",
    author="Luís Gomes",
    author_email="luismsgomes@gmail.com",
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="firefox util commandline",
    install_requires=["lz4"],
    py_modules=["firefox_profile"],
    entry_points={
        "console_scripts": [
            "firefox-profile-json=firefox_profile:main",
        ],
    },
)

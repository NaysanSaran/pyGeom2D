import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name    = "pygeometry-pkg",
    version = "0.0.1",
    author  = "Naysan Saran",
    author_email    = "naysan.saran@gmail.com",
    description     = "A package for 2D geometry in Python",
    url             = "https://github.com/NaysanSaran/pygeometry.git",
    packages        = setuptools.find_packages(),
    classifiers     = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


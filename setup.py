import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name    = "pyGeom2D",
    version = "0.1.2",
    author  = "Naysan Saran",
    author_email    = "naysan.saran@gmail.com",
    description     = "A package for 2D geometry in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url             = "https://github.com/NaysanSaran/pyGeom2D.git",
    license         = "MIT",
    packages        = setuptools.find_packages(),
    include_package_data = True,
    install_requires=["matplotlib", "numpy", "scipy"],
    classifiers     = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


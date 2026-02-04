import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setuptools.setup(
    name="coreli",
    version="0.0.7",
    author="Tristan Stérin",
    author_email="tristan.sterin@mu.ie",
    description="The Collatz Research Library provides tools for experimenting and testing hypothesises related to the Collatz Process.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tcosmo/coreli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=install_requires,
)

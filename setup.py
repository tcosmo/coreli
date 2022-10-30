import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coreli",
    version="0.0.3",
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
    python_requires='>=3.6',
    install_requires=[
          'sympy',
          'drawsvg',
          'ipywidgets'
      ],
)

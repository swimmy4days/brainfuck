import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brainfuck-swimmy4days",
    version="0.0.3",
    author="Ido Drori",
    author_email="idonevodrori@gmail.com",
    description="A BrainFuck Interpreter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swimmy4days/brainfuck",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TheLogicMaster",
    version="0.0.1",
    author="Justin Marentette",
    author_email="justinmarentette11@gmail.com",
    description="A Webkinz mini-game bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheLogicMaster/WebkinzBot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
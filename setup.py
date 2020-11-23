from setuptools import setup, find_packages
from os import path

pathHere = path.abspath(path.dirname(__file__))
with open(path.join(pathHere,"README.md"),encoding="utf-8") as f:
    readme = f.read()

setup(
        name="MangaDexDownloader",
        version=1.0,
        url="https://github.com/Barraque/MangaDexDownloader",
        author="Barraque",
        author_email="balobalo@petit.lu",
        description="Scan downloader from the MangaDex website",
        long_description_content_type="text/markdown",
        long_description=readme,
        keywords="mangadex scan manga download",
        license="UNLICENSE",
        classifiers=[
            "License :: OSI Approved :: THE UNLICENSE"
            "Operating System :: MacOs",
            "Operating System :: POSIX",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: Python :: 3 :: Only",
            ],
        packages=["getmanga.py"],
        entry_points={
            "console_scripts": [ "getmanga = getmanga:main"]
            }
        )

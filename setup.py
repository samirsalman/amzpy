from setuptools import setup, find_packages

setup(
    name="amzpy",
    version="0.1.0",
    description="A lightweight Amazon scraper library.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Anil Sardiwal",
    author_email="theonlyanil@gmail.com",
    url="https://github.com/theonlyanil/amzpy",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "fake-useragent",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

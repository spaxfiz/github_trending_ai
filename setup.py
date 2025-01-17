from setuptools import setup, find_packages

setup(
    name="my_app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
        if line.strip() and not line.startswith("#")
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="一个轻量级Python应用",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
)

from setuptools import setup, find_packages

setup(
    name="SCSTools",
    version="0.1.0",
    description="Package for all tools across SCS projects",
    url="https://www.southcoaststone.com",
    author="Sam Pearson-Smith",
    author_email="sam@southcoaststone.com",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["scs", "tools"],
    packages=find_packages(),
    python_requires=">=3.12"
    # install_requires=[],
)

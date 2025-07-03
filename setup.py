from setuptools import setup, find_packages


setup(name="dab_project_udemy", #name up to you
    version="0.0.1", # version of the package
    description="this contains the code in ./src directory of the project",
    author="Nova Guliyev",
    packages=find_packages(where="./src"), # setuptools will look .src for the packages.
    package_dir={"":"./src"},
    install_requires=["setuptools"] # dependencies, when someone install package it will make sure these packages downloaded
)
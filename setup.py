from setuptools import setup, find_packages

setup(
    name="evdev3_utilities",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["numpy"],
    description="Utility functions from evdev3, like print_structure_shape",
    author="Evan Woods",
    author_email="evanwoods.contact@icloud.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)

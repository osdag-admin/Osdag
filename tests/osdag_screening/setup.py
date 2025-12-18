from setuptools import setup, find_packages

setup(
    name="osdag-validator",
    version="0.1",
    packages=find_packages(include=["osdag_validator", "osdag_validator.*", "Osdag", "Osdag.*"]),
    include_package_data=True,
    install_requires=[],
)

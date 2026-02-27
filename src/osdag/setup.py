# setup.py

from setuptools import setup, find_packages

setup(
    name='osdag-cli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'PyYAML',
        'PyQt5',
    ],
    entry_points={
        'console_scripts': [
            'osdag-cli = osdag.cli_shell:cli',
        ],
    },
)

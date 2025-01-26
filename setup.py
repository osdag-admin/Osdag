# setup.py

from setuptools import setup

setup(
    name='osdag-cli',
    version='0.1.0',
    py_modules=['osdag_cli'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'osdag-cli = osdag_cli:determine_module',
        ],
    },
)

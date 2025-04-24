import os
import subprocess
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

# Path to the test hook that gets executed via .pth
def create_test_pth_file():
    site_packages = next(p for p in sys.path if 'site-packages' in p)
    pth_file = os.path.join(site_packages, 'osdag_test_runner.pth')
    with open(pth_file, 'w') as f:
        f.write("import osdag.run_pytest\n")

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))

# Create the .pth file during setup execution (not install command)
create_test_pth_file()

setup(
    name="osdag",
    version="0.1.0",
    packages=["osdag"],  # Replace with your actual package name
    cmdclass={
        'test': PyTest,
    },
)

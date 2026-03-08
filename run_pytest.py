import subprocess
import sys

print(">>> Automatically running tests with pytest <<<")
try:
    subprocess.check_call([sys.executable, "-m", "pytest", "--maxfail=1", "--disable-warnings"])
except subprocess.CalledProcessError:
    print(">>> Tests failed during editable install <<<")

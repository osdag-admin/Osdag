import argparse

parser = argparse.ArgumentParser(description='converts the input into a report')
parser.add_argument('filename', help='The name of the file which should be processed')
arguments = parser.parse_args()

print(arguments)
print(arguments.filename)
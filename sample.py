import argparse

# loading & unzipping data
parser = argparse.ArgumentParser()
parser.add_argument("path", metavar="p", help="Path to dataset files")
parser.add_argument("output_path", metavar="o", help="Path to save data")
args = parser.parse_args()

print(args.path)
print(args.output_path)

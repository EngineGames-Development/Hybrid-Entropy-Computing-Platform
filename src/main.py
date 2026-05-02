import argparse
from randomness_validation import benchmark
from password_generator import generate_password

parser = argparse.ArgumentParser()

parser.add_argument("mode")

args = parser.parse_args()

if args.mode == "test":
    benchmark()

elif args.mode == "password":
    generate_password()
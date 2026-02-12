"""Very simple password generator.

Usage: python simple_password_generator.py --length 12
"""
import argparse
import secrets
import string


def generate_simple_password(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def parse_args():
    p = argparse.ArgumentParser(description="Simple password generator")
    p.add_argument("--length", "-l", type=int, default=8, help="Password length")
    return p.parse_args()


def main():
    args = parse_args()
    print(generate_simple_password(args.length))


if __name__ == '__main__':
    main()

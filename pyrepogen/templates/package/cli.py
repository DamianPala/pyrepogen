#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse

from spackage import modulo


def main():
    print("Hello from Package!")

    parser = argparse.ArgumentParser(description='Get modulo of two integers.')
    parser.add_argument('divident', type=int, help='a divident of modulo operation')
    parser.add_argument('divisor', type=int, help='a divisor of modulo operation')

    args = parser.parse_args()

    modulus = modulo.get_reminder(args.divident, args.divisor)

    print("{} modulo {} = {}".format(args.divident, args.divisor, modulus))

    return 0

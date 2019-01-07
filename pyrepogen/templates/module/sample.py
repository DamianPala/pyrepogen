#!/usr/bin/env python
# -*- coding: utf-8 -*-


__version__ = '0.1.0'


def get_sum(a, b):
    return a + b


def main():
    print("Hello from Standalone Module!")
    print("2 + 3 = {}".format(get_sum(2, 3)))
    

if __name__ == '__main__':
    main()

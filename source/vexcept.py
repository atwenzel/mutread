"""Exceptions defined for mutread"""

#Global
import sys

#Local

class BadHeaderAccess(Exception):
    def __init__(self):
        print("FATAL ERROR: Tried to modify VCF Header data")

class HeaderParseError(Exception):
    def __init__(self, rawline):
        print("FATAL ERROR: Encountered a parse error in header line: ")
        print(rawline)

class FormatParseError(Exception):
    def __init__(self, rawform, rawstr):
        print("FATAL ERROR: Couldn't parse format in data line")
        print("\tFormat: "+rawform)
        print("\tValues: "+rawstr)

class NoValueError(Exception):
    """Use this for wrapper functions when no value should be added to the cumulative list"""
    def __init__(self):
        return

if __name__ == "__main__":
    print("This file defines exceptions specific to the mutread system")

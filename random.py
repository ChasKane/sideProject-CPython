# 1.2
# Write code to reverse a C-Style String (C-String means
# that “abcd” is represented as five characters, including
# the null character).
# INPUT: pre-formatted (last char is ' ' representing '\0')
# string, "any" length
# OUTPUT: reverse of input string, with ' ' still as last char
def c_reverse(s):
    # the point of this question is somewhat lost in Python,
    # but this was an excellent opportunity to learn about
    # cython from https://jasonstitt.com/mutable-python-strings
    # also super helpful:
    # https://github.com/python/cpython/blob/master/Include/object.h
    # and search `from_address` on this page once you get going:
    # https://github.com/python/cpython/blob/master/Doc/library/ctypes.rst
    # ... 3 hours later (said in bored pirate voice) ...
    # After fidling with this for a while, it seems silly to put here,
    # as it has caused seg faults (in Python!!! :D ), and isn't relevent
    # to the problem per say. I've moved this to a seperate repo:
    #

    return s
from ctypes import sizeof, c_void_p, c_char, c_long, c_int

# All python objects have reference count and type pointers,
# and variable-length objects get a length. Why a length is
# represented as the size of a pointer, idk. So that's 3 ptrs,
# and then stirngs have a hash... thing... which is a long (I
# spent 2 hours looking into this, and I can't figure out
# whether this is a precomputed hash or essentially the
# __hash__ method pointer... it shouldn't be a long???).
# Anyway, that's 3 ptrs and a long for a bytes array header.
bytes_header_size = sizeof(c_void_p) * 3 + sizeof(c_long)

# Add 4 int flags (one of which determines whether the characters
# each take up 1 or 2 bytes) to the size of a byte string object,
# and you get a string object header.
string_header_size = bytes_header_size + sizeof(c_int) * 4

# ctypes (always?) have a from_address function that creates a
# writable window directly into memory

# Cracking the Coding Interview question 1.2
# Write code to reverse a C-Style String (C-String means
# that “abcd” is represented as five characters, including
# the null terminator '\0').
# INPUT: any string "any" length (note: untested with non-ascii chars)
# also, note that python strings aren't null terminated -- don't worry
# about adding one, my code adds one, then removes it upon return
# OUTPUT: reverse of input string, with ' ' still as last char
def c_reverse(s):
    # the point of this question is somewhat lost in Python,
    # but this was an excellent opportunity to learn about
    # CPython from https://jasonstitt.com/mutable-python-strings
    # also super helpful:
    # https://github.com/python/cpython/blob/master/Include/object.h
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
    # writable window directly into memory. I don't quite understand
    # this yet, but I have a grasp of it sufficient for the problem.
    # Search `from_address` on this page to pick up where I left off:
    # https://github.com/python/cpython/blob/master/Doc/library/ctypes.rst
    # Multiplying c_char by a number yields a c_char array of that length,
    # it seems. id() yields the memory address of the string, and then that
    # address must be incremented so that the writable window is over the data,
    # not the header, of the given string. len + 1 so we can see the \0.
    #
    # Note, char array is capital S, and we return lowercase s!!! we modified
    # the input Python string object!
    S = (c_char * (len(s) + 1)).from_address(id(s) + string_header_size)

    # Clear last char, since in python strings don't have a null sentinal.
    # this could cause issues, but I haven't seen any yet!
    S[-1] = 0

    # Now, to reverse the string. In C, the length of a string is unknown at
    # first, so now that we have an actually C-like string, we'll start the
    # timer, if you will. This is actually a fairly simple problem, and the
    # fastest, most memory efficient way I know of to do it is to use in-place
    # data swapping between the front and back of the string, working inward.
    t = 0 # t(ail)
    while ord(S[t]): # while not null sentinal -- ord() because bytes are in base 10(???)
        t += 1

    # t is at null sentinal, so decriment to avoid swapping \0 to front
    t -= 1

    # now in place swap using XOR (because it's fun!)
    h = 0 # h(ead)
    while h < t:
        # XOR doesn't work on byte class, so translate to bits (this wasted
        # space wouldn't be necessary in C)
        a = ord(S[h])
        b = ord(S[t])

        # mix b info with a's memory
        a ^= b
        # mix a and b info with b's memory, canceling all b info there
        b ^= a
        # mix what's now just a info with a's memory, but since a and b info
        # was already in a's memory, the a info is canceled, leaving only b info
        a ^= b

        # auto convert back to bytes ( <3 Python)
        S[h] = a
        S[t] = b

        h += 1
        t -= 1

    return s

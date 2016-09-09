#!/usr/bin/env python
"""
*******************************************************************
 ssr-extractor (extract short sequence repeats)
*******************************************************************
  Automatic short sequence repeat extraction based on run length
  encoding with variable run lengths.
*******************************************************************
"""


from __future__ import unicode_literals
import sys


THRESHOLD = 10000


class Repeat(object):
    """
    Simple repeat structure.
    """
    __slots__ = ['start', 'end', 'count']

    def __init__(self, start, end, count=0):
        """
        Initialize the repeat structure.

        :arg integer start: Start position of the repeat.
        :arg integer end: End position of the repeat.
        :arg integer count: Number of repeats.
        """
        self.start = start
        self.end = end
        self.count = count


def short_sequence_repeat_extractor(string, min_length=1):
    """
    Extract the short tandem repeat structure from a string.

    :arg string string: The string.
    :arg integer min_length: Minimum length of the repeat structure.
    """
    length = len(string)

    k_max = length // 2 + 1
    if k_max > THRESHOLD:
        k_max = THRESHOLD // 2

    repeats = []

    i = 0
    last_repeat = i
    while i < length:
        max_count = 0
        max_k = 1
        for k in range(min_length, k_max):
            count = 0
            for j in range(i + k, length - k + 1, k):
                if string[i:i + k] != string[j:j + k]:
                    break
                count += 1

            if count > 0 and count >= max_count:
                max_count = count
                max_k = k

        if max_count > 0:
            if last_repeat < i:
                repeats.append(Repeat(last_repeat, i))
            repeats.append(Repeat(i, i + max_k, max_count))
            last_repeat = i + max_k * (max_count + 1)

        i += max_k * (max_count + 1)

    if last_repeat < i:
        repeats.append(Repeat(last_repeat, i))

    return repeats


def main():
    """
    Entry point for the console.
    """
    if len(sys.argv) < 2:
        print ("usage: " + sys.argv[0] + " file "
               "[unit_count] [min_length] [min_count] [start] [end]")
        exit()

    with open(sys.argv[1], "r") as infile:
        string = infile.read()

    unit_count = 1
    if len(sys.argv) > 2:
        unit_count = max(1, int(float(sys.argv[2])))

    min_length = 1
    if len(sys.argv) > 3:
        min_length = max(1, int(float(sys.argv[3])))

    min_count = 1
    if len(sys.argv) > 4:
        min_count = max(1, int(float(sys.argv[4])))

    start = 0
    if len(sys.argv) > 5:
        start = max(0, int(float(sys.argv[5])))

    end = len(string)
    if len(sys.argv) > 6:
        end = max(start, int(float(sys.argv[6])))

    repeats = short_sequence_repeat_extractor(string[start:end], min_length)

#    for repeat in repeats:
#        if repeat.count >= min_count:
#            print "%s%d" % (string[repeat.start:repeat.end], repeat.count + 1),
#        else:
#            for _ in range(repeat.count + 1):
#                print string[repeat.start:repeat.end],

    units = {}
    for repeat in repeats:
        if repeat.count + 1 >= unit_count:
            units[string[repeat.start:repeat.end]] = repeat.count + 1

    print units

if __name__ == "__main__":
    main()


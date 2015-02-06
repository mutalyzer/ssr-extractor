#!/usr/bin/env python
## *******************************************************************
##   (C) Copyright 2015 Leiden Institute of Advanced Computer Science
##   Universiteit Leiden
##   All Rights Reserved
## *******************************************************************
## ssr-extractor (extract short sequence repeats)
## *******************************************************************
## FILE INFORMATION:
##   File:     ssr-extractor.py
##   Author:   Jonathan K. Vis
##   Revision: 1.0.1
##   Date:     2015/02/06
## *******************************************************************
## DESCRIPTION:
##  Automatic short sequence repeat extraction based on run length
##  encoding with variable run lengths.
## *******************************************************************

import sys

THRESHOLD = 10000

class Repeat(object):
    __slots__ = ['start', 'end', 'count']

    def __init__(self, start, end, count = 0):
        self.start = start
        self.end = end
        self.count = count


def short_sequence_repeat_extractor(string, min_length = 1):
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
    if len(sys.argv) < 2:
        print "usage: " + sys.argv[0] + " string [min_length] [min_count] [start] [end]"
        exit()

    f = open(sys.argv[1], "r")
    string = f.read()
    f.close()

    min_length = 1
    if len(sys.argv) > 2:
        min_length = int(float(sys.argv[2]))
        if min_length < 1:
            min_length = 1

    min_count = 1
    if len(sys.argv) > 3:
        min_count = int(float(sys.argv[3]))
        if min_count < 1:
            min_count = 1

    start = 0
    if len(sys.argv) > 4:
        start = int(float(sys.argv[4]))
        if start < 0:
            start = 0

    end = len(string)
    if len(sys.argv) > 5:
        end = int(float(sys.argv[5]))
        if end < start:
            end = start

    repeats = short_sequence_repeat_extractor(string[start:end], min_length)

    for r in repeats:
        if r.count >= min_count:
            print "%s%d" % (string[r.start:r.end], r.count + 1),
        else:
            for i in range(r.count + 1):
                print string[r.start:r.end],


if __name__ == "__main__":
    main()


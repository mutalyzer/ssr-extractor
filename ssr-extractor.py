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
##   Revision: 1.0.0
##   Date:     2015/02/05
## *******************************************************************
## DESCRIPTION:
##  Automatic short tandem repeat detection based on run length
##  encoding with variable run lengths.
## *******************************************************************

import sys

THRESHOLD = 10000

class Repeat(object):
  __slots__ = ['start', 'end', 'count']

  def __init__(self, start, end, count = 0):
    self.start = start
    self.end   = end
    self.count = count
  #__init__
#Repeat

def tandem_repeat_annotator(string, min_length = 1):
  length = len(string)
  k_max = length // 2 + 1
  if k_max > THRESHOLD:
    k_max = THRESHOLD // 2
  #if

  result = []

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
        #if
        count += 1
      #for
      if count > 0 and count >= max_count:
        max_count = count
        max_k = k
      #if
    #for
    if max_count > 0:
      if last_repeat < i:
        result.append(Repeat(last_repeat, i))
      #if
      result.append(Repeat(i, i + max_k, max_count))
      last_repeat = i + max_k * (max_count + 1)
    #if
    i += max_k * (max_count + 1)
  #while
  if last_repeat < i:
    result.append(Repeat(last_repeat, i))
  #if
  return result
#tandem_repeat_annotator

def main():
  if len(sys.argv) < 2:
    print "usage: " + sys.argv[0] + " string [min_length] [min_count] [start] [end]"
    exit()
  #if
  print "Tandem Repeat Annotator"

  f = open(sys.argv[1], "r")
  string = f.read()
  f.close()

  min_length = 1
  if len(sys.argv) > 2:
    min_length = int(float(sys.argv[2]))
    if min_length < 1:
      min_length = 1
    #if
  #if
  min_count = 0
  if len(sys.argv) > 3:
    min_count = int(float(sys.argv[3]))
    if min_count < 0:
      min_count = 0
    #if
  #if
  start = 0
  if len(sys.argv) > 4:
    start = int(float(sys.argv[4]))
    if start < 0:
      start = 0
    #if
  #if
  end = len(string)
  if len(sys.argv) > 5:
    end = int(float(sys.argv[5]))
    if end < start:
      end = start
    #if
  #if

  repeats = tandem_repeat_annotator(string[start:end], min_length)

  for r in repeats:
    if r.count >= min_count:
      print "%s%d" % (string[r.start:r.end], r.count + 1),
    #if
    else:
      for i in range(r.count + 1):
        print string[r.start:r.end],
    #else
  #for

#main

if __name__ == "__main__":
  main()
#if


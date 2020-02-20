#!/usr/bin/env python
"""mapper.py"""

import sys
import string

for line in sys.stdin:
    for word in line.strip().split():
        lowered = word.lower()
        filtered = filter(lambda c: 97 <= ord(c) <= 122, lowered)
        if len(filtered) > 0:
            o = ord(filtered[0])
            if o <= 105:
                k = 'early'
            elif o <= 114:
                k = 'middle'
            elif o <= 122:
                k = 'late'
            else: 
                raise "Bad ordinal!"
            print '%s\t%s' % (k, len(filtered))

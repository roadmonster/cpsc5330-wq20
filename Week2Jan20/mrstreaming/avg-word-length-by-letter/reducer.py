#!/usr/bin/env python
import sys

current_label = None
current_sum = 0
current_count = 0
word = None

for line in sys.stdin:
    line = line.strip()
    label, fcount = line.split('\t', 1)
    #  It is a big decision whether to error, log, or ignore bad inputs!
    try:
        fcount = int(fcount)
    except ValueError:
        continue

    if current_label == label:
        current_sum += fcount
        current_count += 1
    else:
        if current_label:
            # Multipy by 1.0 needed to force real-valued division
            print '%s\t%f' % (current_label, (1.0 * current_sum)/current_count)
        current_label = label
        current_sum = fcount
        current_count = 1

if current_label == label:
    print '%s\t%f' % (current_label, (current_sum * 1.0)/ current_count)

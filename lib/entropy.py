# -*- coding: utf-8 -*-

# Taken from https://rosettacode.org/wiki/Entropy#Python
def calculate(phrase):
    import math
    from collections import Counter

    objects, size = Counter(phrase), float(len(phrase))
    return -sum(count/size * math.log(count/size, 2) for count in objects.values())

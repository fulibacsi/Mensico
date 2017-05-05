import random
from fractions import gcd

import numpy as np


def lcm(num1, num2):
    return num1 * num2 // gcd(num1, num2)


def weighted_choice(weights):
    if not weights.sum() == 1.0:
        weights = weights / weights.sum()
    return np.random.choice(len(weights, p=weights)


def weighted_choice_sub(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i


def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    for key, value in dic.iteritems():
        if value == val:
            return key
    return None

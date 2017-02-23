# encoding: utf-8


def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    for key, value in dic.iteritems():
        if value == val:
            return key
    return None

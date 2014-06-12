#!/usr/bin/python3
def divider(l, each):
    # divides a list into a list of lists each of which contains of (each) elements
    z = []
    a = []
    for i, item in enumerate(l):
        if i % each == 0 and i > 0:
            a.extend([z])
            z = []
        z.append(item)
    if len(z) > 0:
        a.extend([z])
    return a

def flatten(x):
    # returns a list containing a flattened version for each non-hashable element ..
    result = []
    for el in x:
        try:
            el.keys()
            hashable = True
        except AttributeError:
            hashable = False
        if isinstance(el, collections.Iterable) and not isinstance(el, str) and not hashable:
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

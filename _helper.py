BUILTIN_ITERABLES = (list, tuple, set, map)


def flatten_list(lists):
    if type(lists) not in BUILTIN_ITERABLES:
        return [lists]
    
    l = []

    for item in lists:
        if type(item) in BUILTIN_ITERABLES:
            l.extend(flatten_list(item))
        else:
            l.append(item)
    
    return l
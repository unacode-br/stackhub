def find_in_list(lst, key, value):
    """
    Find an index in a list.
    """
    try:
        return next(index for (index, x) in enumerate(lst) if x[key] == value)
    except:
        return None

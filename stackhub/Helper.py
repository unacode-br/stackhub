import math
import time
from datetime import datetime

def find_in_list(lst, key, value):
    """
    Find an index in a list.
    """
    try:
        return next(index for (index, x) in enumerate(lst) if x[key] == value)
    except:
        return None

def date_to_unix(dt):
    """
    Convert a string date to an UNIX timestamp.
    """
    return time.mktime(datetime.strptime(dt, '%Y-%m-%d').timetuple())

def learning_curve(z, n, index, counter=5):
    """
    Calculate the learning curve.
    """
    _counter = 1
    _index = index

    x = 1

    data = [ { 'y': 1, 'x': x, 'value': z } ]

    while _counter <= counter:
        x *= 2

        if _counter > 1:
            _index *= index

        lc = z * (math.pow(_index, math.log(n, 2)))

        data.append({ 'y': _index, 'x': x, 'value': lc })

        _counter += 1

    return tuple(data)

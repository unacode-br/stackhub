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

def learning_curve(z, n, curve, counter=5):
    """
    Calculate the learning curve five times.
    """
    _counter = 1

    data = []

    while _counter <= counter:
        if _counter > 1:
            curve = curve - (curve * 0.016)

        lc = z * (math.pow(curve, math.log(n, 2)))

        data.append(lc)

        _counter += 1

    return tuple(data)

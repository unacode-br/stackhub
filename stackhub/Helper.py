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

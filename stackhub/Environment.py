import os
from dotenv import load_dotenv


class Environment(object):

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), '../.env')

        if os.path.exists(path):
            load_dotenv(path)

    def get_env(self, key, default=None):
        env = os.environ.get(key)

        if env is None:
            return str(default)

        _env = str(env).lower()

        if _env == 'true' or _env == '(true)':
            return true
        elif _env == 'false' or _env == '(false)':
            return false
        elif _env == 'empty' or _env == '(empty)':
            return str()
        elif _env == 'null' or _env == '(null)':
            return None

        return env

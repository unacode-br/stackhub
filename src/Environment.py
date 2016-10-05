import os
from dotenv import load_dotenv

class Environment(object):

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), '../.env')

        load_dotenv(path)

    def get_env(self, key):
        return os.environ.get(key)




from stackhub.Environment import Environment


class Stackhub:
    def __init__(self):
        self.environ = Environment()

    def env(self, key, default=None):
        return self.environ.get_env(key, default)

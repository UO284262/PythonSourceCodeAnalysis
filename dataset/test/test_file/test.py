from functools import wraps

class b:
    def f(self):
        pass
    @wraps(f)
    def a(self):
        pass
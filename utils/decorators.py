from datetime import datetime
from functools import wraps
import time 
def log_call(func):
    @wraps(func)
    def wrapper(*args , **kwargs):
        time  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Calling {func.__name__} at {time}")
        return func(*args, **kwargs)
    return wrapper


def time_execution(func):
    @wraps(func)
    def wrapper(*args , **kwargs):
        start = time.time()
        result = func(*args , **kwargs)
        stop = time.time()
        print(f"The time for executing {func.__name__} is {stop-start:.4f}")
        return result
    return wrapper




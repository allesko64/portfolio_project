from datetime import datetime
from functools import wraps
import time
import inspect

def log_call(func):
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"Calling {func.__name__} at {current_time}")
            return await func(*args, **kwargs)
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"Calling {func.__name__} at {current_time}")
            return func(*args, **kwargs)
        return sync_wrapper


def time_execution(func):
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                stop = time.time()
                print(f"The time for executing {func.__name__} is {stop-start:.4f}")
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                stop = time.time()
                print(f"The time for executing {func.__name__} is {stop-start:.4f}")
        return sync_wrapper




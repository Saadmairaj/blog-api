import threading
from typing import Union


class Performer(threading.Thread):
    """
    A subclass of threading.Thread, that returns 
    callback value when done.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None

    def start(self):
        super().start()
        return self

    def run(self):
        """Method representing the thread's activity."""
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, timeout=None):
        super().join(timeout=timeout)
        return self._return


def threaded(fn) -> Performer:
    """To use as decorator to make a function call threaded."""
    def thread_func(*args, **kwargs):
        return Performer(
            target=fn, args=args, kwargs=kwargs, daemon=True
        ).start()
    return thread_func


def wait_until_done(thread_list: list = []) -> list:
    """Wait function for threaded decorator and returns 
    values of their callback functions in same order 
    when all threads are completed"""
    return [thread.join() for thread in thread_list]


def remove_duplicates(data: Union[list, tuple]):
    """Removes duplicates from list of dictionaries"""
    new_data = []
    for i in range(len(data)):
        if data[i] not in new_data:
            new_data.append(data[i])

    return new_data

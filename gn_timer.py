"""
This is a simple timing module which uses wrappers. Time values are stored at
the class level, so multiple generated timer objects will all increment the same
shared time values. Use it to keep track of how much total time different
function calls are taking.

The Timer class stores running timers in seconds as attributes. Attributes
correspond to the name of the function which is wrapped.

Wrap functions you want to time with @Timer.timer. This wrapper
increments the timer which corresponds to the name of the function which it
wraps.

METHODS:

Timer.timer(timer_key: str) -> Callable:
    Wrapper function to time other functions. Time in seconds of execution is
    stored in the class attribute indicated by timer_key.

METHODS:

print_times(): prints all timer attributes from class Timer

CHANGELOG:
4-18-19: Created
4-24-19: Updated to use cls.__dict__ instead of a dict attribute
6-5-19: Overhauled to use the names of the timed functions.
"""
# from typing import Dict
from typing import Callable
import time as time_module


class Timer:
    """
    METHODS:

    Timer.timer() -> Callable:
        Wrapper function to time other functions. Time in seconds of execution
        is stored in the class attribute indicated by timer_key.


    """
    def __setattr__(self, name: str, value: float) -> None:
        if name == 'timer':
            raise Exception("cannot overwrite timer")
        self.__dict__[name] = value

    @classmethod
    def _increment_time(cls, timer_key: str, sec_to_increment: float) -> None:
        """
        increment the time variable specified by Timer.timer_dict[
        abbreviation].
        :param timer_key: key corresponding to the timer attribute to
        increment
        :param sec_to_increment: number of seconds by which to increment the
        timer attribute
        :return: None
        """
        if not hasattr(cls, timer_key):
            setattr(cls, timer_key, 0)
        timer_value = getattr(cls, timer_key)
        new_timer_value = timer_value + sec_to_increment
        setattr(cls, timer_key, new_timer_value)

    @classmethod
    def timer(cls, func: Callable) -> Callable:
        def call(*args, **kwargs) -> object:
            t0 = time_module.time()
            result = func(*args, **kwargs)
            t1 = time_module.time()
            timer_key = func.__name__
            cls._increment_time(timer_key, t1 - t0)
            return result
        call.__name__ = func.__name__
        return call


def print_times() -> None:
    """
    print all timer attributes
    :return:
    """
    for attribute_name in Timer.__dict__:
        if attribute_name.startswith('_'):
            continue
        if attribute_name == 'timer':
            continue
        time_value = getattr(Timer, attribute_name)
        print("{0}: {1}".format(attribute_name, time_value))
    return

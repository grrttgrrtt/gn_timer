"""
This is a simple timing module which uses wrappers. Time values are stored at
the class level, so multiple generated timer objects will all increment the same
shared time values. Use it to keep track of how much total time different
function calls are taking.

The Timer class stores running timers in seconds as attributes. The
attributes can have long names, but, for convenience, you can abbreviate
them when writing yor wrappers.

Timer attributes are connected to their abbreviations by the dictionary
timer_dict. You can pre-initialize this dict by using Timer.define_timers().

By default, passing an abbreviation not in timer_dict will create a new timer
with the attribute having the same name as the abbreviation. This behavior
can be disabled by calling Timer._restrict_abbrs() (useful if you make a typo
in an abbr and want your code to throw an error instead of creating a
new timer.

Different timer attributes can be pre-initialized with Timer._define_timers(),
or generated dynamically.

Wrap functions you want to time with @Timer._time('abbr'). This wrapper
increments the timer which corresponds to the abbreviation 'abbr'.

METHODS:

print_times(): prints all timer attributes from class Timer

CHANGELOG:
4-18-19: Created
4-24-19: Updated to use cls.__dict__ instead of a dict attribute
"""
# from typing import Dict
from typing import Callable
import time as time_module


class Timer:
    """
    ATTRIBUTES:
        _allow_dynamic_timer_creation: bool
            governs whether or not new attributes can be created on the fly
            by the _time() function

    METHODS:
    Timer._define_timers(timer_dict: dict) -> None:
        Pre-initializes takes a dictionary of abbreviation: attribute pairs.

    Timer._time(timer_key: str) -> Callable:
        Wrapper function to time other functions. Time in seconds of execution is
        stored in the class attribute indicated by timer_key.

    Timer._restrict_abbrs() -> None:
        Disables dynamically creating attributes and requires all timers to be
        pre-initialized using define_timers().

    """
    # timer_dict: Dict[str, str]
    _allow_dynamic_timer_creation = True

    def __init__(self) -> None:
        return

    @classmethod
    def _define_timers(cls, timer_dict: dict) -> None:
        """
        Dynamically create attributes in the Timer class based on timer_dict
        :param timer_dict: dictionary of timer_key: attribute_name pairs
        :return:
        """
        # for attribute_name in timer_dict.values():
        #     setattr(cls, attribute_name, 0)
        # cls.timer_dict = timer_dict
        cls.__dict__.update(timer_dict)
        return

    @classmethod
    def _increment_time(cls,
                        timer_key: str,
                        sec_to_increment: float) -> None:
        """
        increment the time variable specified by Timer.timer_dict[
        abbreviation].
        :param timer_key: key corresponding to the timer attribute to
        increment
        :param sec_to_increment: number of seconds by which to increment the
        timer attribute
        :return: None
        """
        # timer_value = getattr(cls, cls.timer_dict[timer_key])
        if not hasattr(cls, timer_key) and cls._allow_dynamic_timer_creation:
            setattr(cls, timer_key, 0)
        timer_value = getattr(cls, timer_key)
        new_timer_value = timer_value + sec_to_increment
        # setattr(cls, cls.timer_dict[timer_key], new_timer_value)
        setattr(cls, timer_key, new_timer_value)
        return

    @classmethod
    def _time(cls, timer_key: str) -> Callable:
        """
        wrapper function to decorate functions with.
        Use @Timer.time( 'timer_key')
        :param timer_key: key corresponding to the timer attribute you wish
        to increment
        :return:
        """
        def decorate(func: Callable) -> Callable:
            def call(*args, **kwargs) -> Callable:
                t0 = time_module.time()
                result = func(*args, **kwargs)
                t1 = time_module.time()
                cls._increment_time(timer_key, t1 - t0)
                return result
            return call
        return decorate

    @classmethod
    def _restrict_timers(cls) -> None:
        cls._allow_dynamic_timer_creation = False
        return


def print_times() -> None:
    """
    print all timer attributes
    :return:
    """
    # for attribute_name in self.timer_dict.values():
    for attribute_name in Timer.__dict__:
        if attribute_name.startswith('_'):
            continue
        time_value = getattr(Timer, attribute_name)
        print(f"{attribute_name}: {time_value}")
    return

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
can be disabled by calling Timer.restrict_abbrs() (useful if you make a typo
in an abbr and want your code to throw an error instead of creating a
new timer.

Different timer attributes can be pre-initialized with Timer.define_timers(),
or generated dynamically.

Wrap functions you want to time with @Timer._time('abbr'). This wrapper
increments the timer which corresponds to the abbreviation 'abbr'.

METHODS:
Timer.define_timers(timer_dict: dict) -> None:
    Pre-initializes takes a dictionary of abbreviation: attribute pairs.

Timer.timer(timer_key: str) -> Callable:
    Wrapper function to time other functions. Time in seconds of execution is
    stored in the class attribute indicated by timer_key.

Timer.restrict_abbrs() -> None:
    Disables dynamically creating attributes and requires all timers to be
    pre-initialized using define_timers().

print_times(): prints all timer attributes

CHANGELOG:
4-18-19: Created
4-24-19: Updated to use cls.__dict__ instead of a dict attribute
4-24-19: Branched from gn_timer.py to remove type hints and be python 2
    compatible.
4-30-19: Updated to prevent dynamic timer creation overwriting class functions
5-8-19: Updated wrapper to pass functions names through; useful when
    double-wrapping
"""
import time as time_module


class Timer:
    """
    METHODS:

    Timer.timer() -> Callable:
        Wrapper function to time other functions. Time in seconds of execution is
        stored in the class attribute indicated by timer_key.


    """
    def __init__(self):
        return

    def __setattr__(self, name, value):
        if name == 'timer':
            raise Exception("cannot overwrite timer")
        self.__dict__[name] = value
        return

    @classmethod
    def _increment_time(cls, timer_key, sec_to_increment):
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
        return

    @classmethod
    def timer(cls, func):
        def call(*args, **kwargs):
            t0 = time_module.time()
            result = func(*args, **kwargs)
            t1 = time_module.time()
            timer_key = func.__name__
            cls._increment_time(timer_key, t1 - t0)
            return result
        call.__name__ = func.__name__
        return call


def print_times():
    """
    print all timer attributes
    :return:
    """
    # for attribute_name in self.timer_dict.values():
    for attribute_name in Timer.__dict__:
        if attribute_name.startswith('_'):
            continue
        if attribute_name == 'timer':
            continue
        time_value = getattr(Timer, attribute_name)
        print("{0}: {1}".format(attribute_name, time_value))
    return

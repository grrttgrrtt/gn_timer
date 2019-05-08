# gn_timer
Simple module for python to time pieces of your code

There is probably an already existing python module for this. I wrote this one to be simple and to learn about wrappers and function decorators.

To use, import either gn_timer (for python 3) or gn_timer_py2 (for python 2).

Due to updates, gn_typer_py2 now works differently than gn_timer; it functions more simply but with fewer options.

Time values are stored at
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

Timer.time(timer_key: str) -> Callable:
    Wrapper function to time other functions. Time in seconds of execution is
    stored in the class attribute indicated by timer_key.

Timer.restrict_abbrs() -> None:
    Disables dynamically creating attributes and requires all timers to be
    pre-initialized using define_timers().

print_times(): prints all timer attributes

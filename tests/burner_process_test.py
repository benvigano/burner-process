import os
from burner_process import processify
from sample_functions import func, get_pid, get_parent_pid


inputs = [4, 25, 100, 32.01, 18298]


def test_processify() -> None:
    processified_func = processify(func)

    for x in inputs:
        assert processified_func(x) == func(x)


def test_pid() -> None:
    processified_get_pid = processify(get_pid)
    processified_get_pid() != get_pid()


def test_parent_pid() -> None:
    processified_get_parent_pid = processify(get_parent_pid)
    processified_get_parent_pid() != get_parent_pid()
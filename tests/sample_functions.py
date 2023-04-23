import math
import os


def func(x):
    return math.sqrt(x)


def get_pid():
    return os.getpid()


def get_parent_pid():
    return os.getppid()
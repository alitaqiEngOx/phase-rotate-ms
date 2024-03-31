import contextlib
import os
import sys


@contextlib.contextmanager
def block_logging() -> None:
    """
    """
    sys.stdout = open(os.devnull, 'w')
    yield
    sys.stdout = sys.__stdout__
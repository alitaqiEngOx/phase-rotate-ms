import contextlib
import logging
import os
import shutil
import sys
from pathlib import Path


@contextlib.contextmanager
def block_logging() -> None:
    """
    Context manager function to block typing into the terminal.
    """
    sys.stdout = open(os.devnull, 'w')
    yield
    sys.stdout = sys.__stdout__

def copy_dir(
        original_dir: Path, target_dir: Path,
        *, name: str, rm: bool=False
) -> None:
    """
    Copies a directory "original_dir" into a target path
    "target_dir". Overwriting is blocked unless --rm is
    flagged in the terminal comand.
    """
    target_dir = original_dir.parent.joinpath(
        name, f"phase_rotated_{original_dir.name}"
    )
    try:
        shutil.copytree(
            str(original_dir), str(target_dir)
        )
    except FileExistsError:
        if rm:
            logging.info(f"\nOverwriting {str(target_dir.name)}.\n")
            shutil.rmtree(target_dir)
            shutil.copytree(
                str(original_dir), str(target_dir)
            )
        else:
            raise FileExistsError(f"Overwriting {str(target_dir.name)} blocked.")

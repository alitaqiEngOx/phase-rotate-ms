import argparse
import logging
import time
from pathlib import Path


def assers_errors(args: argparse.Namespace) -> None:
    """
    """
    if not Path(args.ms_dir).exists():
        raise FileNotFoundError(f"{args.ms_dir} does not exist.")

def main() -> None:
    """
    """

def parse_args() -> argparse.Namespace:
    """
    """
    parser = argparse.ArgumentParser(
        description="Radio astronomy MeasurementSet phase rotator.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "ms_dir",
        type=str,
        help="input MeasurementSet directory."
    )
    parser.add_argument(
        "new_phase_centre",
        type=float,
        nargs=2,
        help="new phase centre in RA DEC."
    )
    parser.add_argument(
        "--name",
        type=str,
        default="output",
        help="name for output dir (default=output)."
    )
    parser.add_argument(
        "--rm",
        type=bool,
        action="store_true",
        help="overwrite existing file with same name"
    )
    return parser.parse_args()


if __name__ == "__main__":
    start_time = time.time()
    main()
    logging.info(f"Full time = {time.time() - start_time} s")
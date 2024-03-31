import argparse
import logging
import time
from pathlib import Path

from astropy.coordinates import SkyCoord

from operations import pipeline


def assert_errors(args: argparse.Namespace) -> None:
    """
    """
    if not Path(args.ms_dir).exists():
        raise FileNotFoundError(f"{args.ms_dir} does not exist.")

def main() -> None:
    """
    """
    args = parse_args()
    assert_errors(args)
    
    pipeline.process_data(
        Path(args.ms_dir), 
        SkyCoord(
            args.new_phase_centre[0], 
            args.new_phase_centre[1], 
            unit="deg"
        ),
        name=args.name, 
        rm=args.rm
    )

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
        help="new phase centre in RA DEC (deg)."
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
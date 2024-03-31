from pathlib import Path

from astropy.coordinates import SkyCoord


def process_data(
        ms_dir: Path, new_phase_centre: SkyCoord,
        *, name: str="output", rm: bool=False
):
    """
    """
    return
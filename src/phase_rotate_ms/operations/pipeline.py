from pathlib import Path

from astropy.coordinates import SkyCoord

from operations import ms


def process_data(
        ms_dir: Path, new_phase_centre: SkyCoord,
        *, name: str="output", rm: bool=False
):
    """
    """
    ms_original = ms.read(ms_dir)
    return
from pathlib import Path

from astropy.coordinates import SkyCoord
from numpy.typing import NDArray

from operations import ms


def process_data(
        ms_dir: Path, new_phase_centre: SkyCoord,
        *, name: str="output", rm: bool=False
) -> None:
    """
    """
    ms_original = ms.read(ms_dir)

def rotate_uvw(
        original_phase_centre: SkyCoord, new_phase_centre: SkyCoord,
        original_uvw: NDArray
) -> NDArray:
    """
    """
    return

def rotate_visibilities(
        original_phase_centre: SkyCoord, new_phase_centre: SkyCoord,
        initial_channel: float, channel_step: float,
        original_uvw: NDArray, original_visibilities: NDArray
) -> NDArray:
    """
    """
    return
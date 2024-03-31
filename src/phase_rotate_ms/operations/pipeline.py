from pathlib import Path

import numpy as np
import ska_sdp_func.visibility as pfl_vis
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
    original_uvw_dims = len(original_uvw.shape)
    while len(original_uvw.shape) < 3:
        original_uvw = np.expand_dims(original_uvw, axis=0)
    new_uvw = np.empty(original_uvw.shape)
    pfl_vis.phase_rotate_uvw(
        original_phase_centre, new_phase_centre,
        original_uvw, new_uvw
    )
    while len(new_uvw.shape) > original_uvw_dims:
        new_uvw = new_uvw[0]
    return new_uvw

def rotate_visibilities(
        original_phase_centre: SkyCoord, new_phase_centre: SkyCoord,
        initial_channel: float, channel_step: float,
        original_uvw: NDArray, original_visibilities: NDArray
) -> NDArray:
    """
    """
    return
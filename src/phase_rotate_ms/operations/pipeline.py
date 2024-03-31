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
    ini_chan, inc_chan = ms_original.get_channels(ms_dir)
    new_uvw = rotate_uvw(
        ms_original.phase_centre, new_phase_centre, ms_original.uvw
    )
    new_visibilities = rotate_visibilities(
        ms_original.phase_centre, new_phase_centre,
        ini_chan, inc_chan, ms_original.uvw, ms_original.visibilities
    )

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
    original_vis_dims = len(original_visibilities.shape)
    while len(original_visibilities.shape) < 4:
        original_visibilities = np.expand_dims(
            original_visibilities, axis=0
        )
    new_visibilities = np.empty(original_visibilities.shape)
    pfl_vis.phase_rotate_vis(
        original_phase_centre, new_phase_centre,
        initial_channel, channel_step, original_uvw,
        original_visibilities, new_visibilities
    )
    while len(new_visibilities.shape) > original_vis_dims:
        new_visibilities = new_visibilities[0]
    return new_visibilities
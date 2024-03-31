from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
from astropy.coordinates import SkyCoord
from casacore.tables import table
from numpy.typing import NDArray

from utils import tools


@dataclass
class MS:
    """
    """

    dir: Path
    """"""

    @property
    def phase_centre(self) -> SkyCoord:
        """
        MeasurementSet phase centre.
        """
        try:
            with tools.block_logging():
                phase_centre = table(
                    str(self.dir.joinpath("FIELD"))
                ).getcol("PHASE_DIR")
        except:
            raise FileNotFoundError(
                "expected a 'FIELD' table with a 'PHASE_DIR' column"
            )
        if np.array(phase_centre).shape != (1, 1, 2):
            raise ValueError("unsupported phase centre definition")
        return SkyCoord(
            phase_centre[0][0][0], phase_centre[0][0][1], unit="rad"
        )

    @property
    def uvw(self) -> NDArray:
        """
        MeasurementSet UVW coordinates.
        """
        try:
            with tools.block_logging():
                uvw = table(self.ms_dir).getcol("UVW")
        except:
            raise FileNotFoundError("expected a 'UVW' column")
        if len(np.asarray(uvw).shape) > 3:
            raise ValueError("unsupported UVW with more than 3 dimensions")
        if np.asarray(uvw).shape[-1] != 3:
            raise ValueError(
                "there must be 3 positional coordinates per observation"
            )
        return np.asarray(uvw)

    @property
    def visibilities(self) -> NDArray:
        """
        MeasurementSet Visiblities.
        """
        try:
            with tools.block_logging():
                visibilities = table(self.ms_dir).getcol("DATA")
        except:
            raise FileNotFoundError("expected a 'DATA' column")
        if len(np.asarray(visibilities).shape) > 4:
            raise ValueError("unsupported DATA with more than 4 dimensions")
        return np.asarray(visibilities)

    @classmethod
    def writer(
            cls, dir: Path, phase_centre: SkyCoord, 
            uvw: NDArray, visibilities: NDArray
    ) -> MS:
        """
        """
        return cls(dir, phase_centre, uvw, visibilities)

    def get_channels(dir: Path) -> Tuple[float, float]:
        """
        """
        if not dir.exists():
            raise FileNotFoundError(f"{str(dir)} does not exist.")
        with tools.block_logging():
            try:
                chan_freq = table(
                    str(dir.joinpath("SPECTRAL_WINDOW"))
                ).getcol("CHAN_FREQ")
            except:
                raise FileNotFoundError(
                    "expected a 'SPECTRAL_WINDOW' table with a 'CHAN_FREQ' column"
                )
        chan_freq = chan_freq.flatten()
        return chan_freq[0], chan_freq[1]-chan_freq[0]


def read(dir: Path) -> MS:
    """
    """
    return MS(dir)

def write(
        dir: Path, phase_centre: SkyCoord,
        uvw: NDArray, visibilities: NDArray
) -> None:
    """
    """
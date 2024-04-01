from pathlib import Path
from typing import Optional, Tuple

import numpy as np
from astropy.coordinates import SkyCoord
from casacore.tables import table
from numpy.typing import NDArray

from utils import tools


class MS:
    """
    """

    def __init__(
            self, dir: Path, phase_centre: Optional[SkyCoord], 
            uvw: Optional[NDArray], visibilities: Optional[NDArray],
            *, manual_define: bool=False
    ):
        """
        """
        self.dir = dir
        self._phase_centre = phase_centre
        self._uvw = uvw
        self._visibilities = visibilities
        self.manual_define = manual_define

    @property
    def phase_centre(self) -> SkyCoord:
        """
        """
        if self.manual_define:
            return self._phase_centre
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
        """
        if self.manual_define:
            return self._uvw
        try:
            with tools.block_logging():
                uvw = table(str(self.dir)).getcol("UVW")
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
        """
        if self.manual_define:
            return self._visibilities
        try:
            with tools.block_logging():
                visibilities = table(str(self.dir)).getcol("DATA")
        except:
            raise FileNotFoundError("expected a 'DATA' column")
        if len(np.asarray(visibilities).shape) > 4:
            raise ValueError("unsupported DATA with more than 4 dimensions")
        return np.asarray(visibilities, dtype=np.complex128)

    @classmethod
    def write_mode(
            cls, dir: Path, phase_centre: SkyCoord, 
            uvw: NDArray, visibilities: NDArray
    ):
        """
        """
        return cls(
            dir, phase_centre, uvw, visibilities, manual_define=True
        )

    def get_channels(self, dir: Path) -> Tuple[float, float]:
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
        if len(chan_freq) == 1:
            return chan_freq[0], 0.
        return chan_freq[0], chan_freq[1]-chan_freq[0]

    def generate_new(self) -> None:
        """
        """


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
    ms = MS.manual_define(dir, phase_centre, uvw, visibilities)
    ms.generate_new()
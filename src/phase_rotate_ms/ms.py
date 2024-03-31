import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from astropy.coordinates import SkyCoord
from casacore.tables import table


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
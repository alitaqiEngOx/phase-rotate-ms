from pathlib import Path
from typing import Optional, Tuple

import numpy as np
from astropy.coordinates import SkyCoord
from casacore.tables import table
from numpy.typing import NDArray

from utils import tools


class MS:
    """
    Class for MeasurementSets.
    """

    def __init__(
            self, dir: Path, phase_centre: Optional[SkyCoord]=None, 
            uvw: Optional[NDArray]=None, visibilities: Optional[NDArray]=None,
            *, manual_define: bool=False
    ):
        """
        Initiator function defining the various attributes as None types. Also,
        "manual_define" is False by default. These parameters are then defined
        either by:
        
        1- directly reading from the MeasurementSet when calling the 
           class directly (manual_define=False), or
        2- calling the class through the write_mode() class method, thereby 
           manually defining the values of the parameters. This means that the
           class instance is generated without the need to have a corresponding
           MeasurementSet existing (manual_define=True).
        """
        self.dir = dir
        self._phase_centre = phase_centre
        self._uvw = uvw
        self._visibilities = visibilities
        self.manual_define = manual_define

    @property
    def phase_centre(self) -> SkyCoord:
        """
        Phase centre of the data.
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
        UVW coordinates.
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
        Visibilities.
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
        Class method which when used to create a class instance, the various
        attributes should be defined manually (i.e., the MeasurementSet does
        not have to exist for a class instance to be generated).
        """
        return cls(
            dir, phase_centre, uvw, visibilities, manual_define=True
        )

    def get_channels(self, dir: Path) -> Tuple[float, float]:
        """
        Returns the initial channel and the step between channels. Raises
        an error if the class is called on write_mode and the corresponding
        MeasurementSet does not exist yet. In such case, run self.generate_new()
        first.
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

    def generate_new(
            self, ms_dir: Path, *, name: str="output", rm: bool=False
    ) -> None:
        """
        Where a class instance exists but not its corresponding MeasurementSet
        (e.g., when calling MS through the write_mode() class method), this method
        generates a new MeasurementSet by copying another MeasurementSet at "ms_dir"
        and writes the class attribues as data into this newly copied directory.
        """
        tools.copy_dir(ms_dir, self.dir, name=name, rm=rm)
        with tools.block_logging():
            main_table = table(str(self.dir), readonly=False)
            main_table.putcol("UVW", self.uvw)
            main_table.putcol("DATA", self.visibilities)
            main_table.close()
            field_table = table(str(self.dir.joinpath("FIELD")), readonly=False)
            existing_phase_centre_dims = len(
                np.asarray(field_table.getcol("PHASE_DIR")).shape
            )
            new_phase_centre = np.asarray([
                self.phase_centre.ra.rad, self.phase_centre.dec.rad
            ])
            while len(new_phase_centre.shape) < existing_phase_centre_dims:
                new_phase_centre = np.expand_dims(new_phase_centre, axis=0)
            field_table.putcol("PHASE_DIR", new_phase_centre)
            field_table.close()


def read(dir: Path) -> MS:
    """
    Generates a normal instance of the MS class.
    """
    return MS(dir)

def write(
        dir: Path, ms_dir: Path, phase_centre: SkyCoord,
        uvw: NDArray, visibilities: NDArray, 
        *, name: str="output", rm: bool=False
) -> None:
    """
    Generates a write_mode() instance of the MS class and passes valeues
    for the different attributes directly.
    """
    ms = MS.write_mode(dir, phase_centre, uvw, visibilities)
    ms.generate_new(ms_dir, name=name, rm=rm)
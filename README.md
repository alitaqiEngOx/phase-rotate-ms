# phase-rotate-ms





This software phase rotates UVW and visibility data in radio astronomy MeasurementSets. It geerates a copy of your input MeasurementSet with the newly phase rotated data along with the updated phase tracking centre.

Libraries required:

- astropy;
- numpy;
- python-casacore;
- ska-sdp-func (https://gitlab.com/ska-telescope/sdp/ska-sdp-func).

Usage is currently as follows:
Clone the repository then, from the parent directory, run the following command:

```
$ python3 ./src/phase_rotate_ms [options] dir/to/your/measurement_set.ms {new RA in deg} {new DEC in deg}
```

The options include ```--name [NAME]``` to specify the name of the output directory, and ```--rm``` to enable overwriting the output directory in case it already exists.

The output directory will be generated in the same directory as your input MeasurementSet, in a sub-directory whose name matches the value you assign to ```--name```.

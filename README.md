cofe-python-analysis-tools
==========================

python tools for cofe data analysis including demodulation, pointing mapmaking etc
repository:
https://github.com/ucsbdeepspace/cofe-python-analysis-tools/

## How to run map-making on COFE

* Raw files produced by Peter in .pkl format contains data, timing information and pointing in local coordinates (azimuth, elevation)
* First we need to compute the Equatorial pointing, in the same process we also extract the data for 1 channel we want to use for mapmaking (hardwritten in the script), this is achieved using `compute_pointing.py` in `utils_zonca/pointing`:
        
        python compute_pointing.py input_file_oneperday.pkl
This produces one `.h5` file with the same name and in the same path as the original `.pkl` file.
* Next we want to concatenate all files to be used for the same mapmaking run:
        
        python concatenate_h5.py file1.h5 file2.h5 file3.h5
The script produces a single `HDF5` file: `concatenated.h5`, in the same folder, to be renamed.
* The `HDF5` file is ready for mapmaking, download `dst` (<https://github.com/zonca/dst>), follow instructions in `README.md` to build it, then prepare a configuration file based on `roof_512.cfg` by changing the file path.
Run destriping with:

        mpirun -np 3 python dst.py yourconfig.cfg
Finally convert the output maps to `FITS` with:

        python plotmaps.py dstoutputfolder

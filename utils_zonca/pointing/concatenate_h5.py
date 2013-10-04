"""Concatenate several HDF5 generated with compute_pointing"""

import sys
import h5py
import os.path

filenames = sys.argv[1:]
output_filename = os.path.join(os.path.dirname(filenames[0]),"concatenated.h5")

with h5py.File(output_filename, mode="w") as output_file:

    with h5py.File(filenames[0], mode="r") as first_file: 
        output_file.create_dataset("data", data=first_file["data"], maxshape=(None,))

    for filename in filenames[1:]:
        print filename
        with h5py.File(filename, mode="r") as h5_file: 
            prev_length = len(output_file["data"])
            output_file["data"].resize((prev_length+len(h5_file["data"]),))
            output_file["data"][prev_length:] = h5_file["data"]

print "Completed"

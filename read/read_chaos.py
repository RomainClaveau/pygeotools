#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of pygeotools

from read_checks import *

# Custom errors
class InvalidArgumentError(Exception): pass
class ColumnMismatchError(Exception): pass

def read_chaos(path_to_hdf5: str) -> dict | Exception:
    """    
    Read CHAOS observations and return it as a model.

    :input:
        - (str) path_to_hdf5
    
    :output:
        - (dict) dict_model
    """

    # Checking arguments
    is_valid = read_checks([
        {"variable": path_to_hdf5, "type": str, "conditions": "is_file,is_hdf5"}
    ])

    if not is_valid:
        raise InvalidArgumentError("Arguments are not valid.")

    expected_keys_lvl_1 = set(['dgnm', 'gnm', 'times', 'var_dgnm', 'var_gnm'])
    
    with h5py.File(path_to_hdf5, "r") as f:
        if not f.keys() == expected_keys_lvl_1:
            raise ColumnMismatchError("Columns mismatching.")

        return {
            "type": "observations",
            "domain": "spectral",
            "name": "chaos",
            "times": f["times"][:],
            "MF": f["gnm"][:],
            "SV": f["dgnm"][:],
            "var_MF": f["var_gnm"],
            "var_SV": f["var_dgnm"]
        }
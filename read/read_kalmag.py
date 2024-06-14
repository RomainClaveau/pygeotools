#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of pygeotools

import numpy

from read_checks import *

# Custom errors
class InvalidArgumentError(Exception): pass
class ColumnMismatchError(Exception): pass

def read_kalmag(path_to_hdf5: str) -> dict | Exception:
    """    
    Read KALMAG observations and return it as a model.

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

    expected_keys_lvl_1 = set(['MF', 'SV', 'times'])
    
    with h5py.File(path_to_hdf5, "r") as f:
        if not f.keys() == expected_keys_lvl_1:
            raise ColumnMismatchError("Columns mismatching.")

        return {
            "type": "observations",
            "domain": "spectral",
            "name": "kalmag",
            "times": f["times"][:],
            "MF": numpy.mean(f["MF"][:], axis=0),
            "SV": numpy.mean(f["SV"][:], axis=0),
            "var_MF": numpy.std(f["MF"], axis=0),
            "var_SV": numpy.std(f["SV"], axis=0),
        }
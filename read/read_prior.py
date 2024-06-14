#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of pygeotools

from read_checks import *

# Custom errors
class InvalidArgumentError(Exception): pass
class ColumnMismatchError(Exception): pass

def read_prior(path_to_hdf5: str) -> dict | Exception:
    """    
    Read prior and return it as a model.

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
    
    expected_keys_lvl_1 = set(['ER', 'MF', 'U', 'times'])
    
    with h5py.File(path_to_hdf5, "r") as f:
        if not f.keys() == expected_keys_lvl_1:
            raise ColumnMismatchError("Columns mismatching.")
        
        return {
            "type": "priors",
            "domain": "spectral",
            "times": f["times"][:],
            "MF": f["MF"][:],
            "U": f["U"][:],
        }
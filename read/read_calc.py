#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of pygeotools

import numpy

from read_checks import *

# Custom errors
class InvalidArgumentError(Exception): pass
class ColumnMismatchError(Exception): pass

def read_calc(path_to_hdf5: str) -> dict | Exception:
    """    
    Read pygeodyn's output file and return it as a model.

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
    
    expected_keys_lvl_1 = set(['analysed', 'computed', 'forecast', 'misfits'])
    expected_keys_lvl_2 = set(['ER', 'MF', 'SV', 'U', 'times'])
    
    with h5py.File(path_to_hdf5, "r") as f:
        if not f.keys() == expected_keys_lvl_1:
            raise ColumnMismatchError("Columns mismatching.")
        
        if not f["computed"].keys() == expected_keys_lvl_2:
            raise ColumnMismatchError("Columns mismatching.")

        return {
            "type": "calculations",
            "domain": "spectral",
            "times": f["computed"]["times"][:],
            "MF": numpy.mean(f["computed"]["MF"][:], axis=0),
            "SV": numpy.mean(f["computed"]["SV"][:], axis=0),
            "U": numpy.mean(f["computed"]["U"][:], axis=0),
            "var_MF": numpy.std(f["computed"]["MF"][:], axis=0),
            "var_SV": numpy.std(f["computed"]["SV"][:], axis=0),
            "var_U": numpy.std(f["computed"]["U"][:], axis=0),
        }
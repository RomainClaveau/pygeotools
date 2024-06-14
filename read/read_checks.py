#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of pygeotools

import os
import h5py

# Custom errors
class EmptyError(Exception): pass
class NotInConditionsListError(Exception): pass

def read_checks(vars_to_check: list | tuple) -> bool | Exception:
    """
    General routine for checking arguments.

    Read a list of arguments, testing the type (str, int, etc.)
    and the condition (filename, positive number, etc.) and return
    the overall status accordingly.

    :input:
        - (list) vars_to_check: List of variables to check.

    :output:
        - (bool) status: Whether the list of arguments is valid or not.

    :flags:
        - is_file   : Checking if the path is linked to an existing file.
        - is_dir    : Checking if the path is linked to an existing directory.
        - is_hdf5   : Checking if the file is a valid hdf5.

    :examples:
        >>> my_var = "/path/to/my/hdf5/file.hdf5"
        >>> read_checks([{"variable": my_var, "type": str, "conditions": "is_file,is_hdf5"}])
    """

    if not isinstance(vars_to_check, (list, tuple)):
        raise TypeError("Arguments must be organized in a list or in a tuple.")

    if len(vars_to_check) == 0:
        raise EmptyError("List of arguments is empty.")
    
    # List of available conditions
    list_of_conditions = {
        "is_file": lambda x: os.path.isfile(x),
        "is_dir": lambda x: os.path.isdir(x),
        "is_hdf5": lambda x: h5py.is_hdf5(x)
    }
    
    # Browsing through the variables
    for arg in vars_to_check:
        if arg.keys() != set(["variable", "type", "conditions"]):
            raise KeyError("Keys mismatching.")
        
        variable = arg["variable"]
        var_type = arg["type"]
        conditions = arg["conditions"]

        # Checking the type
        if not isinstance(variable, (var_type)):
            return False

        # Checking the conditions
        if conditions.find(",") != 1:
            conditions = conditions.split(",")
        else:
            conditions = [conditions]

        # Browsing through the conditions
        for condition in conditions:
            if condition not in list_of_conditions.keys():
                raise NotInConditionsListError("The specified condition was not found in the list.")

            # Checking the condition
            if list_of_conditions[condition](variable) is False:
                return False
            
    return True
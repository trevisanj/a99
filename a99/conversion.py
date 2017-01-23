"""Conversion routines"""


__all__ = [
"str2bool", "bool2str", "chunk_string", "ordinal_suffix", "seconds2str", "make_fits_keys_dict",
"valid_fits_key", "eval_fieldnames", "expr_to_fieldname", "module_to_dict",     ]


import numpy as np
import re



def str2bool(s):
    """Understands "T"/"F" only (case-sensitive). To be used for file parsing."""
    if s == "T":
        return True
    elif s == "F":
        return False
    raise ValueError("I don't understand '{0!s}' as a logical value".format(s))


def bool2str(x):
    """Converts bool variable to either "T" or "F"."""
    assert isinstance(x, bool)
    return "T" if x else "F"


def chunk_string(string, length):
    """
    Splits a string into fixed-length chunks.

    This function returns a generator, using a generator comprehension. The
    generator returns the string sliced, from 0 + a multiple of the length
    of the chunks, to the length of the chunks + a multiple of the length
    of the chunks.

    Reference: http://stackoverflow.com/questions/18854620
    """
    return (string[0 + i:length + i] for i in range(0, len(string), length))


def ordinal_suffix(i):
    """Returns 'st', 'nd', or 'rd'."""
    return 'st' if i == 1 else 'nd' if i == 2 else 'rd' if i == 3 else 'th'


def seconds2str(seconds):
    """Returns string such as 1h 05m 55s."""

    if seconds < 0:
        return "{0:.3g}s".format(seconds)
    elif np.isnan(seconds):
        return "NaN"
    elif np.isinf(seconds):
        return "Inf"

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h >= 1:
        return "{0:g}h {1:02g}m {2:.3g}s".format(h, m, s)
    elif m >= 1:
        return "{0:02g}m {1:.3g}s".format(m, s)
    else:
        return "{0:.3g}s".format(s)


def make_fits_keys_dict(keys):
    """
    Returns a dictionary to translate to unique FITS header keys up to 8 characters long

    This is similar to Windows making up 8-character names for filenames that
    are longer than this

    "The keyword names may be up to 8 characters long and can only contain
    uppercase letters A to Z, the digits 0 to 9, the hyphen, and the underscore
    character." [1]

    Arguments:
        keys -- list of strings

    Returns:
        dictionary whose keys are the elements in the "keys" argument, and whose
        values are made-up uppercase names

    References:
        [1] http://fits.gsfc.nasa.gov/fits_primer.html
    """

    key_dict = {}
    new_keys = []
    for key in keys:
        # converts to valid FITS key according to reference [1] above
        fits_key = valid_fits_key(key)
        num_digits = 1
        i = -1
        i_max = 9
        while fits_key in new_keys:
            i += 1
            if i > i_max:
                i = 0
                i_max = i_max * 10 + 9
                num_digits += 1
            fits_key = fits_key[:(8 - num_digits)] + (("%0{0:d}d".format(num_digits)) % i)

        key_dict[key] = fits_key
        new_keys.append(fits_key)

    return key_dict


def valid_fits_key(key):
    """
    Makes valid key for a FITS header

    "The keyword names may be up to 8 characters long and can only contain
    uppercase letters A to Z, the digits 0 to 9, the hyphen, and the underscore
    character." (http://fits.gsfc.nasa.gov/fits_primer.html)
    """

    ret = re.sub("[^A-Z0-9\-_]", "", key.upper())[:8]
    if len(ret) == 0:
        raise RuntimeError("key '{0!s}' has no valid characters to be a key in a FITS header".format(key))
    return ret


def eval_fieldnames(string_, varname="fieldnames"):
    """Evaluates string_, must evaluate to list of strings. Also converts field names to uppercase"""
    ff = eval(string_)
    if not isinstance(ff, list):
        raise RuntimeError("{0!s} must be a list".format(varname))
    if not all([isinstance(x, str) for x in ff]):
        raise RuntimeError("{0!s} must be a list of strings".format(varname))
    ff = [x.upper() for x in ff]
    return ff


def expr_to_fieldname(expr):
    """Keeps the rightmost part of the class name after the "_" """
    return expr[:expr.index("(")].strip().split("_")[-1]


def module_to_dict(module):
    """Creates a dictionary whose keys are module.__all__

    Returns: {"(attribute name)": attribute, ...}
    """

    lot = [(key, module.__getattribute__(key)) for key in module.__all__]
    ret = dict(lot)
    return ret


"""
Data type - object type + label OR object type without label
"""
DTYPE = tuple[type, str] | type

"""
Data type - multiple types OR just one type descriptor.
For multiple types, you must provide label
"""
DTYPES = tuple[tuple[type, str]] | DTYPE

"""
Consumer ID - data type it consumes
"""
CONSID = tuple[DTYPES, str]

DTYPE_LABEL_REMAP = DTYPES | str | tuple[str] | list[str]


def ismultiple(dt: DTYPES):
    """
    Checks if DTYPE is a collection of acceptable DTYPEs
    """
    if not isinstance(dt, tuple):
        return False

    return all(map(lambda x: isinstance(x, tuple) and isinstance(x[0], type) and isinstance(x[1], str), dt))


def validate_scalar_data(data, dt: DTYPE):
    """
    Checks if scalar data is type of provided dtype.
    Do not provide multiple dtype value, instead use validate_data to check for all possible dtypes
    """
    if isinstance(dt, tuple):
        assert len(dt) == 2

        dtype, label = dt
        return isinstance(data, dtype) and (not hasattr(data, '__DATALABEL__') or data.__DATALABEL__ == dt[1])
    else:
        return isinstance(data, dt)


def validate_data(data, dt: DTYPES):
    """
    Checks if data is type of provided dtype
    """
    if ismultiple(dt):
        # multiple data types
        return any(map(validate_scalar_data, dt))
    return validate_scalar_data(data, dt)


def iterate_dtypes(dtypes: DTYPES):
    if ismultiple(dtypes):
        for dtype in dtypes:
            yield dtype
    elif isinstance(dtypes, tuple) and isinstance(dtypes[0], type) and isinstance(dtypes[1], str):
        yield dtypes
    else:
        yield dtypes, ""


def repr_dtype(dtype: DTYPES):
    if ismultiple(dtype):
        return ', '.join(map(repr_dtype, dtype))
    elif isinstance(dtype, tuple):
        dtype_cls, dtype_id = dtype
    else:
        dtype_cls = dtype
        dtype_id = ''

    return f"({dtype_cls.__name__}, '{dtype_id}')"


def remap_dtype(dtype: DTYPES, override: DTYPE_LABEL_REMAP):
    is_multiple = ismultiple(dtype)
    is_override_multiple = ismultiple(override)
    is_tuple = not is_multiple and isinstance(dtype, tuple)and isinstance(dtype[0], type)
    is_tuple_override = not is_override_multiple and isinstance(override, tuple) and isinstance(override[0], type)

    # modify by inserting data label
    if is_tuple_override or is_override_multiple:
        # no need to modify; just override as-is
        new_dtype = override

    elif is_multiple:
        # multiple dtype labels override
        new_dtype = list(map(list, dtype))
        assert isinstance(override, (tuple, list)) and len(override) == len(dtype), "must provide a string list equal to the dtypes"

        for i, pc_key in enumerate(override):
            new_dtype[i][1] = pc_key

        # convert lists back to tuples
        new_dtype = map(tuple, new_dtype)
    else:
        if is_tuple:
            # replace just data label
            new_dtype = list(dtype)
        else:
            new_dtype = [dtype, None]

        assert isinstance(override, str), "must provide full dtype override or data label"

        new_dtype[1] = override

    # convert back to DTYPE
    return tuple(new_dtype)

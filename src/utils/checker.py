import inspect

from src.exceptions.argument_exception import ArgumentException


def check_arg(arg, correct_type, check_none: bool = False):
    if check_none and arg is not None or not check_none:
        if not isinstance(arg, correct_type):
            arg_name = get_arg_name(arg)
            raise ArgumentException(
                f"Argument '{arg_name}' must be of type {correct_type.__name__}, not {type(arg).__name__}"
            )


def check_max_len(arg, max_len: int):
    if len(arg) > max_len:
        arg_name = get_arg_name(arg)
        raise ArgumentException(f"Length of argument {arg_name} exceeds the maximum allowed limit of 255 characters (current length: {len(arg)}).")

def check_exact_length(arg, length: int):
    if len(arg) != length:
        arg_name = get_arg_name(arg)
        raise ArgumentException(
            f"Arg {arg_name} must be {length} length string."
        )


def get_arg_name(arg):
    try:
        frame = inspect.currentframe().f_back.f_back
        arg_name = [k for k, v in frame.f_locals.items() if v is arg][0]
    except Exception:
        arg_name = ""
    return arg_name

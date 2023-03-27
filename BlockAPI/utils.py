from typing import Sized, Union, List

PLAIN_TEXT = "plain_text"
MRKDWN = "mrkdwn"
DEFAULT = ""
DANGER = "danger"
PRIMARY = "primary"

ALL_TYPES = {PLAIN_TEXT, MRKDWN}


def check_none(_obj):
    if _obj is None:
        raise ValueError(f"{type(_obj)} is None")


def check_length(_obj: Sized, _min: int, _max: int):
    if _min > _max:
        raise ArithmeticError(f"Malformed range.")
    if not _min <= len(_obj) <= _max:
        raise ValueError(f"The property is outside range boundary. Expected in [{_min}, {_max}], is {len(_obj)}.")


def check_valid_type(_t: str, _types: Union[List[str], str] = None):
    if not _types:
        _types = ALL_TYPES
    else:
        if isinstance(_types, list):
            if not all(list(map(lambda x: x in ALL_TYPES, _types))):
                raise AttributeError(f"Wrong text type(s), can only be {ALL_TYPES}.")

    if _t not in _types:
        raise ValueError(f"Wrong text type. Expected {_types} got {_t} instead.")


def check_style(_style: str):
    if _style != DEFAULT and _style != DANGER and _style != PRIMARY:
        raise ValueError(f"Wrong button style. Expected {DANGER} or {PRIMARY} got {_style} instead.")


def check_filter_options(_filter_options: List[str]):
    _ops = ["im", "mpim", "private", "public"]
    if not all(list(map(lambda x: x in _ops, _filter_options))):
        raise ValueError(f"Wrong include options, can only be {_ops}.")


def check_config_options(_config: List[str]):
    if not _config:
        raise ValueError("Config list is empty.")
    else:
        if "on_enter_pressed" not in _config and "on_character_entered" not in _config:
            raise ValueError("Invalid configuration values. Must be on_enter_pressed, on_character_entered or both.")


def check_is_number(_num: str, is_decimal_allowed: bool):
    try:
        int(_num)
    except ValueError:
        try:
            float(_num)
        except ValueError:
            raise ValueError("Only integers and floats are allowed.")
        else:
            if not is_decimal_allowed:
                raise ValueError("Decimal is not allowed. To enable decimal values set is_decimal_allowed True.")


def get_number_from_string(_value) -> Union[int, float]:
    try:
        return int(_value)
    except ValueError:
        return float(_value)

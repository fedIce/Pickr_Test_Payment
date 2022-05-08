from typing import Any

from app.pay_stack.errors import InvalidDataError


def extract_value(data: dict[str, Any], index: str):
    return data[f'{index}'] if f'{index}' in data else None 

def validate_missing_keys(data: dict[str, Any], keys: list):
    missing_keys = []
    for key in keys:
        if key not in data.keys():
            missing_keys.append(key)

    if len(missing_keys) > 0:
        raise InvalidDataError(f"Object is missing keys {missing_keys}")
    else:
        return data
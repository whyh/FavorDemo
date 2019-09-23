from typing import Dict, Optional, Callable, Any
from ast import literal_eval

__all__ = ("encode", "decode", "Args", "NotFoundError")

EQUAL = "="
AND = "_"
MAGIC_SIGN = "-_-"
MAGIC_SIGN_LEN = len(MAGIC_SIGN)


class NotFoundError(KeyError):
    pass


class Args:
    def __init__(self, args: Optional[Dict[str, str]] = None):
        self.args = {} if args is None else args

    def get(self, key: str, type: Optional[Callable] = str, default: Optional[Any] = None) -> Any:
        try:
            value = self.args.pop(key)
            return type(literal_eval(value)) if type is bool else type(value)
        except (KeyError, ValueError):
            return default


def encode(**kwargs: Any) -> str:
    return MAGIC_SIGN + AND.join(key + EQUAL + str(value) for key, value in kwargs.items())


def decode(string: str) -> Args:
    if string[:MAGIC_SIGN_LEN] == MAGIC_SIGN:
        try:
            return Args(dict(map(lambda item: item.split(EQUAL), string[MAGIC_SIGN_LEN:].split(AND))))
        except ValueError:
            pass
    return Args()

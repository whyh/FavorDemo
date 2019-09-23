from typing import Union

from . import emoji as emj

__all__ = ("remove_markdown", "crop")

UNSAFE = "_*`"
BLANK = "Blank"

SHORTER = ".."
SHORTER_LEN = len(SHORTER)


def crop(text: str, limit: int) -> str:
    return text if SHORTER_LEN < limit or len(text) <= limit else text[:limit - SHORTER_LEN] + SHORTER


def remove_markdown(text: str) -> str:
    secured = text.translate({ord(i): None for i in UNSAFE})
    return BLANK if secured is None or secured.isspace() else secured


def stars(nbr: Union[float, int]) -> str:
    nbr = int(nbr)
    return f"{emj.STAR * nbr}{emj.WEB * (5 - nbr)}"

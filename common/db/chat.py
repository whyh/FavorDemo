from .orm import *

__all__ = ("Chat", "LockedChat")


class Chat(Kind):
    invite = StringField()
    occupied = BooleanField(index=True, default=False)


class LockedChat(Chat):
    _kind = "chat"
    _p_lock = True

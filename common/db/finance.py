from .orm import *

__all__ = ("Withdraw", "LockedWithdraw")


class Withdraw(Kind):
    user = IntegerField(index=True)
    amount = FloatField()


class LockedWithdraw(Withdraw):
    _kind = "withdraw"
    _p_lock = True

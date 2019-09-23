from .embedded import *
from .orm import *
from common.glossary import DEF_LANG

__all__ = ("Deal", "LockedDeal")


class Deal(Kind):
    class RewardField(EmbeddedBaseField):
        amount = IntegerField(default=0)
        secured = BooleanField(default=False)
        creator = BooleanField(default=False)
        contributor = BooleanField(default=False)

    class InChatField(EmbeddedBaseField):
        creator = BooleanField(default=False)
        contributor = BooleanField(default=False)

    @property
    def lang(self):
        try:
            return self._lang
        except AttributeError:
            self._lang = self.creator.lang if self.creator.lang == self.contributor.lang else DEF_LANG
            return self._lang

    creator = UserField(default=UserField)
    contributor = UserField(default=UserField)

    post = IntegerField()
    chat = IntegerField(index=True)
    invite = StringField()
    reward = RewardField(default=RewardField)

    conv = ConvField(default=ConvField)
    in_chat = InChatField(default=InChatField)


class LockedDeal(Deal):
    _kind = "deal"
    _p_lock = True

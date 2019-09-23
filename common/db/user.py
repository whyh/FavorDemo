from typing import Optional

from aiogram.types import User as TgUser

from .orm import *
from .embedded import *
from common.glossary import SUPPORTED_LANGS
from common.utils import remove_markdown

__all__ = ("User", "LockedUser")


class User(Kind):
    class StatsField(EmbeddedBaseField):
        class DealField(EmbeddedBaseField):
            @property
            def gpa(self):
                try:
                    return self.gp / self.graded
                except ZeroDivisionError:
                    return 0

            @property
            def avg_reward(self):
                try:
                    return self.reward / self.closed
                except ZeroDivisionError:
                    return 0

            closed = IntegerField(default=0)
            canceled = IntegerField(default=0)
            graded = IntegerField(default=0)

            reward = FloatField(default=0.0)
            gp = IntegerField(default=0)

        class PostField(EmbeddedBaseField):
            created = IntegerField(default=0)
            terminated = IntegerField(default=0)

        creator = DealField(default=DealField)
        contributor = DealField(default=DealField)
        post = PostField(default=PostField)

    class AccountField(EmbeddedBaseField):
        class DealField(EmbeddedBaseField):
            id = IntegerField()
            amount = IntegerField()

        balance = FloatField(default=0.0)
        secured = FloatField(default=0.0)

        uns_deals = ListField(DealField)
        bank_cards = ListField(StringField)

    class ContributorDealField(EmbeddedBaseField):
        id = IntegerField()
        post = IntegerField()

    @classmethod
    def _from_tg_user(cls, tg_user: TgUser) -> "User":
        return cls(id=tg_user.id, lang=tg_user.language_code, name=cls._get_name(tg_user), url=cls._get_url(tg_user))

    @staticmethod
    def _get_url(tg_user: TgUser) -> Optional[str]:
        return None if tg_user.username is None else f"https://t.me/{tg_user.username}"

    @staticmethod
    def _get_name(tg_user: TgUser) -> str:
        return remove_markdown(tg_user.full_name if tg_user.username is None else tg_user.username)

    @classmethod
    def get(cls, tg_user) -> "User":
        user = cls.find(tg_user.id)
        if user is None:
            user = cls._from_tg_user(tg_user)
            user.save()
        else:
            user.name = cls._get_name(tg_user)
            user.url = cls._get_url(tg_user)
        return user

    @classmethod
    def get_locked(cls, tg_user) -> "User":
        user = cls.find(tg_user.id)
        if user is None:
            user = cls._from_tg_user(tg_user)
        else:
            user.name = cls._get_name(tg_user)
            user.url = cls._get_url(tg_user)
        return user

    lang = StringField(valid=lambda lang: True if lang in SUPPORTED_LANGS else False)
    name = StringField()
    url = StringField()

    creator_deals = ListField(IntegerField)
    contributor_deals = ListField(ContributorDealField)
    ung_deals = ListField(IntegerField)
    posts = ListField(IntegerField)

    account = AccountField(default=AccountField)
    repl_token = StringField(index=True)
    stats = StatsField(default=StatsField)

    conv = ConvField(default=ConvField)
    post_content = PostContentField(default=PostContentField)

    admin = BooleanField(default=False)
    moderator = BooleanField(default=False)


class LockedUser(User):
    _kind = "user"
    _p_lock = True

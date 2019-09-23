from typing import Optional

from .orm import *

__all__ = ("Top", "LockedTop")

(CREATORS,
 CONTRIBUTORS
 ) = (i + 1 for i in range(2))


class Top(Kind):
    class UserField(EmbeddedBaseField):
        id = IntegerField()
        name = StringField()
        gp = IntegerField()
        gpa = FloatField()

    def get_index(self, user_id: int) -> Optional[int]:
        index = 0
        for user in self.rating:
            if user.id == user_id:
                return index
            index += 1

    def update(self, new_user: UserField) -> None:
        try:
            self.rating.pop(self.get_index(new_user.id))
        except TypeError:
            self.size += 1

        index = 0
        for user in self.rating:
            if user.gp < new_user.gp:
                break
            index += 1

        self.rating.insert(index, new_user)

    rating = ListField(UserField)
    size = IntegerField(default=0)


class LockedTop(Top):
    _kind = "top"
    _p_lock = True

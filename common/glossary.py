from typing import Union, Tuple, Optional

DEF_LANG = "ru"
SUPPORTED_LANGS = ("en", "ru", "ua")


class IncompletePhraseError(ValueError):
    pass


class Phrase:
    def __init__(self, tpl: Optional[str] = None, **options: Union[str, Tuple[str, ...]]):
        for lang in SUPPORTED_LANGS:
            text = options.get(lang)
            if text is None:
                raise IncompletePhraseError
            else:
                setattr(self, lang, text if tpl is None else tpl % text)

    @property
    def default(self) -> str:
        return getattr(self, DEF_LANG)

    def __call__(self, lang: str = DEF_LANG, *format_args) -> str:
        return getattr(self, lang, self.default).format(*format_args)

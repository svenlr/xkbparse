
class IntNumMixin:
    """
    Workaround to make "__num" as created by peg.attr("__num", ...) as str available as "num" attribute with int type.
    To be derived from in classes with a "__num" peg.attr().
    """

    @property
    def num(self):
        return int(getattr(self, "__num"))

    @num.setter
    def num(self, value):
        setattr(self, "__num", value)

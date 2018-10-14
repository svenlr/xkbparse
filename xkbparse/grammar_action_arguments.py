import re
import pypeg2 as peg

from .grammar_util import IntNumMixin

TRUE_VALUES = ["yes", "on", "true"]
FALSE_VALUES = ["no", "off", "false"]
FALSE_PREFIXES = ["!", "~"]


class BoolArg:
    grammar = peg.optional(peg.attr("prefix", FALSE_PREFIXES)), peg.attr("name", peg.word), \
              peg.optional("=", peg.attr("right_hand_val", TRUE_VALUES + FALSE_VALUES))

    @property
    def value(self):
        if hasattr(self, "prefix") and self.prefix in FALSE_PREFIXES:
            return False
        elif hasattr(self, "right_hand_val") and self.right_hand_val in FALSE_VALUES:
            return False
        else:
            return True

    @value.setter
    def value(self, value):
        if value:
            # if true is desired we want no prefix
            if hasattr(self, "prefix"):
                delattr(self, "prefix")
            # also, we completely omit the right hand side and the equals sign
            if hasattr(self, "right_hand_val"):
                delattr(self, "right_hand_val")
        else:
            setattr(self, "prefix", "!")
            # also, we completely omit the right hand side, only use prefix for negation as above
            if hasattr(self, "right_hand_val"):
                delattr(self, "right_hand_val")


def arg(name: str, variants: list = None):
    if variants is None:
        variants = []
    if name not in variants:
        variants.append(name)
    return variants, peg.optional("=", peg.attr("value", re.compile(r"[^,)]+")))


class OtherArgument:
    grammar = peg.attr("name", re.compile(r"[^=,)]+")), peg.optional("=", peg.attr("value", re.compile(r"[^,)]+")))


class XCoordArgument:
    grammar = "x", "=", peg.attr("value", re.compile(r"[0-9]+"))


class GroupArgument(IntNumMixin):
    grammar = ["group"], "=", peg.attr("__num", re.compile(r"[1-4]"))


class RelativeGroupArgument(IntNumMixin):
    grammar = ["group"], "=", peg.attr("num", re.compile(r"[+\-][1-4]"))


class ModifiersArgument(peg.List):
    """ modifiers= or mods= argument in action command. Takes a list of '+'-separated modifiers """
    grammar = ["modifiers", "mods"], "=", peg.csl(peg.word, separator="+")


class BoolArgsListMixin(peg.List):
    def get_specified_bool_args(self):
        ret = []
        for e in self:
            if isinstance(e, BoolArg):
                ret.append(e)
        return ret

    def get_specified_bool_arg_names(self):
        return map(lambda bool_arg: bool_arg.value, self.get_specified_bool_args())

    def get_bool(self, name):
        for e in self:
            if isinstance(e, BoolArg) and e.name == name:
                return e.value

    def set_bool(self, name, value):
        for e in self:
            if isinstance(e, BoolArg) and e.name == name:
                e.value = value

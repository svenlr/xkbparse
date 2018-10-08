import re

import pypeg2 as peg

from .grammar_util import IntNumMixin


def bool_arg(name: str, variants: list = None):
    if variants is None:
        variants = []
    if name not in variants:
        variants.append(name)
    grammar_true = peg.flag(name, list(map(lambda v: (v, peg.optional("=", ["yes", "on", "true"])), variants))),
    return [grammar_true, ("~", variants), ("!", variants), (variants, "=", ["no", "off", "false"])]


def arg(name: str, variants: list = None):
    if variants is None:
        variants = []
    if name not in variants:
        variants.append(name)
    return variants, peg.optional("=", peg.attr("name", re.compile(r"[^,)]+")))


def action(name_aliases: list, arguments: list):
    return name_aliases, "(", peg.csl(arguments, separator=","), ")"


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


class SetModsAction:
    """
     SetMods() action as used in interpret { ... } or key description.
     Applies the modifiers as long as the key is pressed.
     If clearLocks is specified, unlock possibly locked modifiers that are amongst the specified modifiers.
    """
    grammar = action(["SetMods"], [bool_arg("clearLocks"), peg.attr("modifiers", ModifiersArgument)])


class LatchModsAction(peg.List):
    """ LatchMods() action as used in interpret { ... } or key description. Difference to SetMods unknown?? """
    arguments = [peg.attr("modifiers", ModifiersArgument), bool_arg("latchToLock"), bool_arg("clearLocks")]
    grammar = "LatchMods", "(", arguments, peg.maybe_some(",", arguments), ")"


class LockModsAction:
    """
     LockMods() action as used in interpret { ... } or key description.
     Lock specified modifiers at key press that are not already locked.
     Release specified modifiers that are already locked.
    """
    grammar = "LockMods", ",", peg.attr("modifiers", ModifiersArgument), ")"


class SetGroupAction:
    arguments = [bool_arg("clearLocks"), peg.attr("group", GroupArgument), peg.attr("rel_group", RelativeGroupArgument)]
    grammar = action(["SetGroup"], arguments)


class LatchGroupAction:
    arguments = [bool_arg("clearLocks"), bool_arg("latchToLock"), peg.attr("group", GroupArgument),
                 peg.attr("rel_group", RelativeGroupArgument)]
    grammar = action(["LatchGroup"], arguments)


class LockGroupAction:
    grammar = "LockGroup", "(", [peg.attr("group", GroupArgument), peg.attr("rel_group", RelativeGroupArgument)], ")"


class MovePointerAction:
    arguments = [arg("x"), arg("y"), bool_arg("accelerate", ["accel", "repeat"])]
    grammar = action(["MovePtr", "MovePointer"], arguments)


class PointerButtonAction:
    arguments = [arg("button", ["value"]), arg("count")]
    grammar = action(["PointerButton", "PointerBtn", "PtrButton", "PtrBtn"], arguments)


class LockPointerButtonAction:
    affect_arg = ("affect", "=", ["lock", "unlock", "both", "neither"])
    arguments = [arg("button", ["value"]), arg("count"), peg.attr("affect", affect_arg)]
    grammar = action(["LockPointerButton", "LockPointerBtn", "LockPtrButton", "LockPtrBtn"], arguments)


class RedirectKeyAction:
    """ Redirect() or RedirectKey() action that is used in interpret { ... } or key description """
    grammar = ["Redirect", "RedirectKey"], "(",

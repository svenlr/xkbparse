import re

import pypeg2 as peg

from .grammar_action_arguments import *


def action(name_aliases: list, arguments: list):
    return name_aliases, "(", peg.csl(arguments, separator=","), ")"


class SetModsAction:
    """
     SetMods() action as used in interpret { ... } or key description.
     Applies the modifiers as long as the key is pressed.
     If clearLocks is specified, unlock possibly locked modifiers that are amongst the specified modifiers.
    """
    grammar = action(["SetMods"], [peg.attr("modifiers", ModifiersArgument), BoolArg])


class LatchModsAction(BoolArgsListMixin):
    """ LatchMods() action as used in interpret { ... } or key description. Difference to SetMods unknown?? """
    arguments = [peg.attr("modifiers", ModifiersArgument), BoolArg]
    grammar = "LatchMods", "(", arguments, peg.maybe_some(",", arguments), ")"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setattr(self, "modifiers", ModifiersArgument())


class LockModsAction:
    """
     LockMods() action as used in interpret { ... } or key description.
     Lock specified modifiers at key press that are not already locked.
     Release specified modifiers that are already locked.
    """
    grammar = "LockMods", ",", peg.attr("modifiers", ModifiersArgument), ")"


class SetGroupAction:
    arguments = [BoolArg, peg.attr("group", GroupArgument),
                 peg.attr("rel_group", RelativeGroupArgument)]
    grammar = action(["SetGroup"], arguments)


class LatchGroupAction:
    arguments = [BoolArg, BoolArg, peg.attr("group", GroupArgument),
                 peg.attr("rel_group", RelativeGroupArgument)]
    grammar = action(["LatchGroup"], arguments)


class LockGroupAction:
    grammar = "LockGroup", "(", [peg.attr("group", GroupArgument), peg.attr("rel_group", RelativeGroupArgument)], ")"


class MovePointerAction:
    arguments = [arg("x"), arg("y"), BoolArg]
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

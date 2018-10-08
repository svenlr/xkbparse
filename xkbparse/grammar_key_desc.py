import re

import pypeg2 as peg

from .grammar_util import IntNumMixin


class LevelType:
    """ A level type, such as "FOUR_LEVEL" or "EIGHT_LEVEL". Matches quotes as well. """
    grammar = "\"", peg.attr("name", re.compile(r"([A-Z]|_|\+)*")), "\""


class ScanCodeName:
    """ A key code such as <UP> or <DOWN> """
    grammar = "<", peg.attr("name", re.compile(r"([A-Z]|\+|-|[0-9])+")), ">"

    @staticmethod
    def from_name(name):
        return peg.parse("<" + name + ">", ScanCodeName)


class KeySym:
    """ Key symbol such as bracketleft, braceleft, 1, 2, 3, a, b, A, B... """
    grammar = peg.attr("name", peg.word)


class KeySymList(peg.List):
    """ A list of key symbols in brackets """
    grammar = "[", peg.optional(peg.csl(KeySym)), "]"

    @staticmethod
    def from_strings(strings: list):
        levels = KeySymList()
        for s in strings:
            k = KeySym()
            k.name = s
            levels.append(k)
        return levels


class ActionsList(peg.List):
    """  A list of actions in brackets """
    pass


class KeyDescSymbols(IntNumMixin):
    """ inside a key definition inside key_symbols { ... }, this is the part symbols[Group1]=[...]"""
    grammar = "symbols", "[", ["Group", "group"], peg.attr("__num", re.compile(r"[0-9]+")), "]", \
              "=", peg.attr("levels", KeySymList)


class KeyDescOverlay(IntNumMixin):
    """ inside a key definition inside key_symbols { ... }, this is the part overlayX=<...>"""
    grammar = "overlay", peg.attr("__num", re.compile(r"[0-9]")), "=", peg.attr("key_code", ScanCodeName)


class KeyDescActions():
    """ inside a key definition inside key_symbols { ... }, this is the part actions[Group1]= [] """
    grammar = "actions", "[", ["Group", "group"], peg.attr("__num", re.compile(r"[0-9]+")), "]", \
              "=", peg.attr("actions", ActionsList)


class KeyDescription(peg.List):
    """ A key definition in the xkb_symbols { ... } section """
    _contained_grammars = [KeyDescSymbols, KeyDescActions, KeyDescOverlay, ("type", "=", LevelType),
                           peg.attr("short_levels", KeySymList)]
    grammar = "key", peg.blank, peg.attr("key_code", ScanCodeName), peg.blank, "{", peg.endl, \
              peg.indent(
                  _contained_grammars,
                  peg.maybe_some(",", peg.endl, _contained_grammars),
                  peg.optional(","), peg.endl
              ), "}", ";", peg.endl

    @property
    def type(self):
        for e in self:
            if isinstance(e, LevelType):
                return e
        return None

    def convert_short_keysym_list(self, group_nums: list):
        assert hasattr(self, "short_levels")
        for group_num in group_nums:
            self.set_symbols_group(group_num, self.short_levels)
        delattr(self, "short_levels")

    def get_overlays(self):
        overlays = []
        for child in self:
            if isinstance(child, KeyDescOverlay):
                overlays.append(child)
        return overlays

    def get_overlay_nums(self):
        map(lambda o: o.num, self.get_overlays())

    def get_overlay_by_num(self, num: int):
        return [child for child in self if isinstance(child, KeyDescOverlay) and child.num == num][0]

    def remove_overlay_by_num(self, num: int):
        self[:] = [child for child in self if not isinstance(child, KeyDescOverlay) or child.num != num]

    def set_overlay(self, num: int, key_code: ScanCodeName):
        self.remove_overlay_by_num(num)
        overlay = KeyDescOverlay()
        overlay.num = num
        overlay.key_code = key_code
        self.append(overlay)

    def get_symbols_groups(self):
        groups = []
        for child in self:
            if isinstance(child, KeyDescSymbols):
                groups.append(child)
        return groups

    def get_symbols_group_nums(self):
        map(lambda syms: syms.group_num, self.get_symbols_groups())

    def get_symbols_group_by_num(self, num: int):
        return [child for child in self if isinstance(child, KeyDescSymbols) and child.num == num][0]

    def remove_symbols_group_by_num(self, num: int):
        self[:] = [child for child in self if not isinstance(child, KeyDescSymbols) or child.num != num]

    def set_symbols_group(self, num: int, levels: KeySymList):
        self.remove_symbols_group_by_num(num)
        group = KeyDescSymbols()
        group.num = num
        group.levels = levels
        self.append(group)

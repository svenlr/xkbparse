import re

import pypeg2 as peg


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


class LevelType:
    """ A level type, such as "FOUR_LEVEL" or "EIGHT_LEVEL". Matches quotes as well. """
    grammar = "\"", peg.attr("name", re.compile(r"([A-Z]|_|\+)*")), "\""


class KeyCode:
    """ A key code such as <UP> or <DOWN> """
    grammar = "<", peg.attr("name", re.compile(r"([A-Z]|\+|-|[0-9])+")), ">"

    @staticmethod
    def from_name(name):
        return peg.parse("<" + name + ">", KeyCode)


class KeySym:
    """ Key symbol such as bracketleft, braceleft, 1, 2, 3, a, b, A, B... """
    grammar = peg.attr("name", peg.word)


class KeySymLevels(peg.List):
    """ A list of key symbols in brackets """
    grammar = "[", peg.optional(peg.csl(KeySym)), "]"

    @staticmethod
    def from_strings(strings: list):
        levels = KeySymLevels()
        for s in strings:
            k = KeySym()
            k.name = s
            levels.append(k)
        return levels


class KeyDefSymbolsGroup(IntNumMixin):
    """ inside a key definition inside key_symbols { ... }, this is the part symbols[Group1]=[...]"""
    grammar = "symbols", "[", ["Group", "group"], peg.attr("__num", re.compile(r"[0-9]+")), "]", \
              "=", peg.attr("levels", KeySymLevels)


class KeyDefOverlay(IntNumMixin):
    """ inside a key definition inside key_symbols { ... }, this is the part overlayX=<...>"""
    grammar = "overlay", peg.attr("__num", re.compile(r"[0-9]")), "=", peg.attr("key_code", KeyCode)


class KeyDefShort:
    """ short key definition inside key_symbols { ... }, such as key <A> { [a, A] }"""
    grammar = "key", peg.blank, peg.attr("key_code", KeyCode), peg.blank, "{", \
              peg.indent(peg.attr("short_levels", KeySymLevels)), peg.endl, "}", ";"

    def convert(self, group_nums: list, type: LevelType):
        key_def = KeyDef()
        key_def.type = type
        for group_num in group_nums:
            key_def.set_symbols_group(group_num, self.short_levels)
        return key_def


class KeyDef(peg.List):
    """ A key definition in the xkb_symbols { ... } section """
    grammar = "key", peg.blank, peg.attr("key_code", KeyCode), peg.blank, "{", peg.endl, \
              peg.indent(
                  peg.optional(("type", "=", peg.attr("type", LevelType)), ","), peg.endl,
                  [KeyDefSymbolsGroup, KeyDefOverlay],
                  peg.maybe_some(",", peg.endl, [KeyDefSymbolsGroup, KeyDefOverlay]),
                  peg.optional(","), peg.endl
              ), "}", ";", peg.endl

    def get_overlays(self):
        overlays = []
        for child in self:
            if isinstance(child, KeyDefOverlay):
                overlays.append(child)
        return overlays

    def get_overlay_nums(self):
        map(lambda o: o.num, self.get_overlays())

    def get_overlay_by_num(self, num: int):
        return [child for child in self if isinstance(child, KeyDefOverlay) and child.num == num][0]

    def remove_overlay_by_num(self, num: int):
        new_list = [child for child in self if not isinstance(child, KeyDefOverlay) or child.num != num]
        self.clear()
        for elem in new_list:
            self.append(elem)

    def set_overlay(self, num: int, key_code: KeyCode):
        self.remove_overlay_by_num(num)
        overlay = KeyDefOverlay()
        overlay.num = num
        overlay.key_code = key_code
        self.append(overlay)

    def get_symbols_groups(self):
        groups = []
        for child in self:
            if isinstance(child, KeyDefSymbolsGroup):
                groups.append(child)
        return groups

    def get_symbols_group_nums(self):
        map(lambda syms: syms.group_num, self.get_symbols_groups())

    def get_symbols_group_by_num(self, num: int):
        return [child for child in self if isinstance(child, KeyDefSymbolsGroup) and child.num == num][0]

    def remove_symbols_group_by_num(self, num: int):
        new_list = [child for child in self if not isinstance(child, KeyDefSymbolsGroup) or child.num != num]
        self.clear()
        for elem in new_list:
            self.append(elem)

    def set_symbols_group(self, num: int, levels: KeySymLevels):
        self.remove_symbols_group_by_num(num)
        group = KeyDefSymbolsGroup()
        group.num = num
        group.levels = levels
        self.append(group)

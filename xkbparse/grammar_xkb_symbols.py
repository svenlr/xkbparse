from .grammar_key_desc import *

from .grammar_util import IntNumMixin


class GroupLanguageDef(IntNumMixin):
    grammar = "name", "[", ["Group", "group"], peg.attr("__num", re.compile(r"[0-9]+")), "]", \
              peg.blank, "=", peg.blank, "\"", peg.name(), "\"", ";", peg.endl


class ModifierMapDef:
    grammar = "modifier_map ", peg.attr("modifier", re.compile(r"\w+")), peg.blank, \
              "{", peg.blank, peg.attr("key_code", ScanCodeName), peg.blank, "}", ";", peg.endl


class XKBSymbolsSection(peg.List):
    _contained_grammars = [GroupLanguageDef, KeyDescription, ModifierMapDef]
    grammar = "xkb_symbols", peg.blank, "\"", peg.attr("name", re.compile(r"(\w|\(|\))*")), "\"", peg.blank, "{", \
              peg.indent(peg.maybe_some(peg.endl, _contained_grammars)), "}", ";"

    def get_groups(self):
        groups = []
        for e in self:
            if isinstance(e, GroupLanguageDef):
                groups.append(e)
        return groups

    def __language_by_group_num(self, num: int):
        for e in self:
            if isinstance(e, GroupLanguageDef) and e.num == num:
                return e
        return None

    def get_language_name_by_group_num(self, group_num: int):
        return self.__language_by_group_num(group_num).name

    def set_language(self, group_num: int, language_name: str):
        language = self.__language_by_group_num(group_num)
        assert language is not None
        language.name = language_name

    def get_key_descs(self):
        key_defs = []
        for e in self:
            if isinstance(e, KeyDescription):
                key_defs.append(e)
        return key_defs

    def get_key_desc(self, key_code):
        normal_key_defs = self.get_key_descs()
        for key_desc in normal_key_defs:
            if key_desc.key_code == key_code:
                return key_desc
        return None

    def set_key_desc(self, key_def):
        existing = self.get_key_desc(key_def.key_code)
        if existing:
            self.remove(existing)
        self.append(key_def)



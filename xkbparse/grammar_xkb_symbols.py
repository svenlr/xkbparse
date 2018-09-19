from .grammar_key_def import *


class GroupLanguageDef(IntNumMixin):
    grammar = "name", "[", ["Group", "group"], peg.attr("__num", re.compile(r"[0-9]+")), "]", \
              peg.blank, "=", peg.blank, "\"", peg.name(), "\"", ";", peg.endl


class ModifierMapDef:
    grammar = "modifier_map ", peg.attr("modifier", re.compile(r"\w+")), peg.blank, \
              "{", peg.blank, peg.attr("key_code", KeyCode), peg.blank, "}", ";", peg.endl


class XKBSymbolsSection(peg.List):
    _contained_grammars = [GroupLanguageDef, KeyDef, KeyDefShort, ModifierMapDef]
    grammar = "xkb_symbols", peg.blank, "\"", peg.attr("name", re.compile(r"(\w|\(|\))*")), "\"", peg.blank, "{", \
              peg.indent(peg.maybe_some(peg.endl, _contained_grammars)), "}", ";"

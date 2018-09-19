import os

import pypeg2 as peg

import xkbparse
from .data_dir_path import TEST_DATA_DIR


def test_GroupLanguageDef():
    parsed = peg.parse("name[group1]=\"German\";", xkbparse.GroupLanguageDef)
    assert parsed.num == 1
    assert parsed.name == "German"


def test_ModifierMapDef():
    parsed = peg.parse("modifier_map Mod5 { <MDSW> };", xkbparse.ModifierMapDef)
    assert parsed.modifier == "Mod5"
    assert parsed.key_code.name == "MDSW"


def test_XKBSymbolsSection():
    with open(os.path.join(TEST_DATA_DIR, "xkb_symbols1")) as f:
        parsed = peg.parse(f.read(), xkbparse.XKBSymbolsSection)

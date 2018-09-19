import os

import pypeg2

import xkbparse
from .test_data_dir import TEST_DATA_DIR


def test_KeyCode():
    assert pypeg2.parse("<AE01>", xkbparse.KeyCode).name == "AE01"


def test_KeySym():
    assert pypeg2.parse("KP_Multiply", xkbparse.KeySym).name == "KP_Multiply"
    assert pypeg2.parse("XF86ClearGrab", xkbparse.KeySym).name == "XF86ClearGrab"


def test_TypeString():
    assert pypeg2.parse("\"CTRL+ALT\"", xkbparse.LevelType).name == "CTRL+ALT"


def test_KeySymLevels():
    with open(os.path.join(TEST_DATA_DIR, "list_AE01")) as f:
        parsed = pypeg2.parse(f.read(), xkbparse.KeySymLevels)
        assert parsed[0].name == "1"
        assert parsed[1].name == "exclam"
        assert parsed[2].name == "onesuperior"
        assert parsed[3].name == "exclamdown"

    with open(os.path.join(TEST_DATA_DIR, "list_empty")) as f:
        parsed = pypeg2.parse(f.read(), xkbparse.KeySymLevels)
        assert len(parsed) == 0


def test_KeyDefSymbols():
    with open(os.path.join(TEST_DATA_DIR, "symbols_AE01")) as f:
        parsed = pypeg2.parse(f.read(), xkbparse.KeyDefSymbolsGroup)
        assert parsed.num == 1
        assert parsed.levels[2].name == "onesuperior"


def test_KeyDef():
    with open(os.path.join(TEST_DATA_DIR, "AE01")) as f:
        parsed = pypeg2.parse(f.read(), xkbparse.KeyDef)
        assert parsed.get_symbols_group_by_num(1).levels[2].name == "onesuperior"
        parsed.set_overlay(1, xkbparse.KeyCode.from_name("UP"))
        parsed.set_overlay(2, xkbparse.KeyCode.from_name("LEFT"))
        parsed.set_overlay(2, xkbparse.KeyCode.from_name("DOWN"))
        parsed.set_symbols_group(2, xkbparse.KeySymLevels.from_strings(["1"]))
        parsed.set_symbols_group(2, xkbparse.KeySymLevels.from_strings(["1", "2"]))
        parsed.remove_symbols_group_by_num(1)
        parsed.remove_overlay_by_num(1)
        composed = pypeg2.compose(parsed, xkbparse.KeyDef)
        # print(composed)
        reparsed = pypeg2.parse(composed, xkbparse.KeyDef)
        assert reparsed.type.name == "FOUR_LEVEL"
        assert reparsed.key_code.name == "AE01"
        assert reparsed.get_symbols_group_by_num(2).levels[0].name == "1"
        assert reparsed.get_overlay_by_num(2).key_code.name == "DOWN"

    with open(os.path.join(TEST_DATA_DIR, "KPMU")) as f:
        parsed = pypeg2.parse(f.read(), xkbparse.KeyDef)
        assert parsed.type.name == "CTRL+ALT"
        assert parsed.key_code.name == "KPMU"
        assert parsed.get_symbols_group_by_num(1).levels[2].name == "KP_Multiply"

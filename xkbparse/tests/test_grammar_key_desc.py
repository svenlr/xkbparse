import os

import pypeg2 as peg

import xkbparse
from .data_dir_path import TEST_DATA_DIR


def test_KeyCode():
    assert peg.parse("<AE01>", xkbparse.ScanCodeName).name == "AE01"
    assert peg.parse("<MDSW>", xkbparse.ScanCodeName).name == "MDSW"


def test_KeySym():
    assert peg.parse("KP_Multiply", xkbparse.KeySym).name == "KP_Multiply"
    assert peg.parse("XF86ClearGrab", xkbparse.KeySym).name == "XF86ClearGrab"


def test_TypeString():
    assert peg.parse("\"CTRL+ALT\"", xkbparse.LevelType).name == "CTRL+ALT"


def test_KeySymLevels():
    with open(os.path.join(TEST_DATA_DIR, "list_AE01")) as f:
        parsed = peg.parse(f.read(), xkbparse.KeySymList)
        assert parsed[0].name == "1"
        assert parsed[1].name == "exclam"
        assert parsed[2].name == "onesuperior"
        assert parsed[3].name == "exclamdown"

    with open(os.path.join(TEST_DATA_DIR, "list_empty")) as f:
        parsed = peg.parse(f.read(), xkbparse.KeySymList)
        assert len(parsed) == 0


def test_KeyDefSymbols():
    with open(os.path.join(TEST_DATA_DIR, "symbols_AE01")) as f:
        parsed = peg.parse(f.read(), xkbparse.KeyDescSymbols)
        assert parsed.num == 1
        assert parsed.levels[2].name == "onesuperior"


def test_KeyDef():
    with open(os.path.join(TEST_DATA_DIR, "AE01")) as f:
        parsed = peg.parse(f.read(), xkbparse.KeyDescription)
        assert parsed.get_symbols_group_by_num(1).levels[2].name == "onesuperior"
        parsed.set_overlay(1, xkbparse.ScanCodeName.from_name("UP"))
        parsed.set_overlay(2, xkbparse.ScanCodeName.from_name("LEFT"))
        parsed.set_overlay(2, xkbparse.ScanCodeName.from_name("DOWN"))
        parsed.set_symbols_group(2, xkbparse.KeySymList.from_strings(["1"]))
        parsed.set_symbols_group(2, xkbparse.KeySymList.from_strings(["1", "2"]))
        parsed.remove_symbols_group_by_num(1)
        parsed.remove_overlay_by_num(1)
        composed = peg.compose(parsed, xkbparse.KeyDescription)
        # print(composed)
        reparsed = peg.parse(composed, xkbparse.KeyDescription)
        assert reparsed.type.name == "FOUR_LEVEL"
        assert reparsed.key_code.name == "AE01"
        assert reparsed.get_symbols_group_by_num(2).levels[0].name == "1"
        assert reparsed.get_overlay_by_num(2).key_code.name == "DOWN"

    with open(os.path.join(TEST_DATA_DIR, "KPMU")) as f:
        parsed = peg.parse(f.read(), xkbparse.KeyDescription)
        assert parsed.type.name == "CTRL+ALT"
        assert parsed.key_code.name == "KPMU"
        assert parsed.get_symbols_group_by_num(1).levels[2].name == "KP_Multiply"

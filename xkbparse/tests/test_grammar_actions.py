import os

import pypeg2 as peg

import xkbparse
from .data_dir_path import TEST_DATA_DIR


def test_bool_arg():
    parsed = peg.parse("clearLocks", xkbparse.bool_arg("clearLocks"))
    options = xkbparse.bool_arg("abc") + xkbparse.bool_arg("def")
    print(options)
    parsed2 = peg.parse("abc,def", (options, ",", options))


def test_ModifiersArgument():
    parsed1 = peg.parse("modifiers=LevelFive", xkbparse.ModifiersArgument)
    assert parsed1[0] == "LevelFive"
    parsed2 = peg.parse("modifiers=LevelFive+Shift", xkbparse.ModifiersArgument)
    assert parsed2[0] == "LevelFive"
    assert parsed2[1] == "Shift"


def test_LatchModsAction():
    parsed = peg.parse("LatchMods(modifiers=LevelFive,clearLocks,latchToLock)", xkbparse.LatchModsAction)
    assert parsed.clearLocks
    assert parsed.latchToLock

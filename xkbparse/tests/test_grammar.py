import os

import pypeg2

import xkbparse
from .test_data_dir import TEST_DATA_DIR


def test_KeyCode():
    assert pypeg2.parse("<AE01>", xkbparse.KeyCode).name == "AE01"


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
        parsed = pypeg2.parse(f.read(), xkbparse.KeyDefSymbols)
        assert parsed.group == "Group1"
        assert parsed.levels[2].name == "onesuperior"

# def test_KeyDef():
#     with open(os.path.join(TEST_DATA_DIR, "AE01")) as f:
#         parsed = pypeg2.parse(f.read(), xkbparse.KeyDef)

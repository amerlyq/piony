import pytest

import piony.budparser.exceptions as bux
from piony.budparser.segment import SegmentMaker
from piony.budparser.ring import RingMaker
from piony.budparser.parser import BudParser


SEG = SegmentMaker.SEG


def RING(rgs):
    return {'segments': rgs}


class TestSegmentMaker:

    def test_fromList(self):
        func = SegmentMaker().fromList
        assert (None, None, None) == func([])
        assert ("a", "a", "a") == func(["a"])
        assert ("All", "a", "a") == func(["a", "All"])
        assert ("n", "a", "t") == func(["a", "n", "t"])

    def test_fromDict(self):
        func = SegmentMaker().fromDict
        assert (None, None, None) == func({})
        assert (None, None, None) == func({"a": 1})
        assert ("N", None, None) == func({"name": "N"})
        assert (None, None, "T") == func({"tooltip": "T"})
        assert ("A", "A", "A") == func({"action": "A"})

    def test_make(self):
        func = SegmentMaker().make
        assert SEG("", None, SegmentMaker.PS) == func(None)
        assert SEG("", None, SegmentMaker.PS) == func([])
        assert SEG("", None, SegmentMaker.PS) == func("")
        assert SEG("a", "a", "a") == func("a")
        assert SEG("a", "a", "a") == func(["a"])
        assert SEG("a", "a", "a") == func({"action": "a"})

        with pytest.raises(bux.BudSyntaxError):
            func(2)


class TestRingMaker:

    def test_fromList(self):
        func = RingMaker().fromList
        assert func(["a"]) == ["a"]
        assert func(("a", "b")) == ("a", "b")
        assert func(["", {"name": "N"}]) == ["", {"name": "N"}]
        assert func({"k": "v"}) == {"k": "v"}

        with pytest.raises(bux.BudSyntaxError):
            func([["a"], "b"])
        with pytest.raises(bux.BudSyntaxError):
            func([1, {"k": "v"}])

    def test_fromDict(self):
        func = RingMaker().fromDict
        assert func({"segments": ["a"]}) == ["a"]
        assert func({"action": "a"}) == [{"action": "a"}]
        assert func({"name": "N", "tooltip": "T"}) == [{"name": "N", "tooltip": "T"}]

        with pytest.raises(bux.BudSyntaxError):
            func({"rings": ["a"]})
        with pytest.raises(bux.BudSyntaxError):
            func({"segments": ["a"], "some": []})

    def test_make(self):
        func = RingMaker().make
        assert func(None) == RING([])
        assert func([]) == RING([])
        assert func(["a"]) == RING([SEG("a", "a", "a")])
        assert func(RING(["a"])) == RING([SEG("a", "a", "a")])
        assert func({"action": "a"}) == RING([SEG("a", "a", "a")])
        assert func(["a", "b"]) == RING(
            [SEG("a", "a", "a"), SEG("b", "b", "b")])


# https://pytest.org/latest/fixture.html
@pytest.fixture
def bps():
    return BudParser()


class TestBudParser:
    def test_addEntry(self, bps):
        assert bps.parse("") == {"slices": [{"rings": [{"segments": []}]}]}

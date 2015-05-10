import pytest

import piony.budparser.exceptions as bux
from piony.budparser.segment import SegmentMaker
from piony.budparser.ring import RingMaker
from piony.budparser.slice import SliceMaker
from piony.budparser.parser import BudParser


def SEG(n, a, t=None):
    if a and not t:
        t = '<b>' + a + '</b>'
    return SegmentMaker.SEG(n, a, t)


def RING(*rgs):
    return {'segments': list(rgs)}


def SLCE(*sls):
    return {'rings': list(sls)}


def BUD(*buds):
    return {'slices': list(buds)}


class TestSegmentMaker:

    def test_fromList(self):
        func = SegmentMaker().fromList
        assert SEG(None, None, None) == func([])
        assert SEG("a", "a") == func(["a"])
        assert SEG("All", "a") == func(["a", "All"])
        assert SEG("n", "a", "t") == func(["a", "n", "t"])

    def test_fromDict(self):
        func = SegmentMaker().fromDict
        assert SEG(None, None, None) == func({})
        assert SEG(None, None, None) == func({"a": 1})
        assert SEG("N", None, None) == func({"name": "N"})
        assert SEG(None, None, "T") == func({"tooltip": "T"})
        assert SEG("A", "A") == func({"action": "A"})

    def test_make(self):
        func = SegmentMaker().make
        assert SEG("", None, SegmentMaker.PS) == func(None)
        assert SEG("", None, SegmentMaker.PS) == func([])
        assert SEG("", None, SegmentMaker.PS) == func("")
        assert SEG("a", "a") == func("a")
        assert SEG("a", "a") == func(["a"])
        assert SEG("a", "a") == func({"action": "a"})

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
        assert func(None) == RING()
        assert func([]) == RING()
        assert func(["a"]) == RING(SEG("a", "a"))
        assert func(RING("a")) == RING(SEG("a", "a"))
        assert func({"action": "a"}) == RING(SEG("a", "a"))
        assert func(["a", "b"]) == RING(
            SEG("a", "a"), SEG("b", "b"))

        with pytest.raises(bux.BudArgumentError):
            func("a")


class TestSliceMaker:

    def test_fromList(self):
        func = SliceMaker().fromList
        assert func([["a"]]) == [["a"]]
        assert func([RING("a")]) == [RING("a")]

        with pytest.raises(bux.BudSyntaxError):
            assert func("a")
        with pytest.raises(bux.BudSyntaxError):
            assert func(["a"])
        with pytest.raises(bux.BudSyntaxError):
            assert func(SLCE(["a"])) == SLCE(["a"])

    def test_fromDict(self):
        func = SliceMaker().fromDict
        assert func(RING("a")) == [RING("a")]
        assert func(SLCE(["a"])) == [["a"]]

        with pytest.raises(bux.BudSyntaxError):
            func({"slices": ["a"]})
        with pytest.raises(bux.BudSyntaxError):
            func({"rings": ["a"], "some": []})
        with pytest.raises(bux.BudSyntaxError):
            func({"any": ["a"], "some": []})

    def test_make(self):
        func = SliceMaker().make
        assert func(None) == SLCE(RING())
        assert func([["a"]]) == SLCE(RING(SEG("a", "a")))
        assert func(SLCE(["a"])) == SLCE(RING(SEG("a", "a")))
        # assert func(["a"]) == RING([])

        with pytest.raises(bux.BudArgumentError):
            func("a")


# https://pytest.org/latest/fixture.html
@pytest.fixture
def bps():
    return BudParser()


class TestBudParser:
    def test_addEntry(self, bps):
        # It's an accumulating scheme
        assert bps.parse(None) == BUD(SLCE(RING()))
        assert bps.parse("") == BUD(SLCE(RING()), SLCE(RING()))

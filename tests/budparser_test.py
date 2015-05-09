import pytest

from piony.budparser.parser import BudParser


# https://pytest.org/latest/fixture.html
@pytest.fixture
def bps():
    return BudParser()


class TestBudParser:

    def test_addEntry(self, bps):
        assert bps.parse("") == {"slices": [{"rings": [{"segments": []}]}]}

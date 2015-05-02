import pytest

from piony.config.budparser import BudParser


# https://pytest.org/latest/fixture.html
@pytest.fixture
def bps():
    return BudParser()


class TestBudParser:

    def test_addEntry(self, bps):
        pass
        # assert bps.parse_args("")

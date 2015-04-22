from piony.common import *

class TestF_degreeNorm:
    def test_equ(self):
        assert 0 == degreeNorm(0)
        assert 0 == degreeNorm(-360)
        assert 0 == degreeNorm(360)
        assert 350 == degreeNorm(710)
        assert 350 == degreeNorm(-10)


# WARNING: no negative values
class TestF_touchArc:
    def test_len0_equ(self):
        assert arcContains(0,0, 0)
        assert arcContains(90,0, 90)
        assert arcContains(180,0, 180)

    def test_len0_non(self):
        assert not arcContains(0,0, 180)
        assert not arcContains(0,0, 90)
        assert not arcContains(270,0, 90)

    def test_len360_equ(self):
        assert arcContains(0,360, 0)
        assert arcContains(0,360, 90)
        assert arcContains(0,360, 180)
        assert arcContains(0,360, 270)
        assert arcContains(0,360, 360)

    def test_at0(self):
        assert arcContains(0,30, 0)
        assert arcContains(350,30, 0)
        assert arcContains(0,90, 0)
        assert arcContains(0,90, 90)

    def test_at0_ext(self):
        assert arcContains( -20,30, 0)
        assert arcContains( 350,30, 0)
        assert arcContains(-300,50,90)
        assert arcContains( 780,30,90)
        assert arcContains(-740,30, 0)

    def test_infl(self):
        assert not arcContains(0,30, 90)
        assert not arcContains(60,270, 0)
        assert not arcContains(1,358, 0)


class TestF_iround:
    def test_equ(self):
        assert iround(86, 90) == 90
        assert iround(115, 90) == 90

    def test_non(self):
        assert iround(0, 90) == 0
        assert iround(180, 90) == 180

    def test_neg(self):
        assert iround(-83, 90) == -90
        assert iround(-180, 90) == -180


class TestF_lrotate:
    def test_sz(self):
        assert lrotate( [], 1) == []
        assert lrotate([1], 1) == [1]
        assert lrotate([1],-1) == [1]
        assert lrotate([1], 3) == [1]

    def test_in(self):
        assert lrotate([1,2,3], 0) == [1,2,3]
        assert lrotate([1,2,3], 1) == [2,3,1]
        assert lrotate([1,2,3], 2) == [3,1,2]

    def test_wrap(self):
        assert lrotate([1,2,3], 3) == [1,2,3]
        assert lrotate([1,2,3], 7) == [2,3,1]
        assert lrotate([1,2,3],-4) == [3,1,2]


class TestF_ra_xy:
    def test_ra2xy(self):
        assert similar(  [0, 10], ra2xy(10, 90))
        assert similar([8.66, 5], ra2xy(10, 30))

    def test_xy2ra(self):
        assert similar([10, 90], xy2ra(0, 10))
        assert similar([10, 30], xy2ra(8.66, 5))


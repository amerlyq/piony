from PyQt5.QtCore import QRect

from piony.common import similar, ra2xy
from piony.gui.ringsegment import RingSegment


class TestRingSegment():

    def test_points_ra_n90(self):
        assert similar([[-10, 0], [-30, 0], [0, -30], [0, -10]],
                       RingSegment(10, 180, 20, 90).points_ra())
        assert similar([[0, 10], [0, 20], [0, -20], [0, -10]],
                       RingSegment(10, 90, 10, 180).points_ra())
        assert similar([[10, 0], [30, 0], [30, 0], [10, 0]],
                       RingSegment(10, 0, 20, 360).points_ra())

    def test_points_ra_fract(self):
        assert similar([[20, 0], [30, 0], [25.98, 15], [17.32, 10]],
                       RingSegment(20, 0, 10, 30).points_ra())
        assert similar([[20, 0], [30, 0], [-5.21, 29.544], [-3.473, 19.696]],
                       RingSegment(20, 0, 10, 100).points_ra())
        assert similar([[20, 0], [30, 0], [-15, 25.98], [-10, 17.32]],
                       RingSegment(20, 0, 10, 120).points_ra())
        assert similar([[17.32, -10], [25.98, -15], [-21.213, -21.213], [-14.142, -14.142]],
                       RingSegment(20, -30, 10, 255).points_ra())

    ## ---------------

    def test_limitAt_non(self):
        assert similar(0, RingSegment(0, 0, 0, 0).limitAt(0, None))
        assert similar(10, RingSegment(10, 0, 0, 0).limitAt(0, None))
        assert similar(20, RingSegment(10, 0, 10, 0).limitAt(0, None))

    def test_limitAt_pts(self):
        pts = [["0x", "0y"], ["1x", "1y"], ["2x", "2y"], ["3x", "3y"]]
        assert "1x" == RingSegment(10, 30, 10, 20).limitAt(0, pts)
        assert "2y" == RingSegment(10, 30, 10, 20).limitAt(1, pts)
        assert "3x" == RingSegment(10, 30, 10, 20).limitAt(2, pts)
        assert "0y" == RingSegment(10, 30, 10, 20).limitAt(3, pts)

    def test_limitAt_ang(self):
        assert similar(20, RingSegment(10, 350, 10, 20).limitAt(0, None))
        assert similar(20, RingSegment(10, 80, 10, 20).limitAt(1, None))
        assert similar(-20, RingSegment(10, 170, 10, 20).limitAt(2, None))
        assert similar(-20, RingSegment(10, 260, 10, 20).limitAt(3, None))

    def test_limitAt_360(self):
        assert similar(20, RingSegment(10, 0, 10, 360).limitAt(0, None))
        assert similar(20, RingSegment(10, 0, 10, 360).limitAt(1, None))
        assert similar(-20, RingSegment(10, 0, 10, 360).limitAt(2, None))
        assert similar(-20, RingSegment(10, 0, 10, 360).limitAt(3, None))

    ## ---------------

    def test_bbox_ra_non(self):
        assert similar([0, 0, 0, 0], RingSegment(0, 0, 0, 0).bbox_ra())
        assert similar([10, 0, 0, 0], RingSegment(10, 0, 0, 0).bbox_ra())
        assert similar([10, 0, 10, 0], RingSegment(10, 0, 10, 0).bbox_ra())
        assert similar([0, 10, 10, 10], RingSegment(10, 0, 0, 90).bbox_ra())

    # For negative r, dr -- will not work, as bbox vertex indexes changed.
    #   However, expecting: r -- as a+180, dr -- as CW indexing.

    def test_bbox_ra_90(self):
        assert similar([0, 20, 20, 20], RingSegment(10, 0, 10, 90).bbox_ra())
        assert similar([-30, 30, 30, 30], RingSegment(20, 90, 10, 90).bbox_ra())
        assert similar([-20, 0, 20, 20], RingSegment(10, 180, 10, 90).bbox_ra())
        assert similar([0, 0, 20, 20], RingSegment(10, -90, 10, 90).bbox_ra())

    def test_bbox_ra_frac(self):
        assert similar([-20, 20, 40, 20], RingSegment(10, 0, 10, 180).bbox_ra())
        assert similar([-10, 20, 30, 20], RingSegment(10, 0, 10, 120).bbox_ra())

    def test_bbox_ra_arc(self):
        assert similar([-10, 20, 20, 11.34], RingSegment(10, 60, 10, 60).bbox_ra())
        assert similar([-10, -8.66, 20, 11.34], RingSegment(10, 240, 10, 60).bbox_ra())

    ## ---------------

    def test_text_bbox_src(self):
        assert QRect(16, 1, 7, 7) == RingSegment(10, 0, 10, 180).text_bbox_scr()
        assert QRect(1, 16, 7, 7) == RingSegment(10, 0, 10, 358).text_bbox_scr()

    # def test_points_src(self):
        # assert similar([[11, 20], [19, 20], [0, 1], [0, 9]], RingSegment(10, 0, 10, 90).points_scr(1))

    ## ---------------

    def test_geometry(self):
        assert QRect(-10, -20, 20, 20) == RingSegment(10, 0, 10, 90).geometry(0, 0)
        assert QRect(10, 0, 20, 20) == RingSegment(10, 0, 10, 90).geometry(20, 20)
        assert QRect(0, 0, 30, 20) == RingSegment(10, 0, 10, 120).geometry(20, 20)

    def test_geometry_pos(self):
        x0, y0 = 180, 180
        r, dr = 10, 10
        d = r + dr
        pos = [[180, 160], [160, 160], [160, 180], [180, 180]]
        for i in range(0, 3):
            x, y = ra2xy(r, 90*i)
            x += x0
            y = y0 - y
            assert QRect(pos[i][0], pos[i][1], d, d) == RingSegment(r, 90*i, dr, 90).geometry(x, y)

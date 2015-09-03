from .base import BaseLayoutEngine


class RingLayoutEngine(BaseLayoutEngine):
    def applyToItems(self):
        da = float(360) / len(self.items)
        for i, item in enumerate(self.items):
            a = self.rotation + i*da
            item.setBoundings(r=self.r, R=self.R, a=a, A=a+da)

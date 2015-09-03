from .base import BaseLayoutEngine


class SliceLayoutEngine(BaseLayoutEngine):
    def applyToItems(self):
        dr = float(self.R - self.r) / len(self.items)  # Linear distribution
        ds = float(self.spacing) / 2
        for i, item in enumerate(self.items):
            r = self.r + i*dr
            item.setBoundings(r=r+ds, R=r+dr-ds)

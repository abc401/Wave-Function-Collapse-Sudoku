from cell import Cell
from pygame import Rect, Surface

a = [Cell(Surface((2, 2)), i, 0, Rect(1, 1, 0, 0)) for i in range(9)]

b = a[:2]
a.remove(a[1])
print(a)
print(b)

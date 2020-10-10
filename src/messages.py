from collections import namedtuple

LeftMouseDownAt = namedtuple('LeftMouseDownAt', 'pos')
LeftMouseUpAt = namedtuple('LeftMouseUpAt', 'pos')
ColumnWasClicked = namedtuple('ColumnWasClicked', 'column')
MouseMovedTo = namedtuple('MouseMovedTo', 'pos')
Tick = namedtuple('Tick', 'time')
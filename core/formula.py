import typing


class Formula:
    def __init__(
            self,
            function: typing.Callable,
            formula: str,
            xmin: int,
            xmax: int,
            x_coordinates: typing.List[int] = [],
            y_coordinates: typing.List[int] = [],
            expression: str = None
    ):
        self._xmin: int = xmin
        self._xmax: int = xmax
        self._function: typing.Callable = function
        self._formula: str = formula
        self._x_coordinates: typing.List[int] = x_coordinates
        self._y_coordinates: typing.List[int] = y_coordinates
        self._expression: str = expression

    @property
    def xmin(self):
        return self._xmin

    @property
    def xmax(self):
        return self._xmax

    @property
    def formula(self):
        return self._formula

    @property
    def function(self):
        return self._function

    @property
    def x_coordinates(self):
        return self._x_coordinates

    @property
    def y_coordinates(self):
        return self._y_coordinates

    @property
    def expression(self):
        return self._expression

    def set_x_coordinates(self, x_coordinates: typing.List[int]):
        self._x_coordinates = x_coordinates
        return self

    def set_y_coordinates(self, y_coordinates: typing.List[int]):
        self._y_coordinates = y_coordinates
        return self

    def set_expression(self, expression: str):
        self._expression = expression
        return self
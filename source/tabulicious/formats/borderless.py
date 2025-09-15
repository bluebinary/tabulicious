from tabulicious.formats.plaintext import Plaintext

import math


class Borderless(Plaintext):
    _separator: str = None
    _padding: bool = True
    _spacing: int | tuple[int] = None
    _ellipses: bool = False

    def __init__(
        self,
        separator: str = None,
        padding: bool = True,
        spacing: int | tuple[int] = None,
        ellipses: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        if separator is None:
            pass
        elif isinstance(separator, str):
            self._separator = separator
        else:
            raise TypeError(
                "The 'separator' argument, if specified, must have a string value!"
            )

        if isinstance(padding, bool):
            self._padding = padding
        else:
            raise TypeError(
                "The 'padding' argument, if specified, must have an boolean value!"
            )

        if spacing is None:
            self._spacing = (0, 1)
        elif isinstance(spacing, int):
            self._spacing = (0, spacing)
        elif isinstance(spacings := spacing, tuple):
            for spacing in spacings:
                if not isinstance(spacing, int):
                    raise TypeError(
                        "The 'spacing' argument, if specified, must have an integer or tuple of integers value!"
                    )
            self._spacing = spacings
        else:
            raise TypeError(
                "The 'spacing' argument, if specified, must have an integer value or tuple of integers value!"
            )

        if isinstance(ellipses, bool):
            self._ellipses = ellipses
        else:
            raise TypeError(
                "The 'ellipses' argument, if specified, must have an boolean value!"
            )

    def _row(self, row: list[str], header: bool = False):
        table: str = ""

        def font(value: str) -> str:
            if header is True:
                if self._bolding is True:
                    return f"\033[1m{value}\033[0m"
                else:
                    return value
            elif header is False:
                return value

        for index, column in enumerate(row):
            # table += " "

            if column is None:
                value = ""
                length = 0
            else:
                value = str(column)
                length = len(value)
                value = font(value)

            if self._alignments[index] == "right":
                if length < self._widths[index]:
                    table += " " * (self._widths[index] - length)
                    table += value
                elif length > self._widths[index]:
                    table += value[0 : (self._widths[index] - 1)] + "…"
                else:
                    table += value
            elif self._alignments[index] in ["centre", "center"]:
                if length < self._widths[index]:
                    lendiff = self._widths[index] - length
                    lenhalf = math.ceil(lendiff / 2)
                    table += " " * lenhalf
                    table += value

                    if (lenhalf + length + lenhalf) > self._widths[index]:
                        lenhalf = lenhalf - (
                            (lenhalf + length + lenhalf) - self._widths[index]
                        )

                    table += " " * lenhalf
                elif length > self._widths[index]:
                    table += value[0 : (self._widths[index] - 1)] + "…"
                else:
                    table += value
            else:
                if length < self._widths[index]:
                    table += value
                    if self._padding is True:
                        if self._ellipses is True and index == 0:
                            table += "." * (self._widths[index] - length)
                        elif (index + 1) < len(row):
                            table += " " * (self._widths[index] - length)
                elif length > self._widths[index]:
                    table += value[0 : (self._widths[index] - 1)] + "…"
                else:
                    table += value

            if (index + 1) < len(row):
                if self._ellipses is True:
                    table += "." * self._spacing[0]
                elif self._padding is True:
                    table += " " * self._spacing[0]

                if self._separator and index == 0:
                    table += self._separator

                if self._padding is False:
                    if length < self._widths[index]:
                        if self._ellipses is True and index == 0:
                            table += "." * (self._widths[index] - length)
                        elif (index + 1) < len(row):
                            table += " " * (self._widths[index] - length)

                if (index + 1) < len(row):
                    table += " " * self._spacing[1]

        return table

    def string(self) -> str:
        """Generates a plain text formatted table similar to the following:

        ┌───────────┬───────────┬───────────┐
        │ Header 1  │ Header 2  │ Header 3  │
        ├───────────┼───────────┼───────────┤
        │ Column 1A │ Column 1B │ Column 1C │
        ├───────────┼───────────┼───────────┤
        │ Column 2A │ Column 2B │ Column 2C │
        └───────────┴───────────┴───────────┘
        """

        string: str = ""

        # Table Header Row & Row Separator
        if isinstance(self.table.headers, list) and len(self.table.headers) > 0:
            string += self._row(self.table.headers, header=True) + "\n"

        # Table Row Columns & Row Separator
        for index, row in enumerate(self.table.rows, start=1):
            string += self._row(row) + "\n"

        return string

    def print(self):
        """Print the string representation of the table."""

        print(self.string())

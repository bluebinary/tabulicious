from __future__ import annotations

import abc
import tabulicious


class Format(object):
    """The Format base class provides support for creating subclasses that generate
    representations of the provided tabular data such as Plaintext, Markdown & HTML."""

    _table: tabulicious.Tabulicious = None

    def __init__(self, table: tabulicious.Tabulicious, **kwargs):
        self._table = table

    @property
    def table(self) -> tabulicious.Tabulicious:
        return self._table

    @abc.abstractmethod
    def string(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def print(self):
        raise NotImplementedError

from tabulicious import (
    Tabulicious,
    Borderless,
)


def test_table_plaintext_borderless(
    headers: list[str], rows: list[list[object]], data: callable
):
    table = Tabulicious(
        headers=headers,
        rows=rows,
        format=Borderless,
        spacing=3,
    )

    string = table.string()

    assert isinstance(string, str)
    assert string == data("examples/plaintext/borderless.txt")


def test_table_plaintext_borderless_with_separator(
    headers: list[str], rows: list[list[object]], data: callable
):
    table = Tabulicious(
        headers=headers,
        rows=rows,
        format=Borderless,
        spacing=3,
        separator=":",
        padding=False,
    )

    string = table.string()

    assert isinstance(string, str)
    assert string == data("examples/plaintext/borderless-with-separator.txt")


def test_table_plaintext_borderless_no_header(
    headers: list[str], rows: list[list[object]], data: callable
):
    table = Tabulicious(
        rows=rows,
        format=Borderless,
        spacing=3,
        separator=":",
        padding=False,
    )

    string = table.string()

    assert isinstance(string, str)
    assert string == data("examples/plaintext/borderless-no-header.txt")


def test_table_plaintext_borderless_with_ellipses(
    headers: list[str], rows: list[list[object]], data: callable
):
    table = Tabulicious(
        rows=rows,
        format=Borderless,
        spacing=3,
        separator=":",
        padding=False,
        ellipses=True,
    )

    string = table.string()

    assert isinstance(string, str)
    assert string == data("examples/plaintext/borderless-with-ellipses.txt")

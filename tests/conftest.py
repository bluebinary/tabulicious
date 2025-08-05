import sys, os
import pytest
import logging

# Add the library path for importing into the tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "source"))

logger = logging.getLogger(__name__)


# Override the default alphabetic sort of the test modules, into the order we wish to test
TEST_MODULE_ORDER = [
    "test_library_initialisation",
    "test_formatter_plaintext",
    "test_formatter_markdown",
    "test_formatter_html",
    "test_formatter_github",
    "test_formatter_atlassian",
]


def pytest_collection_modifyitems(items):
    """Modifies test items in place to ensure test modules run in the given order."""

    module_mapping = {item: item.module.__name__ for item in items}

    sorted_items = items.copy()

    # Iteratively move tests of each module to the end of the test queue
    for module in TEST_MODULE_ORDER:
        sorted_items = [it for it in sorted_items if module_mapping[it] != module] + [
            it for it in sorted_items if module_mapping[it] == module
        ]

    items[:] = sorted_items


@pytest.fixture(scope="session", name="path")
def path() -> callable:
    """Create a fixture that can be used to obtain the absolute filepath of example data
    files by specifying the path relative to the /tests/data folder."""

    def fixture(path: str, exists: bool = True, extension: bool = True) -> str:
        """Assemble the absolute filepath for the specified example data file."""

        if not isinstance(path, str):
            raise TypeError("The 'path' argument must have a string value!")

        if not isinstance(exists, bool):
            raise TypeError("The 'exists' argument must have a boolean value!")

        if not isinstance(extension, bool):
            raise TypeError("The 'extension' argument must have a boolean value!")

        if extension is True and not (path.endswith(".tiff") or path.endswith(".TIF")):
            path += ".tiff"

        filepath = os.path.join(os.path.dirname(__file__), "data", path)

        if exists is True and not os.path.exists(filepath):
            raise ValueError(
                f"The requested example file, '{filepath}', does not exist!"
            )

        return filepath

    return fixture


@pytest.fixture(scope="session", name="data")
def data() -> callable:
    """Create a fixture that can be used to obtain the contents of example data files as
    strings or bytes by specifying the path relative to the /tests/data folder."""

    def fixture(path: str, binary: bool = False) -> str:
        """Read the specified data file, returning its contents either as a string value
        or if requested in binary mode returning the encoded bytes value."""

        if not isinstance(path, str):
            raise TypeError("The 'path' argument must have a string value!")

        if not isinstance(binary, bool):
            raise TypeError("The 'binary' argument must have a boolean value!")

        filepath = os.path.join(os.path.dirname(__file__), "data", path)

        if not os.path.exists(filepath):
            raise ValueError(
                f"The requested example file, '{filepath}', does not exist!"
            )

        # If binary mode has been specified, adjust the read mode accordingly
        mode: str = "rb" if binary else "r"

        with open(filepath, mode) as handle:
            return handle.read()

    return fixture


@pytest.fixture(name="headers", scope="module")
def headers() -> list[str]:
    return ["Header 1", "Header 2", "Header 3"]


@pytest.fixture(name="rows", scope="module")
def rows() -> list[list[object]]:
    return [
        ["Column 1A", "Column 1B", "Column 1C"],
        ["Column 2A", "Column 2B", "Column 2C"],
    ]

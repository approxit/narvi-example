from pathlib import Path

import pytest

from words.utils.word_grouping import group_words_by_prefix

NAMES_PATH = Path(__file__).with_name("names.csv")


@pytest.fixture
def names():
    with NAMES_PATH.open() as f:
        return [l.strip() for l in f.readlines()]


def _test_word_grouping(names):
    result = group_words_by_prefix(names)

    assert result is None


def test_simple_grouping():
    assert group_words_by_prefix(
        [
            "foo_bar",
            "foo_baz",
        ]
    ) == {
        "foo": [
            "foo_bar",
            "foo_baz",
        ]
    }


def test_nested_grouping():
    assert group_words_by_prefix(
        [
            "foo_bar",
            "foo_bar_baz",
        ]
    ) == {
        "foo_bar": [
            "foo_bar",
            "foo_bar_baz",
        ]
    }


def test_nested_larger_grouping():
    assert group_words_by_prefix(
        [
            "foo_bar",
            "foo_bar_baz",
            "foo_bar_batman",
            "foo_bar_batmobil",
        ]
    ) == {
        "foo_bar": [
            "foo_bar",
            "foo_bar_baz",
            "foo_bar_batman",
            "foo_bar_batmobil",
        ]
    }


def test_multiple_nested_grouping():
    assert group_words_by_prefix(
        [
            "bar_man",
            "bar_mobil",
            "foo_bar",
            "foo_bar_baz",
        ]
    ) == {
        "bar": [
            "bar_man",
            "bar_mobil",
        ],
        "foo_bar": [
            "foo_bar",
            "foo_bar_baz",
        ],
    }


def test_multiple_nested_with_common_parent_grouping():
    assert group_words_by_prefix(
        [
            "fun_bar_man",
            "fun_bar_mobil",
            "fun_foo_bar",
            "fun_foo_bar_baz",
        ]
    ) == {
        "fun_bar": [
            "fun_bar_man",
            "fun_bar_mobil",
        ],
        "fun_foo_bar": [
            "fun_foo_bar",
            "fun_foo_bar_baz",
        ],
    }


def test_ungrouped():
    assert group_words_by_prefix(
        [
            "foo",
            "bar",
            "bat_man",
        ]
    ) == {
        "foo": [
            "foo",
        ],
        "bar": [
            "bar",
        ],
        "bat_man": [
            "bat_man",
        ],
    }


def test_custom_delimiter():
    assert group_words_by_prefix(
        [
            "foo-bar",
            "foo-bar-man",
            "bat-man",
            "bat-mobil",
        ],
        delimiter="-",
    ) == {
        "foo-bar": [
            "foo-bar",
            "foo-bar-man",
        ],
        "bat": [
            "bat-man",
            "bat-mobil",
        ],
    }

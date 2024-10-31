from collections import defaultdict
from typing import Any

MIN_ITEMS_IN_GROUP = 2
# Determines how many entries is required to create a separate prefix group

nested_defaultdict = lambda: defaultdict(nested_defaultdict)


def group_words_by_prefix(words: list[str], delimiter: str = "_") -> dict[str, str]:
    """Return dictionary of words grouped by its common prefix.

    Each word will be available as a dictionary value.

    Examples:
        > group_words_by_prefix(['foo', 'foo_bar', 'bat_man', 'bat_mobil', 'fun'])
        {'foo': ['foo', 'foo_bar'}, 'bat': ['bat_man', 'bat_mobil'], 'fun': ['fun']}

        > group_words_by_prefix(['foo_bar_man', 'foo_bar_fun', 'foo_bat_man', 'foo_bat_mobil])
        {'foo_bar': ['foo_bar_man', 'foo_Bar_fun'}, 'foo_bat': ['foo_bat_man', 'foo_bat_mobil']}
    """
    exploded_collection = _explode_collection(words, delimiter)

    collapsed_collection = defaultdict(list)

    for key, value in exploded_collection.items():
        leftovers = _collapse_collection(value, (key,), collapsed_collection, delimiter)

        if leftovers:
            for leftover in leftovers:
                collapsed_collection[leftover].append(leftover)

    return dict(collapsed_collection)


def _explode_collection(words: list[str], delimiter: str = "_") -> dict[str, Any]:
    """Explode list of given words to nested dictionary.

    Explicit word entry is stored in empty string key.
    """
    exploded_collection = nested_defaultdict()

    for word in words:
        parts = word.split(delimiter)

        current_collection = exploded_collection

        for part in parts:
            current_collection = current_collection[part]

        current_collection[""] = word

    return exploded_collection


def _collapse_collection(
    collection: dict[str, Any],
    keys: tuple[str, ...],
    collapsed_collection: defaultdict[str, list],
    delimiter: str,
) -> list[str]:
    """Iterate over exploded collection gathering entries at the same level.

    If gathered entries exceeds certain amount, they will be added explicitly instead of returning."""

    words = []
    for nested_key, item in collection.items():
        if nested_key == "":
            words.append(item)
        else:
            nested_keys = keys + (nested_key,)
            words.extend(
                _collapse_collection(item, nested_keys, collapsed_collection, delimiter)
            )

    if MIN_ITEMS_IN_GROUP <= len(words):
        collapsed_collection[delimiter.join(keys)].extend(words)

        words.clear()

    return words

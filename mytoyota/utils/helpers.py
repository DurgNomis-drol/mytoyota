"""Helper functions used in multiple places."""


def add_with_none(this, that):
    """Add two items.

    First checking if either item is None.
    """
    if this is None:
        return that
    if that is None:
        return this

    return this + that

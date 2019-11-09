def validate_xor(**kwargs):
    try:
        assert sum(x is not None for x in kwargs.values()) == 1
    except AssertionError:
        raise ValueError(
            f"one and only one of {kwargs.values()} must be non null"
        )


def validate_nand(**kwargs):
    try:
        assert sum(x is not None for x in kwargs.values()) <= 1
    except AssertionError:
        raise ValueError(
            f"no more than one of {kwargs.values()} may be non null"
        )

"""Small executable reference rules for Stage 03 section 3.1."""


def recode_yes_no(value):
    """Map SPSS 1/2 to 1/0 while preserving missing or unsupported codes."""

    if value == 1:
        return 1
    if value == 2:
        return 0
    return None


def recode_rejection(value):
    """Reverse a 1/2 justification item into rejection 0/1."""

    result = recode_yes_no(value)
    return None if result is None else 1 - result


def justified_any(*values):
    """Return NULL only when every justification item is missing."""

    if all(value is None for value in values):
        return None
    return int(any(value == 1 for value in values))

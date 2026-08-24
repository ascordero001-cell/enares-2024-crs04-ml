"""Small executable reference rules for Stage 03 section 3.5."""


def violence_accumulation(*values):
    """Count positive violence contexts, treating missing as zero as specified."""

    return sum(value == 1 for value in values)


def all_violence_forms(*values):
    """Return one only when every required violence form is present."""

    return int(all(value == 1 for value in values))


def consequence_count(values):
    """Preserve NULL unless every consequence item is observed."""

    values = list(values)
    if any(value is None for value in values):
        return None
    return sum(value == 1 for value in values)

"""Small executable reference rules for Stage 03 section 3.4."""


def sexual_form_12m(*, item, recent):
    """A form occurred in the last 12 months only when both flags equal one."""

    return int(item == 1 and recent == 1)


def vs_12m(form_values):
    """Aggregate the sixteen 12-month form indicators using the SPSS rule."""

    return int(any(value == 1 for value in form_values))

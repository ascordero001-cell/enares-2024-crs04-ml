"""Executable reference semantics for CRS04 school indicators."""


def school_form(
    *,
    item,
    gateway,
    confirmation_a,
    confirmation_c,
    confirmation_e,
):
    """Reproduce one C3P223 psychological-violence school form."""

    return int(
        item == 1
        and gateway == 1
        and (
            confirmation_a == 1
            or confirmation_c == 1
            or confirmation_e == 1
        )
    )


def vp_escuela(form_values):
    """Aggregate the fourteen school-form indicators."""

    return int(any(value == 1 for value in form_values))
"""Executable reference semantics for CRS04 household indicators."""

VALID_DIRECT_PERPETRATOR_CODES = {1, 2, 3, 4, 19}


def household_form(
    *,
    sexo,
    item,
    gateway,
    perpetrator_a,
    perpetrator_e,
    confirm_c,
    confirm_d,
    confirm_f,
):
    """Reproduce one C3P201 household psychological-violence form."""

    if sexo not in {1, 2}:
        return 0

    if item != 1 or gateway != 1:
        return 0

    direct_match = (
        perpetrator_a in VALID_DIRECT_PERPETRATOR_CODES
        or perpetrator_e in VALID_DIRECT_PERPETRATOR_CODES
    )

    confirmed_a = (
        perpetrator_a is not None
        and perpetrator_a not in VALID_DIRECT_PERPETRATOR_CODES
        and confirm_c == 1
        and confirm_d == 1
    )

    confirmed_e = (
        perpetrator_e is not None
        and perpetrator_e not in VALID_DIRECT_PERPETRATOR_CODES
        and confirm_f == 1
    )

    return int(direct_match or confirmed_a or confirmed_e)


def vp_hogar(form_values):
    """Aggregate the eleven form indicators using the SPSS 0/1 rule."""

    return int(any(value == 1 for value in form_values))
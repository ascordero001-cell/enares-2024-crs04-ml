"""Small executable reference rules for Stage 03 section 3.6."""


def recode_yes_no(value):
    """Map SPSS 1/2 to 1/0 and preserve all other states as NULL."""

    if value == 1:
        return 1
    if value == 2:
        return 0
    return None


def received_help_for_victim(*, victim, response):
    """Apply the victim universe and preserve the explicit code-3 nonresponse."""

    if victim != 1:
        return None
    if response == 3:
        return None
    return int(response == 1)


def help_gap(*, searched, received):
    """Measure an unmet-help gap only among adolescents who sought help."""

    if searched != 1 or received not in {0, 1}:
        return None
    return int(received == 0)

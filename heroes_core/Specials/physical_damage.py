"""
Module with methods to calculate physical damage modifiers
Each method take 1 argument unit, which have modifiers,
    returns modifiers for given unit
"""

from heroes_core.TMP_some_constants import DEFENCE_MULT


def ignore_defence(unit):
    """
    ignore 80% of target armor
    _39_ old code

    :param unit: unit with modifier
    :return: modifiers
    """
    return {DEFENCE_MULT: 0.2}

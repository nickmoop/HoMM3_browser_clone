"""
Module with methods to calculate physical damage modifiers
Each method take 1 argument unit, which have modifiers,
    returns modifiers and log message dict for given unit
"""

from heroes_core.TMP_some_constants import DEFENCE_MULT, LOG_MESSAGE


def ignore_defence(unit):
    """
    ignore 80% of target armor
    _39_ old code

    :param unit: unit with modifier
    :return: modifiers and log message
    """
    return {DEFENCE_MULT: 0.2, LOG_MESSAGE: 'ignore 80% armor'}

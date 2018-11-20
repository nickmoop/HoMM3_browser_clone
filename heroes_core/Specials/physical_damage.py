"""
Module with methods to calculate physical damage modifiers
Each method take 2 argument attacker and defender units
    returns modifiers and log message dict for given unit
"""

from heroes_core.TMP_some_constants import (
    DEFENCE_MULT, LOG_MESSAGE, DAMAGE_MULT
)
from heroes_core.helper_methods import cells_distance


def ignore_defence(attacker, defender):
    """
    ignore 80% of target armor
    _39_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: modifiers and log message
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    return {DEFENCE_MULT: 0.2, LOG_MESSAGE: 'ignore 80% armor'}


def jousting(attacker, defender):
    """
    +5% damage per cell from attacker to defender
    _51_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: attack modifier
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    distance = int(
        cells_distance(attacker.cell_coordinates, defender.cell_coordinates)
    )
    if distance < 0:
        distance = 0

    return {
        DAMAGE_MULT: 1 + distance * 0.05,
        LOG_MESSAGE: '{} jousting {} for {} hexes distance\n'.format(
            attacker.name, defender.name, distance)
    }

"""
Module with all possible positive effects.
Each effect take 1 argument - unit to take effect, returns modifiers dict
"""

from heroes_core.TMP_some_constants import (
    SPEED_ADD, DEFENCE_ADD, ATTACK_ADD, DAMAGE
)


def haste_basic(unit):
    """
    +3 hexes

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {SPEED_ADD: 3}


def haste_advanced(unit):
    """
    +5 hexes

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {SPEED_ADD: 5}


def stone_skin_basic(unit):
    """
    +3 defence rating

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {DEFENCE_ADD: 3}


def stone_skin_advanced(unit):
    """
    +6 defence rating

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {DEFENCE_ADD: 6}


def bloodlust_basic(unit):
    """
    +3 attack rating

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {ATTACK_ADD: 3}


def bloodlust_advanced(unit):
    """
    +6 attack rating

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {ATTACK_ADD: 6}


def bless_basic(unit):
    """
    unit do maximum damage

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {DAMAGE: unit.maximum_damage}


def bless_advanced(unit):
    """
    unit do maximum damage +1

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {DAMAGE: unit.maximum_damage + 1}

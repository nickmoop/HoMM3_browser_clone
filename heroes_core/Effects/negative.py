"""
Module with all possible negative effects.
Each effect take 1 argument - unit to take effect, returns modifiers dict
"""

from heroes_core.TMP_some_constants import (
    ATTACK_ADD, DEFENCE_ADD, DAMAGE, DAMAGE_MULT, HEALTH_MULT, SPEED_MULT
)


def diseased(unit):
    """
    -2 Attack -2 Defence to unit
    neg.2 old code

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {DEFENCE_ADD: -2, ATTACK_ADD: -2}


def cursed(unit):
    """
    cursed unit deal minimum damage
    neg.5 old code

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {DAMAGE: unit.minimum_damage}


def wicked(unit):
    """
    -3 Attack skill to unit
    neg.7 old code

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {ATTACK_ADD: -3}


def stoned(unit):
    """
    -50% damage to stoned unit
    stone effect dispelling after attack
    neg.8 old code

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    unit.dispel_effect('stoned')

    return {DAMAGE_MULT: 0.5, SPEED_MULT: 0}


def paralyzed(unit):
    """
    paralyzed effect dispelling after attack

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    unit.dispel_effect('paralyzed')

    return {SPEED_MULT: 0}


def aged(unit):
    """
    -50% maximum health
    neg.4 old code

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {HEALTH_MULT: 0.5}


def poisoned(unit):
    """
    -10% unit maximum health each turn
    neg.6 old code

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {HEALTH_MULT: 0.1 * (4 - unit.effects['poisoned']['duration'])}


def slow_basic(unit):
    """
    slow speed for 25%

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {SPEED_MULT: 0.75}


def slow_advanced(unit):
    """
    slow speed for 50%

    :param unit: unit to take effect
    :return: unit stats modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    return {SPEED_MULT: 0.5}

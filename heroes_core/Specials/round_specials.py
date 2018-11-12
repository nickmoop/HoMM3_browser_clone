"""
Special methods casts every round starts
Each method take 1 argument - unit which have special skill,
    returns modifiers, or change unit attributes
"""

from heroes_core.TMP_some_constants import GUEST_MP_ADD, CREATOR_MP_ADD, GUEST


def unlimited_retaliations(unit):
    """
    each unit have only 1 retaliation attack per round,
    this unit have unlimited attacks
    _50_ old code

    :param unit: unit to take special every round
    :return: modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    unit.retaliation = 100
    return {}


def regeneration(unit):
    """
    fully regen hp each round
    _28_ old code

    :param unit: unit to take special every round
    :return: modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    unit.take_heal(1000)
    return {}


def drain_mana(unit):
    """
    drain 2 mana points of enemy hero each round
    _29_ old code

    :param unit: unit to take special every round
    :return: modifiers
    :type unit: BattleUnit
    :rtype: dict
    """
    if unit.role == GUEST:
        mana_modifiers = {GUEST_MP_ADD: 2, CREATOR_MP_ADD: -2}
    else:
        mana_modifiers = {GUEST_MP_ADD: -2, CREATOR_MP_ADD: 2}

    return mana_modifiers

"""
Special methods for taking casts by units
Each method take 1 argument spell, which casted on unit,
    returns modifiers for unit
"""

from heroes_core.TMP_some_constants import DAMAGE_MULT


def immune_to_five_and_less_level_spells(spell):
    """
    immune to all spells which level 5 or less (black dragon)
    _10_ old code

    :param spell: spell which casted on unit
    :return: modifiers for it spell
    :type spell: BattleSpell
    :rtype: dict
    """
    if spell.level <= 5:
        return {DAMAGE_MULT: 0}

    return {}


def immune_to_4_and_less_level_spells(spell):
    """
    immune to all spells which level 4 or less (gold dragon)

    :param spell: spell which casted on unit
    :return: modifiers for it spell
    :type spell: BattleSpell
    :rtype: dict
    """
    if spell.level <= 4:
        return {DAMAGE_MULT: 0}

    return {}


def only_take_40_percent_of_spell_damage(spell):
    """
    only take 40% of damage by spells (iron golem)
    _40_ old code

    :param spell: spell which casted on unit
    :return: modifiers for it spell
    :type spell: BattleSpell
    :rtype: dict
    """
    if getattr(spell, 'damage', 0):
        return {DAMAGE_MULT: 0.25}

    return {}


def blind_immune(spell):
    """
    immune to blind (troglodyte)
    _4_ old code

    :param spell: spell which casted on unit
    :return: modifiers for it spell
    :type spell: BattleSpell
    :rtype: dict
    """
    if spell.name == 'Blind':
        return {DAMAGE_MULT: 0}

    return {}

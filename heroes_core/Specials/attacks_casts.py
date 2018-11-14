"""
Possible casts when attacker unit attack defender unit.
Each method take 2 arguments - attacker unit, defender unit
    returns empty dict if cast no procs,
    log message in dict and change attacker or defender attributes if cast proc
For more information look at resources/Spell/Neutral/spell_name_here
"""

import random

from heroes_core.Spell import ALL_SPELLS
from heroes_core.TMP_some_constants import LOG_MESSAGE
from heroes_core.helper_methods import range_damage


def binding(attacker, defender):
    """
    bind defender to current position
    _46_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict if cast not procs, log message in dict if cast procs
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    return {LOG_MESSAGE: defender.take_spell(ALL_SPELLS['Neutral_Binding'])}


def stone_gaze(attacker, defender):
    """
    20% chance to cast stone gaze on defender
    _8_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict if cast not procs, log message in dict if cast procs
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    range_damage_koeff = range_damage(
        attacker.cell_coordinates, defender.cell_coordinates)
    if 'ranged' in attacker.special and range_damage_koeff:
        return {}
    elif random.randint(0, 100) <= 20:
        return {
            LOG_MESSAGE: defender.take_spell(ALL_SPELLS['Neutral_Stone_gaze'])
        }


def paralyze(attacker, defender):
    """
    20% chance to cast paralyze on defender

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict if cast not procs, log message in dict if cast procs
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if random.randint(0, 100) <= 20:
        return {
            LOG_MESSAGE: defender.take_spell(ALL_SPELLS['Neutral_Paralyze'])
        }

    return {}


def blind(attacker, defender):
    """
    20% chance to cast blind on defender

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict if cast not procs, log message in dict if cast procs
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if random.randint(0, 100) <= 20:
        return {
            LOG_MESSAGE: defender.take_spell(ALL_SPELLS['Neutral_Blind'])
        }

    return {}


def lightning_strike(attacker, defender):
    """
    20% chance to cast lightning strike on defender
    _38_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if random.randint(0, 100) <= 20:
        spell = ALL_SPELLS['Neutral_Lightning_Strike']
        spell.damage = eval(spell.formula)
        return {LOG_MESSAGE: defender.take_spell(spell)}

    return {}


def curse(attacker, defender):
    """
    20% chance to cast curse on defender
    _32_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if random.randint(0, 100) <= 20:
        return {LOG_MESSAGE: defender.take_spell(ALL_SPELLS['Neutral_Curse'])}

    return {}


def disease(attacker, defender):
    """
    20% chance to cast disease on defender
    _27_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if random.randint(0, 100) <= 20:
        return {
            LOG_MESSAGE: defender.take_spell(ALL_SPELLS['Neutral_Disease'])
        }

    return {}


def poisonous(attacker, defender):
    """
    20% chance to cast poison on defender, -10% of maximum health each turn
    _16_old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if random.randint(0, 100) <= 20:
        return {LOG_MESSAGE: defender.take_spell(ALL_SPELLS['Neutral_Poison'])}

    return {}


def weakness(attacker, defender):
    """
    cast weakness on defender, -defence, -attack skill to defender unit
    _13_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if 'wicked' not in defender.effects.keys():
        return {
            LOG_MESSAGE: defender.take_spell(ALL_SPELLS['Neutral_Weakness'])
        }

    return {}


def aging(attacker, defender):
    """
    20% chance to age enemy, maximum unit health *= 0.5
    _35_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if random.randint(0, 100) <= 20:
        return {LOG_MESSAGE:defender.take_spell(ALL_SPELLS['Neutral_Aging'])}

    return {}


def dispels(attacker, defender):
    """
    remove all positive spells from defender unit
    _14_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    for positive_effect_name in defender.positive_effects:
        return {LOG_MESSAGE: defender.dispel_effect(positive_effect_name)}

    return {}

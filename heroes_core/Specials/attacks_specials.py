"""
Specials attack methods, like additional damage to some kind of units,
ranged attacks calculation, etc.
Each method take 2 arguments - attacker unit, defender unit
    returns dict with modifiers and log message to attacker unit,
    or change defender attributes
"""

import random

from heroes_core.helper_methods import range_damage, cells_distance
from heroes_core.TMP_some_constants import DAMAGE_MULT, LOG_MESSAGE


def death_stare(attacker, defender):
    """
    10% chance (per 10 attacker units) to kill defender top creature
    decrease defender stack size if procs
    _15_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: empty dict if cast not procs, log message in dict if cast procs
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    chance = int(attacker.stack / 10) * 10
    if random.randint(0, 100) <= chance:
        defender.stack -= 1
        return {
            LOG_MESSAGE: 'After {} death stare, {} one unit dead\n'.format(
                attacker.name, defender.name
            )
        }

    return {}


def ranged(attacker, defender):
    """
    archers damage *= 0.5 in melee and *= 0.5 after 10 hexes range
    _1_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: ranged attack modifiers and log message in dict
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    range_damage_koeff = range_damage(
        attacker.cell_coordinates, defender.cell_coordinates)

    # range attack to defender
    if range_damage_koeff:
        return {
            DAMAGE_MULT: range_damage_koeff,
            LOG_MESSAGE: '{} shoot {}. {} damage coefficient\n'.format(
                attacker.name, defender.name, range_damage_koeff)
        }
    # melee attack to defender
    else:
        # no penalty for melee
        if 'no_melee_penalty' in attacker.special:
            return {
                DAMAGE_MULT: 1,
                LOG_MESSAGE: '{} hit {} without melee penalty\n'.format(
                    attacker.name, defender.name)
            }
        # penalty for melee
        return {
            DAMAGE_MULT: 0.5,
            LOG_MESSAGE: '{} hit {} with melee penalty\n'.format(
                attacker.name, defender.name)
        }


def hate_titan(attacker, defender):
    """
    150% damage if defender titans
    _11_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: attack modifiers, 1.5 for special named unit, 1 for each other
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """

    if 'Titan' in defender.name:
        return {
            DAMAGE_MULT: 1.5,
            LOG_MESSAGE: '{} hate {}. Do 150% damage\n'.format(
                attacker.name, defender.name)
        }

    return {DAMAGE_MULT: 1}


def hate_master_genie(attacker, defender):
    """
    150% damage if defender master genies
    _22_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: attack modifiers, 1.5 for special named unit, 1 for each other
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if 'Master_Genie' in defender.name:
        return {
            DAMAGE_MULT: 1.5,
            LOG_MESSAGE: '{} hate {}. Do 150% damage\n'.format(
                attacker.name, defender.name)
        }

    return {DAMAGE_MULT: 1}


def hate_archangel(attacker, defender):
    """
    150% damage if defender archangels
    _25_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: attack modifiers, 1.5 for special named unit, 1 for each other
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if 'Archangel' in defender.name:
        return {
            DAMAGE_MULT: 1.5,
            LOG_MESSAGE: '{} hate {}. Do 150% damage\n'.format(
                attacker.name, defender.name)
        }

    return {DAMAGE_MULT: 1}


def hate_efreet_sultan(attacker, defender):
    """
    150% damage if defender efreet sultan
    _42_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: attack modifiers, 1.5 for special named unit, 1 for each other
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if 'Efreet_Sultan' in defender.name:
        return {
            DAMAGE_MULT: 1.5,
            LOG_MESSAGE: '{} hate {}. Do 150% damage\n'.format(
                attacker.name, defender.name)
        }

    return {DAMAGE_MULT: 1}


def hate_black_dragon(attacker, defender):
    """
    150% damage if defender black dragon
    _44_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: attack modifiers, 1.5 for special named unit, 1 for each other
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if 'Black_Dragon' in defender.name:
        return {
            DAMAGE_MULT: 1.5,
            LOG_MESSAGE: '{} hate {}. Do 150% damage\n'.format(
                attacker.name, defender.name)
        }

    return {DAMAGE_MULT: 1}


def hate_archdevil(attacker, defender):
    """
    150% damage if defender arch devil
    _52_ old code

    :param attacker: attacker unit
    :param defender: defender unit
    :return: attack modifiers, 1.5 for special named unit, 1 for each other
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if 'Arch_Devil' in defender.name:
        return {
            DAMAGE_MULT: 1.5,
            LOG_MESSAGE: '{} hate {}. Do 150% damage\n'.format(
                attacker.name, defender.name)
        }

    return {DAMAGE_MULT: 1}


def death_blow(attacker, defender):
    """
    20% chance to do double damage to defender
    _33_ old code


    :param attacker: attacker unit
    :param defender: defender unit
    :return: attack modifiers, 2 if special procs, 1 if not procs
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :rtype: dict
    """
    if random.randint(0, 100) <= 20:
        return {
            DAMAGE_MULT: 2,
            LOG_MESSAGE: '{} make death blow to {}. Do x2 damage\n'.format(
                attacker.name, defender.name)
        }

    return {DAMAGE_MULT: 1}


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
    distance = cells_distance(
        attacker.cell_coordinates, defender.cell_coordinates)
    if distance < 0:
        distance = 0

    return {
        DAMAGE_MULT: 1 + distance * 0.05,
        LOG_MESSAGE: '{} jousting {} for {} hexes distance\n'.format(
            attacker.name, defender.name, distance)
    }

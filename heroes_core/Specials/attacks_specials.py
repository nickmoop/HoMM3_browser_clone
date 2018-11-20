"""
Specials attack methods, like additional damage to some kind of units,
attacks calculation, etc.
Each method take 2 arguments - attacker unit, defender unit
    returns dict with modifiers and log message to attacker unit,
    or change defender attributes
"""

import random

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

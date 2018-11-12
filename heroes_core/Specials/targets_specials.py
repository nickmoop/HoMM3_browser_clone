"""
Module with all possible types of aoe attacks.
Each effect take arguments: attacker unit, defender unit, all units dict,
    returns modifier, with list of additional targets (if units in range), or
    with empty list
"""

from heroes_core.helper_methods import dragon_breath_coordinates, range_damage
from heroes_core.TMP_some_constants import TARGETS_ADD


def dragon_breath(attacker, defender, units):
    """
    dragon breath, possible to attack 1 additional unit,
    who stay on line of attack
    _12_ old code

    :param attacker: unit who attack defender unit
    :param defender: defender unit
    :param units: all units
    :return: additional target modifier (list of targets in dict or empty dict)
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :type units: dict
    :rtype: dict
    """
    attacker_coords = attacker.cell_coordinates
    target_coords = defender.cell_coordinates
    second_target_coords = dragon_breath_coordinates(
        attacker_coords, target_coords)
    for unit in units.values():
        if second_target_coords in unit.coordinates and unit != defender:
            return {TARGETS_ADD: [unit]}

    return {}


def attack_all_nearby_units(attacker, defender, units):
    """
    attack all nearby units around attacker, DO NOT attack same unit twice
    _17_ old code

    :param attacker: unit who attack defender unit
    :param defender: defender unit
    :param units: all units
    :return: additional target modifier (list of targets in dict or empty dict)
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :type units: dict
    :rtype: dict
    """
    attack_coords = {coordinates: '' for coordinates in attacker.coordinates}
    additional_targets = list()
    attacker.calculate_attack_cells(attack_coords, units)

    for unit in units:
        if attacker.role == unit.role:
            continue

        for coordinates in unit.coordinates:
            if coordinates in attack_coords:
                if unit not in additional_targets:
                    additional_targets.append(unit)

    return {TARGETS_ADD: additional_targets}


def attack_units_in_front(attacker, defender, units):
    """
    attack 3 target in front of attacker unit
    _20_ old code

    :param attacker: unit who attack defender unit
    :param defender: defender unit
    :param units: all units
    :return: additional target modifier (list of targets in dict or empty dict)
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :type units: dict
    :rtype: dict
    """
    attacker_coords = attacker.cell_coordinates
    target_coords = defender.cell_coordinates
    if attacker_coords[1] != target_coords[1]:

        if (attacker_coords[0] - target_coords[0]) > 0:
            second_target_coords = [attacker_coords[0] - 1, attacker_coords[1]]
            third_target_coords = [target_coords[0] + 1, target_coords[1]]

        elif (attacker_coords[0] - target_coords[0]) < 0:
            second_target_coords = [attacker_coords[0] + 1, attacker_coords[1]]
            third_target_coords = [target_coords[0] - 1, target_coords[1]]

        else:
            if attacker_coords[1] % 2 == 0:
                third_target_coords = [target_coords[0] + 1, target_coords[1]]
                second_target_coords = [
                    attacker_coords[0] - 1, attacker_coords[1]]
            else:
                third_target_coords = [target_coords[0] - 1, target_coords[1]]
                second_target_coords = [
                    attacker_coords[0] + 1, attacker_coords[1]]
    else:

        if attacker_coords[1] % 2 == 0:
            add_x = 1
        else:
            add_x = 0

        if (attacker_coords[0] - target_coords[0]) > 0:
            second_target_coords = [
                target_coords[0] + add_x, attacker_coords[1] - 1]
            third_target_coords = [
                target_coords[0] + add_x, attacker_coords[1] + 1]
        else:
            second_target_coords = [
                target_coords[0] + add_x - 1, attacker_coords[1] - 1]
            third_target_coords = [
                target_coords[0] + add_x - 1, attacker_coords[1] + 1]

    list_of_possible_cells = [second_target_coords, third_target_coords]
    additional_targets = list()
    for unit in units.values():
        if attacker.role == unit.role:
            continue

        for coordinates in unit.coordinates:
            if coordinates in list_of_possible_cells:
                if unit not in additional_targets and unit != defender:
                    additional_targets.append(unit)

    return {TARGETS_ADD: additional_targets}


def hit_twice(attacker, defender, units):
    """
    double hit defender unit
    _36_ old code

    :param attacker: unit who attack defender unit
    :param defender: defender unit
    :param units: all units
    :return: additional target modifier (list of targets in dict or empty dict)
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :type units: dict
    :rtype: dict
    """
    return {TARGETS_ADD: [defender]}


def shoot_twice(attacker, defender, units):
    """
    double shoot defender unit
    _49_ old code

    :param attacker: unit who attack defender unit
    :param defender: defender unit
    :param units: all units
    :return: additional target modifier (list of targets in dict or empty dict)
    :type attacker: BattleUnit
    :type defender: BattleUnit
    :type units: dict
    :rtype: dict
    """
    if range_damage(attacker.cell_coordinates, defender.cell_coordinates):
        return {TARGETS_ADD: [defender]}

    return {}

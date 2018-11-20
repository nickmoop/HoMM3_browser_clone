from heroes_core.TMP_some_constants import DAMAGE_MULT, LOG_MESSAGE, MOVE_UNIT
from heroes_core.helper_methods import range_damage, get_nearby_cells


def ranged(attacker, defender, units):
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

    attacker_nearby_cells = set()
    for coordinates in attacker.coordinates:
        attacker_nearby_cells = attacker_nearby_cells.union(
            get_nearby_cells(coordinates))

    is_enemy_close = False
    for unit in units.values():
        if unit.role == attacker.role:
            continue

        is_enemy_close = attacker_nearby_cells.intersection(unit.coordinates)
        if is_enemy_close:
            break

    if is_enemy_close:
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

    range_damage_koeff = range_damage(
        attacker.cell_coordinates, defender.cell_coordinates)

    # range attack to defender
    return {
        DAMAGE_MULT: range_damage_koeff,
        MOVE_UNIT: False,
        LOG_MESSAGE: '{} shoot {}. {} damage coefficient\n'.format(
            attacker.name, defender.name, range_damage_koeff)
    }

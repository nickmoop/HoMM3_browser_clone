"""
Special methods happens after some unit attack other unit
Each method take 2 arguments - damage taken by unit,
    target unit to take effect of special
    returns empty dict (to be same as other specials),
    and change target unit attributes
"""

from heroes_core.Spell import ALL_SPELLS


def life_drain(damage, target_unit):
    """
    restore target unit by amount of damage made by target unit
    can resurrect units in stack, but no more than maximum units in stack
    _30_ old code

    :param damage: amount of damage which make target_unit to some unit
    :param target_unit: unit which make damage, unit to restore
    :return: empty dict
    :type damage: int
    :type target_unit: BattleUnit
    :rtype: dict
    """
    target_unit.take_restoration(damage)

    return {}


def fire_shield(damage, target_unit):
    """
    return half of taken damage to attacker (to target unit)
    damage value used in eval(formula)
    _23_ old code

    :param damage: amount of damage which make target_unit to some unit
    :param target_unit: unit which make damage, unit to take half damage back
    :return: empty dict
    :type damage: int
    :type target_unit: BattleUnit
    :rtype: dict
    """
    spell = ALL_SPELLS['Fire_Fire_Shield']
    spell.damage = eval(spell.formula)
    target_unit.take_spell(spell)

    return {}

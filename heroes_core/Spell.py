"""
Module to contain spells classes.
Heroes3Spell class is for all general spell, using for fast access to spell
BattleSpell class is spells of the hero of the battle
"""

from heroes_core.Resource import Resource
from heroes_core.TMP_some_constants import RESOURCES, SPELL, SORTING_PARAMETER


class Heroes3Spell(Resource):
    """
    Base spell resource class
    using to define all "abstract" spells,
    spells should be defined right before battle, using player stats
    """

    # redefine sorting parameter name for spell resources
    sorting_parameter_name = RESOURCES[SORTING_PARAMETER][SPELL]


class BattleSpell(object):
    """
    Defined spells class which using in battle
    Spells defined by using player stats
    using in player model to avoid spells resources recalculations each time
    when player want to cast some spell
    """

    def __init__(self, attributes):
        """
        Can make class instance only by using dict of attributes

        :param attributes: battle spell class attributes
        :type attributes: dict
        """
        for key, value in attributes.items():
            self.__dict__[key] = value

    @classmethod
    def to_json(cls, spells):
        """
        Serialize BattleSpells dict (with Heroes3Spell.key as key and
        BattleSpell as value) to json

        :param spells: dict with spell.key as key and BattleSpell as value
        :return: BattleSpells serialized to json
        :type spells: dict
        :rtype: dict
        """
        spells_dict = dict()
        for spell_key, battle_spell in spells.items():
            spells_dict[spell_key] = battle_spell.__dict__

        return spells_dict

    @classmethod
    def from_json(cls, spells_dict):
        """
        Deserialize json to BattleSpells dict (with Heroes3Spell.key as key and
        BattleSpell as value)

        :param spells_dict: BattleSpells serialized to json
        :return: dict with spell.key as key and BattleSpell as value
        :type spells_dict: dict
        :rtype: dict
        """
        spells = dict()
        for key, value in spells_dict.items():
            spells[key] = BattleSpell(value)

        return spells


# all spells from json files to memory storage
ALL_SPELLS = Heroes3Spell.load_resources()

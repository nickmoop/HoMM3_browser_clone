"""
Module with useful constant variables values
"""

# resources constants
UNIT = 'Unit'
SPELL = 'Spell'
NAME = 'Name'
SORTING_PARAMETER = 'Sorting parameter'
RESOURCES = {
    NAME: {
        UNIT: UNIT,
        SPELL: SPELL
    },
    SORTING_PARAMETER: {
        UNIT: 'castle',
        SPELL: 'school'
    }
}

# players constants
CREATOR = 'creator'
GUEST = 'guest'
BATTLE_START_CELLS = {
    'initial_cell': {
        CREATOR: 14,
        GUEST: 0
    },
    'big_initial_cell': {
        CREATOR: 13,
        GUEST: 1
    },
    'start_side': {
        CREATOR: 'right',
        GUEST: 'left'
    }
}

# specials constants
ATTACK_ADD = 'additional attack'
DEFENCE_ADD = 'additional defence'
DEFENCE_MULT = 'defence multipicator'
DAMAGE = 'damage'
DAMAGE_ADD = 'additional damage'
DAMAGE_MULT = 'damage multiplicator'
TARGETS_ADD = 'additional targets'
HEALTH_MULT = 'health multiplicator'
GUEST_MP_ADD = 'additional mana to guest'
CREATOR_MP_ADD = 'additional mana to creator'
SPEED_ADD = 'additional speed hexes'
SPEED_MULT = 'speed multiplicator'

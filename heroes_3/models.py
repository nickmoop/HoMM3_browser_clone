import json
import re

from django.db import models
from django.middleware.csrf import get_token
from django.shortcuts import redirect

from heroes_3 import forms
from heroes_core.Spell import BattleSpell
from heroes_core.Unit import BattleUnit
from heroes_core.helper_methods import (
    get_csrf_token_from_request, get_nearby_cells
)
from heroes_core.TMP_some_constants import GUEST_MP_ADD, CREATOR, GUEST


class Battles(models.Model):
    name = models.CharField(max_length=60)
    state = models.CharField(max_length=10)
    creator = models.ForeignKey(
        'Players', related_name='creator',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    guest = models.ForeignKey(
        'Players', related_name='guest',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    creator_castle = models.CharField(max_length=20)
    guest_castle = models.CharField(max_length=20, null=True)
    growth = models.IntegerField()
    log = models.CharField(max_length=20000, null=True)
    _units = models.CharField(max_length=20000, null=True)

    @classmethod
    def get_empty_battles(cls):
        return cls.objects.filter(state='empty')

    def add_units(self, new_units):
        units = self.units
        units.update(BattleUnit.to_json(new_units))
        self._units = json.dumps(units)
        self.save()

    def update_units(self, new_units):
        self._units = json.dumps(BattleUnit.to_json(new_units))
        self.save()

    def calculate_rating(self, winner_role):
        looser_role = [CREATOR, GUEST]
        if winner_role in looser_role:
            looser_role.remove(winner_role)
            looser_role = looser_role[0]

        winner = getattr(self, winner_role)
        looser = getattr(self, looser_role)
        winner.rating += 10
        winner.experience += 100 * self.growth
        winner.win_count += 1
        looser.loose_count += 1
        looser.rating -= 10
        winner.save()
        looser.save()

    def next_round(self, units):
        for unit in units.values():
            unit.turn = 1
            unit.retaliation = 1
            unit.decrease_effects_duration()

            for method in unit.round_specials:
                tmp_modifier = method(unit)
                # TODO make me!!
                guest_mp_add = tmp_modifier.get(GUEST_MP_ADD, None)

        self.update_units(units)
        self.save()

    @property
    def units(self):
        if self._units:
            return json.loads(self._units)

        return dict()


def create_battle(create_battle_form, creator_user):
    new_battle = Battles(
        name=create_battle_form.cleaned_data['name'],
        state='empty',
        creator=creator_user.player,
        creator_castle=create_battle_form.cleaned_data['creator_castle'],
        growth=create_battle_form.cleaned_data['growth'],
    )
    new_battle.save()
    creator_user.player.current_mp = creator_user.player.maximum_mp
    creator_user.player.save()

    creator_user.update_battle(new_battle)

    return new_battle


class Users(models.Model):
    user_name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    token = models.CharField(max_length=80, null=True)
    player = models.ForeignKey(
        'Players',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    battle = models.ForeignKey(
        'Battles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def update_battle(self, battle):
        self.battle = battle
        self.save()

    def update_user_token(self, token):
        self.token = token
        self.save()


def register_new_user(request, token=None):
    form = forms.Registration(request.POST)
    if not form.is_valid():
        return None

    if not token:
        token = get_token(request)

    user_name = form.cleaned_data['user_name']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']

    user = Users.objects.filter(user_name=user_name, email=email)
    if user:
        return None

    new_player = Players(nick_name=user_name)
    new_player.save()
    new_user = Users(
        user_name=user_name, email=email, password=password, player=new_player)
    new_user.save()
    new_user.update_user_token(token)

    return new_user


def get_user_by_token(token):
    users = Users.objects.filter(token=token)

    if not users:
        return None

    if len(users) > 1:
        for user in users:
            user.update_user_token(None)

        return None

    return users[0]


def is_logged_in(function):
    def new_func(*original_args, **original_kwargs):
        token = get_csrf_token_from_request(original_args[1])
        user = get_user_by_token(token)

        if user is None:
            return redirect('user_login')
        else:
            return function(*original_args, **original_kwargs)

    return new_func


def login_user_by_password(request, token=None):
    form = forms.Login(request.POST)
    if not form.is_valid():
        return None

    user = check_username_password(form)
    if not user:
        return None

    if not token:
        token = get_token(request)

    user.update_user_token(token)

    return token


def check_username_password(login_form):
    user_name = login_form.cleaned_data['user_name']
    password = login_form.cleaned_data['password']

    try:
        user = Users.objects.get(user_name=user_name, password=password)
    except Users.DoesNotExist:
        user = None

    return user


class Players(models.Model):
    nick_name = models.CharField(max_length=40)
    rating = models.FloatField(default=1000)
    win_count = models.IntegerField(default=0)
    loose_count = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    special = models.CharField(max_length=255, null=True)
    spells_names = models.CharField(max_length=1000, null=True)
    battle_spells = models.CharField(max_length=1000, null=True)
    spell_to_cast = models.CharField(max_length=100, null=True)
    current_mp = models.IntegerField(default=0)
    _skills = models.CharField(max_length=255, null=True)
    _attributes = models.CharField(
        max_length=255,
        default=json.dumps({
            'Attack': 0, 'Defence': 0,
            'Spell Power': 0, 'Knowledge': 0
        })
    )

    def make_battle_spells(self, spells):
        player_spells = self.spells
        player_skills = self.skills
        battle_spells = dict()
        for spell_id, spell in spells.items():
            spell_school, spell_name = re.split(r'_', spell_id, maxsplit=1)
            if spell_name in player_spells:
                school_skill_name = '{} Magic'.format(spell_school)
                school_skill_value = 'general'
                if school_skill_name in player_skills:
                    school_skill_value = player_skills[school_skill_name]

                spell_power = self.spell_power
                if isinstance(spell.formula, dict):
                    spell_formula = spell.formula[school_skill_value]
                else:
                    spell_formula = spell.formula

                if isinstance(spell.radius, dict):
                    spell_radius = spell.radius[school_skill_value]
                else:
                    spell_radius = spell.radius

                if spell.effect:
                    effect = spell.effect[school_skill_value]
                    duration = eval(spell_formula)
                    damage = 0
                    description = 'Cast {}, {} {} spell, for {} rounds'.format(
                        effect['name'], spell_school,
                        effect['type'], duration
                    )
                else:
                    damage = eval(spell_formula)
                    effect = None
                    duration = 0
                    description = 'Making {} damage of {}'.format(
                        damage, spell_school)

                if spell_radius == 0:
                    description += ' to unit'
                elif spell_radius == 100:
                    description += ' to all units'
                else:
                    description += ' in radius {}'.format(spell_radius)

                spell_cost = spell.cost[school_skill_value]

                attributes = {
                    'name': spell.name,
                    'school': spell.school,
                    'level': spell.level,
                    'effect': effect,
                    'radius': spell_radius,
                    'cost': spell_cost,
                    'damage': damage,
                    'duration': duration,
                    'description': description
                }

                battle_spells[spell.name] = BattleSpell(attributes)

        return battle_spells

    def cast_spell(self, spell, units, click_coordinates):
        self.spell_to_cast = None

        if spell.cost > self.current_mp:
            return

        self.current_mp -= spell.cost

        self.save()

        aoe_cells = [click_coordinates]
        current_step_coordinates = aoe_cells

        if spell.radius != 100:
            for step in range(0, spell.radius):
                closest_cells_coordinates = set()
                for coordinates in current_step_coordinates:
                    closest_cells_coordinates = closest_cells_coordinates.union(
                        get_nearby_cells(coordinates))

                for coordinates in closest_cells_coordinates:
                    if coordinates in aoe_cells:
                        continue
                    if coordinates in current_step_coordinates:
                        continue

                    current_step_coordinates.append(coordinates)

                aoe_cells += current_step_coordinates

            units_take_spell = list()
            for unit in units.values():
                for unit_coordinates in unit.coordinates:
                    if unit_coordinates in aoe_cells:
                        units_take_spell.append(unit)
                        break

        else:
            units_take_spell = units.values()

        for unit in units_take_spell:
            unit.take_spell(spell)

    @property
    def attributes(self):
        return json.loads(self._attributes)

    @property
    def skills(self):
        if self._skills:
            return json.loads(self._skills)
        else:
            return dict()

    @property
    def attack(self):
        return self.attributes['Attack']

    @property
    def defence(self):
        return self.attributes['Defence']

    @property
    def knowledge(self):
        return self.attributes['Knowledge']

    @property
    def spell_power(self):
        return self.attributes['Spell Power']

    @property
    def luck(self):
        luck = 0
        if 'Luck' in self.skills.keys():
            luck_skill_value = self.skills['Luck']
            if luck_skill_value == 'bas':
                luck = 1
            elif luck_skill_value == 'adv':
                luck = 2
            elif luck_skill_value == 'exp':
                luck = 3
            else:
                raise ValueError('Invalid Luck skill value: {}'.format(
                    luck_skill_value))

        return luck

    @property
    def morale(self):
        guest_morale = 1
        if 'Leadership' in self.skills.keys():
            leadership_skill_value = self.skills['Leadership']
            if leadership_skill_value == 'bas':
                add_morale = 1
            elif leadership_skill_value == 'adv':
                add_morale = 2
            elif leadership_skill_value == 'exp':
                add_morale = 3
            else:
                raise ValueError('Invalid Leadership skill value: {}'.format(
                    leadership_skill_value))

            guest_morale += add_morale

        return guest_morale

    @property
    def info(self):
        return {
            'nick name': self.nick_name,
            'special': self.special,
            'rating': self.rating,
            'win count': self.win_count,
            'loose count': self.loose_count,
            'level': self.level,
            'experience': self.experience,
            'attack': self.attack,
            'defence': self.defence,
            'spell power': self.spell_power,
            'knowledge': self.knowledge,
            'skills': ', '.join(self.skills.keys()),
        }

    @property
    def spells(self):
        if self.spells_names:
            return self.spells_names.split(',')

        return []

    @property
    def maximum_mp(self):
        return self.knowledge * 10

import random

from heroes_core.Effects import negative, positive
from heroes_core.Resource import Resource
from heroes_core.Specials import (
    after_attack_specials, attacks_casts, attacks_specials, physical_damage,
    round_specials, spells_specials, targets_specials
)
from heroes_core.Specials import attacks_ranged
from heroes_core.helper_methods import (
    coordinates_to_abs, get_attacker_cell, range_damage, get_special_methods,
    get_nearby_cells
)
from heroes_core.TMP_some_constants import (
    DAMAGE, DEFENCE_ADD, ATTACK_ADD, DEFENCE_MULT, TARGETS_ADD, HEALTH_MULT,
    DAMAGE_MULT, SPEED_MULT, SPEED_ADD, BATTLE_START_CELLS, GUEST, CREATOR,
    RESOURCES, SORTING_PARAMETER, UNIT, LOG_MESSAGE, MOVE_UNIT
)


class Heroes3Unit(Resource):
    """
    Base unit resource class
    using to define all "abstract" units
    units should be defined right before battle, using player stats
    """

    # redefine sorting parameter name for unit resources
    sorting_parameter_name = RESOURCES[SORTING_PARAMETER][UNIT]


class BattleUnit(object):
    def __init__(
            self, heroes3_unit=None, player=None, unit_number=None, role=None,
            growth=None, attributes=None
    ):
        # initialize unit by using dict
        if attributes:
            for key, value in attributes.items():
                self.__dict__[key] = value
            return

        self.role = role
        self.player_pk = player.pk
        # 1 - unit will turn in this round
        # 2 - unit turn now
        # 3 - brave unit! move twice this round
        self.turn = 1
        self.unit_number = unit_number
        self.effects = {}
        self.resistance = 5
        self.attack_skill = heroes3_unit.attack_skill + player.attack
        self.defense_skill = heroes3_unit.defense_skill + player.defence
        self.minimum_damage = heroes3_unit.minimum_damage
        self.maximum_damage = heroes3_unit.maximum_damage
        self.health_max = heroes3_unit.health
        self._health_left = heroes3_unit.health
        self.stack = heroes3_unit.growth * growth
        self.stack_max = heroes3_unit.growth * growth
        self.luck = player.luck
        self.morale = 1 + player.morale
        self.special = heroes3_unit.special
        self.speed = heroes3_unit.speed
        self.name = heroes3_unit.name
        self.castle = heroes3_unit.castle
        self.retaliation = self.get_retaliation()
        self.cell_coordinates = self.calculate_cell_coordinates()
        self.absolute_coordinates = self.calculate_absolute_coordinates()
        self.picture = 'pictures/units/{}/{}_{}.png'.format(
            heroes3_unit.castle, heroes3_unit.name,
            BATTLE_START_CELLS['start_side'][role]
        )

    def move(self, coords, units):
        new_coordinates = [coords]
        if 'big' in self.special:
            if self.role == GUEST:
                new_coordinates.append((coords[0] - 1, coords[1]))
            else:
                new_coordinates.append((coords[0] + 1, coords[1]))

            for coordinates in new_coordinates:
                if coordinates[0] > 14:
                    new_coordinates[0] = (
                        new_coordinates[0][0] - 1, new_coordinates[0][1])
                    new_coordinates[1] = (
                        new_coordinates[1][0] - 1, new_coordinates[1][1])
                elif coordinates[0] < 0:
                    new_coordinates[0] = (
                        new_coordinates[0][0] + 1, new_coordinates[0][1])
                    new_coordinates[1] = (
                        new_coordinates[1][0] + 1, new_coordinates[1][1])

        for unit in units.values():
            if unit == self:
                continue

            for coordinates in new_coordinates:
                if coordinates in unit.coordinates:
                    if self.role == GUEST:
                        new_coordinates[0] = (
                            new_coordinates[0][0] + 1, new_coordinates[0][1])
                        new_coordinates[1] = (
                            new_coordinates[1][0] + 1, new_coordinates[1][1])
                    else:
                        new_coordinates[0] = (
                            new_coordinates[0][0] - 1, new_coordinates[0][1])
                        new_coordinates[1] = (
                            new_coordinates[1][0] - 1, new_coordinates[1][1])

        coords = sorted(new_coordinates)[0]
        self.cell_coordinates = new_coordinates[0]
        self.absolute_coordinates = coordinates_to_abs(coords, 60, 100)

    def attack(
            self, target_unit, units, attack_cell=None, counter_attack=False
    ):
        # save attacker coordinates before move
        old_coordinates = self.coordinates[0]
        # make list of targets to attack
        target_list = self.make_targets_list(target_unit, units)
        log_message = str()
        # attack each target in list
        for target in target_list:
            log_message += self.attack_calculations(target, units, attack_cell)

        # decrease unit turns left (in this round)
        self.make_turn()

        # is it ranged attack or ranged unit hit in melee radius
        range_damage_coefficient = 0
        if 'ranged' in self.special:
            range_damage_coefficient = range_damage(
                self.cell_coordinates, target_unit.cell_coordinates)

        # target unit DO NOT MAKE counter attack if
        # this attack is counter attack or
        # target cant counter attack or
        # this attack is ranged attack or
        # attacker cancel retaliation
        if not (
            counter_attack or
            target_unit.retaliation == 0 or
            range_damage_coefficient or
            'no_enemy_retaliation' in self.special
        ):
            target_unit.retaliation -= 1
            log_message += target_unit.attack(
                self, units, counter_attack=True)

        # go back after attack (like Harpy Hag)
        if 'strike_and_return' in self.special:
            return self.move(old_coordinates, units)

        return log_message

    def make_targets_list(self, target, units):
        targets_list = [target]

        for method in self.targets_specials:
            additional_targets = method(
                self, target, units
            ).get(TARGETS_ADD, None)
            if additional_targets:
                for target in additional_targets:
                    targets_list.append(target)

        return targets_list

    def attack_calculations(self, target_unit, units, attack_cell):
        # calculate base damage and init log
        damage, full_attack_log = self.physical_damage_to_target(target_unit)

        # specials physical damage and log
        special_physical_log = str()
        damage_mult = 1
        for method in self.attack_specials:
            method_results_dict = method(self, target_unit)
            special_physical_log += method_results_dict.get(LOG_MESSAGE, '')

            method_damage_mult = method_results_dict.get(DAMAGE_MULT, None)
            if method_damage_mult:
                damage_mult *= method_damage_mult

        full_attack_log += special_physical_log

        # ranged attack and log
        ranged_log = str()
        move_unit_flag = True
        for method in self.attack_ranged:
            method_results_dict = method(self, target_unit, units)
            ranged_log += method_results_dict.get(LOG_MESSAGE, '')

            method_damage_mult = method_results_dict.get(DAMAGE_MULT, None)
            if method_damage_mult:
                damage_mult *= method_damage_mult

            if not method_results_dict.get(MOVE_UNIT, True):
                move_unit_flag = False

        full_attack_log += ranged_log

        # move unit to attack cell after basic damage calculations
        if move_unit_flag and attack_cell:
            self.move(attack_cell, units)

        # attack casts and log
        attack_casts_log = str()
        for method in self.attack_casts:
            attack_casts_log += method(self, target_unit).get(LOG_MESSAGE, '')

        full_attack_log += attack_casts_log

        # x0.5, x1, x2 damage depends on luck and log
        TMP_self_luck = self.TMP_lucky(units)
        luck_state = str()
        if TMP_self_luck == 0.5:
            luck_state = ' unlucky'
        elif TMP_self_luck == 2:
            luck_state = ' lucky'

        # finalize damage value and log
        damage = int(TMP_self_luck * damage * damage_mult)
        damage_log = '{}{}, make {} damage\n'.format(
            self.name, luck_state, damage)
        damage_log += target_unit.take_damage(damage)

        full_attack_log += damage_log

        # attacker after attack specials
        after_attack_log = str()
        for method in self.after_attack_specials:
            after_attack_log += method(damage, self).get(LOG_MESSAGE, '')

        # defender after attack specials
        for method in target_unit.after_attack_specials:
            after_attack_log += method(damage, self).get(LOG_MESSAGE, '')

        # after attack log
        full_attack_log += after_attack_log

        # check target unit dead
        if target_unit.stack == 0 and target_unit.health_left == 0:
            target_unit_key = '{}_{}'.format(
                target_unit.name, target_unit.role)
            if target_unit_key in units.keys():
                del units[target_unit_key]

        return full_attack_log

    def make_turn(self):
        if self.turn == 3:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 0

    def physical_damage_to_target(self, target_unit):
        damage = random.randint(self.minimum_damage, self.maximum_damage)
        attack_add = 0
        target_defence_add = 0
        target_defence_mult = 1
        damage_mult = 1

        physical_damage_log = str()
        for method in self.special_physical_damage:
            method_modifiers = method(self, target_unit)
            physical_damage_log += method_modifiers.get(LOG_MESSAGE, '')

            tmp_target_defence_mult = method_modifiers.get(DEFENCE_MULT, None)
            if tmp_target_defence_mult:
                target_defence_mult *= tmp_target_defence_mult

            tmp_damage_mult = method_modifiers.get(DAMAGE_MULT, None)
            if tmp_damage_mult:
                damage_mult *= tmp_damage_mult

        for method in self.negative_effects:
            modifiers = method(self)

            tmp_attack_add = modifiers.get(ATTACK_ADD, None)
            if tmp_attack_add:
                attack_add += tmp_attack_add

            tmp_damage = modifiers.get(DAMAGE, None)
            if tmp_damage:
                damage = tmp_damage

        for method in target_unit.negative_effects:
            tmp_target_defence_add = method(target_unit).get(DEFENCE_ADD, None)
            if tmp_target_defence_add:
                target_defence_add += tmp_target_defence_add

        attacker_attack_skill = self.attack_skill + attack_add
        target_defence_skill = target_unit.defense_skill + target_defence_add
        target_defence_skill *= target_defence_mult
        delta_skill = attacker_attack_skill - target_defence_skill
        if delta_skill > 0:
            damage_coefficient = 1 + delta_skill * 0.05
            if damage_coefficient > 4:
                damage_coefficient = 4
        elif delta_skill < 0:
            damage_coefficient = 1 - delta_skill * 0.02
            if damage_coefficient < 0.7:
                damage_coefficient = 0.7
        else:
            damage_coefficient = 1

        total_damage = int(
            damage * self.stack * damage_coefficient * damage_mult)

        return total_damage, physical_damage_log

    def get_retaliation(self):
        retaliation = 1
        if 'unlimited_retaliations' in self.special:
            retaliation = 100

        return retaliation

    def calculate_cell_coordinates(self):
        x = BATTLE_START_CELLS['initial_cell'][self.role]
        if 'big' in self.special:
            x = BATTLE_START_CELLS['big_initial_cell'][self.role]

        return x, self.unit_number

    def calculate_absolute_coordinates(self):
        return coordinates_to_abs(sorted(self.coordinates)[0], 60, 100)

    def calculate_move_cells(self, forbidden_cells):
        coordinates_to_check = self.coordinates
        move_cells = dict()

        for coordinates in coordinates_to_check:
            move_cells[coordinates] = 'green'

        # unit bounded
        if 'bounded' in self.effects.keys():
            return move_cells

        for step in range(0, self.speed):
            closest_cells_coordinates = set()
            current_step_coordinates = dict()
            for coordinates in coordinates_to_check:
                closest_cells_coordinates = closest_cells_coordinates.union(
                    get_nearby_cells(coordinates))

            for coordinates in closest_cells_coordinates:
                if coordinates in move_cells.keys():
                    continue
                if coordinates in coordinates_to_check:
                    continue
                if coordinates in current_step_coordinates.keys():
                    continue
                if coordinates in forbidden_cells and 'flying' not in self.special:
                    continue

                current_step_coordinates[coordinates] = 'gray'

            if 'big' in self.special:
                all_current_step_coordinates = list(
                    current_step_coordinates.keys())
                all_coordinates = all_current_step_coordinates + list(
                    move_cells.keys())
                for coordinates in all_current_step_coordinates:
                    x = coordinates[0]
                    y = coordinates[1]
                    if (x + 1, y) in all_coordinates or (
                        x - 1, y) in all_coordinates:
                        continue
                    else:
                        del current_step_coordinates[coordinates]

            move_cells.update(current_step_coordinates)
            coordinates_to_check = list(current_step_coordinates.keys())

        if 'flying' in self.special:
            all_possible_coordinates = list(move_cells.keys())
            for coordinates in all_possible_coordinates:
                if coordinates in forbidden_cells and move_cells[
                    coordinates] != 'green':
                    del move_cells[coordinates]

        if 'flying' in self.special and 'big' in self.special:
            all_possible_coordinates = list(move_cells.keys())
            for coordinates in all_possible_coordinates:
                x = coordinates[0]
                y = coordinates[1]
                if (x + 1, y) not in all_possible_coordinates and (
                    x - 1, y) not in all_possible_coordinates:
                    del move_cells[coordinates]

        return move_cells

    def calculate_attack_cells(self, coordinates_of_move_cells, units):
        to_update_dict = dict()
        for unit in units.values():
            if unit.role == self.role:
                continue

            unit_coordinates = unit.coordinates
            closest_cells_coordinates = set()
            for coordinates in unit_coordinates:
                closest_cells_coordinates = closest_cells_coordinates.union(
                    get_nearby_cells(coordinates))

            TMP_TMP = set(coordinates_of_move_cells.keys())

            if closest_cells_coordinates.intersection(TMP_TMP):
                for coordinates in unit_coordinates:
                    to_update_dict[coordinates] = 'red'

        coordinates_of_move_cells.update(to_update_dict)

    def decrease_effects_duration(self):
        effects_names = list(self.effects.keys())
        for effect_name in effects_names:
            self.effects[effect_name]['duration'] -= 1
            # effect ended
            if self.effects[effect_name]['duration'] == 0:
                self.dispel_effect(effect_name)

    def dispel_effect(self, effect_name):
        del self.effects[effect_name]

    @classmethod
    def get_unit_to_move(cls, units):
        max_speed = -1
        now_turn_unit = None
        for unit in units.values():
            speed_add = 0
            speed_mult = 1
            for method in unit.negative_effects:
                tmp_unit_speed_mult = method(unit).get(SPEED_MULT, 0)
                tmp_unit_speed_add = method(unit).get(SPEED_ADD, 0)
                if tmp_unit_speed_mult:
                    speed_mult *= tmp_unit_speed_mult
                if tmp_unit_speed_add:
                    speed_add += tmp_unit_speed_add

            unit_speed = unit.speed * speed_mult + speed_add
            if (unit.turn != 0) and (unit_speed > max_speed):
                max_speed = unit_speed
                now_turn_unit = unit

        if not now_turn_unit:
            return None

        unit_brave = now_turn_unit.TMP_brave(units)
        if unit_brave < 0:
            now_turn_unit.turn = 0
            cls.get_unit_to_move(units)

        elif unit_brave > 0:
            now_turn_unit.turn = 3
        else:
            now_turn_unit.turn = 2

        return now_turn_unit

    @classmethod
    def to_json(cls, units):
        units_dict = dict()
        for key, battle_unit in units.items():
            units_dict[key] = battle_unit.__dict__

        return units_dict

    @classmethod
    def from_json(cls, units_dict):
        units = dict()
        for key, value in units_dict.items():
            units[key] = BattleUnit(attributes=value)

        return units

    def TMP_brave(self, units):
        # undead havent morale
        if 'undead' in self.special:
            return 0

        add_morale = 0
        koeff = 0

        for unit in units.values():
            # -1 morale ghost dragon
            if 'bad_enemy_morale' in unit.special and unit.role != self.role:
                add_morale -= 1

        unit_morale = (int(self.morale) + add_morale)

        # morale never below 1
        if ('high_morale' in self.special) and (unit_morale < 1):
            unit_morale = 1

        if random.randint(1, 100) <= (4.15 * abs(unit_morale)):
            koeff = int(abs(unit_morale) / unit_morale)

        return koeff

    def TMP_lucky(self, units):
        add_luck = 0
        koeff = 1

        for unit in units.values():
            # -1 luck arch devil
            if 'bad_enemy_luck' in unit.special and unit.role != self.role:
                add_luck -= 1

        attacker_luck = 4.15 * (self.luck + add_luck)
        if random.randint(1, 100) <= abs(attacker_luck):
            koeff = 1.0 * (2.0 ** (abs(attacker_luck) / attacker_luck))

        return koeff

    def maybe_attack_other_unit(self, coords, vectors, units, possible_cells):
        if vectors[0] == 0 and vectors[1] == 0:
            return None, None

        for unit in units.values():
            if coords in unit.coordinates:
                # cant attack friendly unit
                if unit.role == self.role:
                    return None, None

                attacker_cell = get_attacker_cell(coords, vectors)

                # ranged attack
                if 'ranged' in self.special:
                    return attacker_cell, unit

                # melee attack
                if attacker_cell in possible_cells:
                    return attacker_cell, unit

        return None, None

    def take_damage(self, damage):
        total_health_left = self.health_total - damage

        if total_health_left <= 0:
            self.stack = 0
            self._health_left = 0

            return '{} dead now\n'.format(self.name)

        full_stack_left = int(total_health_left / self.health)
        health_left = int(total_health_left - full_stack_left * self.health)

        if health_left > 0:
            full_stack_left += 1

        log_message = '{} take {} damage, {} units lost\n'.format(
            self.name, damage, self.stack - full_stack_left)

        self.stack = full_stack_left
        self._health_left = health_left

        return log_message

    def take_restoration(self, heal_amount):
        total_health = self.health_total
        total_health += heal_amount
        healed_unit_stack = int(total_health / self.health) + 1
        unit_health_left = total_health - (healed_unit_stack - 1) * self.health

        if healed_unit_stack > self.stack_max:
            healed_unit_stack = self.stack_max
            unit_health_left = self.health

        if unit_health_left > self.health:
            unit_health_left = self.health

        log_message = '{} restore {} health, {} units resurrected\n'.format(
            self.name, heal_amount, healed_unit_stack-self.stack)

        self.stack = healed_unit_stack
        self._health_left = unit_health_left

        return log_message

    def take_heal(self, heal_amount):
        new_health_left = self.health_left + heal_amount
        if new_health_left > self.health:
            new_health_left = self.health

        log_message = '{} take {} heal points\n'.format(
            self.name, new_health_left - self._health_left)
        self._health_left = new_health_left

        return log_message

    def take_spell(self, spell):
        damage_multiplier = 1
        log_message = str()
        for method in self.spells_specials:
            modifiers = method(spell)
            damage_multiplier *= modifiers.get(DAMAGE_MULT, 1)
            spell_log_message = modifiers.get(LOG_MESSAGE, None)
            if spell_log_message:
                log_message += '{} {}\n'.format(self.name, spell_log_message)

        # spell does not effect or damage unit
        if damage_multiplier == 0:
            return log_message

        # unit resist spell
        if random.randint(1, 100) <= int(self.resistance):
            return '{} resists {}\n'.format(self.name, spell.name)

        # unit take spell effect
        if spell.effect:
            log_message = self.take_effect(spell.effect)

        # unit take spell damage
        if getattr(spell, 'damage', 0):
            log_message += self.take_damage(spell.damage * damage_multiplier)

        return log_message

    def take_effect(self, effect):
        self.effects[effect['name']] = {
            'type': effect['type'],
            'duration': effect['duration']
        }

        return '{} take {}\n'.format(self.name, effect['name'])

    @property
    def health_total(self):
        return (self.stack - 1) * self.health + self.health_left

    @property
    def health(self):
        health_multiplier = 1
        for method in self.negative_effects:
            tmp_multiplier = method(self).get(HEALTH_MULT, None)
            if tmp_multiplier:
                health_multiplier *= tmp_multiplier

        return self.health_max * health_multiplier

    @property
    def health_left(self):
        health_multiplier = 1
        for method in self.negative_effects:
            tmp_multiplier = method(self).get(HEALTH_MULT, None)
            if tmp_multiplier:
                health_multiplier *= tmp_multiplier

        return self._health_left * health_multiplier

    @property
    def coordinates(self):
        unit_coordinates = [tuple(self.cell_coordinates), ]
        if 'big' in self.special:
            if self.role == CREATOR:
                unit_coordinates.append(
                    (self.cell_coordinates[0] + 1, self.cell_coordinates[1]))
            else:
                unit_coordinates.append(
                    (self.cell_coordinates[0] - 1, self.cell_coordinates[1]))

        return unit_coordinates

    @property
    def special_physical_damage(self):
        return get_special_methods(physical_damage, self.special)

    @property
    def attack_specials(self):
        return get_special_methods(attacks_specials, self.special)

    @property
    def attack_ranged(self):
        return get_special_methods(attacks_ranged, self.special)

    @property
    def attack_casts(self):
        return get_special_methods(attacks_casts, self.special)

    @property
    def round_specials(self):
        return get_special_methods(round_specials, self.special)

    @property
    def after_attack_specials(self):
        return get_special_methods(after_attack_specials, self.special)

    @property
    def targets_specials(self):
        return get_special_methods(targets_specials, self.special)

    @property
    def spells_specials(self):
        return get_special_methods(spells_specials, self.special)

    @property
    def positive_effects(self):
        return get_special_methods(positive, self.effects)

    @property
    def negative_effects(self):
        return get_special_methods(negative, self.effects)


ALL_UNITS = Heroes3Unit.load_resources()


def get_all_from_castle(castle_name):
    castle_units = list()

    for unit_key, unit in ALL_UNITS.items():
        if castle_name in unit_key:
            castle_units.append(unit)

    return castle_units


def add_units_to_battle(battle, role):
    player = getattr(battle, role)
    castle_name = getattr(battle, '{}_castle'.format(role))
    castle_units = get_all_from_castle(castle_name)

    units_prepared_for_battle = dict()
    for unit_number, unit in enumerate(castle_units):
        unit_to_append = BattleUnit(
            unit, player, unit_number, role, battle.growth)
        units_prepared_for_battle[
            '{}_{}'.format(unit.name, role)] = unit_to_append

    battle.add_units(units_prepared_for_battle)


def get_shaded_cells(units, unit_to_move):
    forbidden_cells = list()
    for unit in units.values():
        forbidden_cells += unit.coordinates

    coordinates_of_shaded_cells = unit_to_move.calculate_move_cells(
        forbidden_cells)
    unit_to_move.calculate_attack_cells(coordinates_of_shaded_cells, units)

    abs_coordinates_of_shaded_cells = list()
    for coordinates, color in coordinates_of_shaded_cells.items():
        coords = coordinates_to_abs(coordinates, 76, 64)
        abs_coordinates_of_shaded_cells.append(
            {'x': coords[0], 'y': coords[1], 'color': color})

    return abs_coordinates_of_shaded_cells, coordinates_of_shaded_cells

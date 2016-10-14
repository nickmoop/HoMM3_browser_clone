import random

def rangeDamageKoeff(attacker_coords, target_coords):#MAKE ME CORRECT!!!!!
    distance = int(pointsDistance(attacker_coords, target_coords))
#    distance = int(((attacker_coords[0] - target_coords[0]) ** 2 + (attacker_coords[1] - target_coords[1]) ** 2) ** (0.5))

    if distance == 1:
        koeff = False
    elif distance >= 10:
        koeff = 0.5
    else:
        koeff = 1

    return koeff

def possibleCellsForNotFlying(possible_cells, unit_coords, unit_speed):
    tmp = [unit_coords]
    to_return = [unit_coords]

    for i in range(0, unit_speed):
        cells_to_add = []
        for coords in tmp:
            current_cells = nearestCells(coords)

            for cell in list(current_cells):
                if (cell in possible_cells) and not (cell in cells_to_add) and not (cell in to_return):
                    cells_to_add.append(cell)

        to_return += cells_to_add

        tmp = cells_to_add

    return to_return
#    to_return = sorted(to_return)
#    return to_retur

def nearestCells(cell_coords):
    cells = []
    x = cell_coords[0]
    y = cell_coords[1]

    cells.append([x - 1, y])
    cells.append([x + 1, y])

    if (y % 2 == 0):
        add_x = 1

    if (y % 2 == 1):
        add_x = -1

    cells.append([x, y - 1])
    cells.append([x + add_x, y - 1])
    cells.append([x, y + 1])
    cells.append([x + add_x, y + 1])

    for coords in list(cells):
        if coords[0] < 0 or coords[0] > 14 or coords[1] < 0 or coords[1] > 10:
            cells.remove(coords)

    return cells

def trySpell(spell, spell_owner, coords, units):
    spell = eval(spell)
    not_spell_owner_add_mp = 0
    spell_owner_add_mp = -int(spell['cost'])
    log_message = '$$$$$'
#   SPECIALS

    for unit in units:

#   mana_channel 20% of spell cost
        if ('_18_' in unit['special']) and (unit['owner'] != spell_owner):
            not_spell_owner_add_mp = int(0.2 * int(spell['cost']))

#   -2 to spell cost
        if ('_41_' in unit['special']) and (unit['owner'] == spell_owner):
            spell_owner_add_mp = spell_owner_add_mp + 2

#   SPECIALS

    if spell['cells'] == 'all':
        for unit in units:
            units.remove(unit)
            TMP = castSpell(spell, unit)
            unit = TMP[0]
            log_message = log_message + TMP[1] + '$$$$$'
            units.append(unit)

    if spell['cells'] == 'all_enemy':
        for unit in units:

            if unit['owner'] == spell_owner:
                continue

            units.remove(unit)
            TMP = castSpell(spell, unit)
            unit = TMP[0]
            log_message = log_message + TMP[1] + '$$$$$'
            units.append(unit)

    if spell['cells'] == 'all_allied':
        for unit in units:

            if unit['owner'] != spell_owner:
                continue

            units.remove(unit)
            TMP = castSpell(spell, unit)
            unit = TMP[0]
            log_message = log_message + TMP[1] + '$$$$$'
            units.append(unit)

    if 'target' in spell['cells']:
        for unit in units:
            unit_coords = [int(unit['x']), int(unit['y'])]

            if unit_coords == coords:
                units.remove(unit)
                TMP = castSpell(spell, unit)
                unit = TMP[0]
                log_message = log_message + TMP[1] + '$$$$$'
                units.append(unit)
                break

            if '_3_' in unit['special']:

                if unit['owner'] == 'guest':
                    unit_coords = [unit_coords[0] - 1, unit_coords[1]]
                if unit['owner'] == 'creator':
                    unit_coords = [unit_coords[0] + 1, unit_coords[1]]

                if unit_coords == coords:
                    units.remove(unit)
                    TMP = castSpell(spell, unit)
                    unit = TMP[0]
                    log_message = log_message + TMP[1] + '$$$$$'
                    units.append(unit)
                    break

    return [units, spell_owner_add_mp, not_spell_owner_add_mp, log_message]

def castSpell(spell, unit):

#   black dragon special
    if ('_10_' in unit['special']) and (int(spell['level']) <= 5):
        log_message = unit['name'] + ' resist all spells 1-5 levels'
        return [unit, log_message]

#   gold dragon special
    if ('_48_' in unit['special']) and (int(spell['level']) <= 4):
        log_message = unit['name'] + ' resist all spells 1-4 levels'
        return [unit, log_message]

    if str(spell['effect']) != '0':

        if random.randint(1, 100) <= int(unit['resistance']):
            log_message = unit['name'] + ' resisted ' + spell['name']
            return [unit, log_message]

        unit['effects'] = refreshEffect(unit, spell['effect'])['effects']
        log_message = spell['name'] + ' make effect on ' + unit['name']

    if str(spell['damage']) != '0':
        damage = int(spell['damage'])
        if damage > 0:

            if random.randint(1, 100) <= int(unit['resistance']):
                log_message = unit['name'] + ' resisted ' + spell['name']
                return [unit, log_message]

#   iron golem special
            if '_40_' in unit['special']:
                damage = int(0.25 * damage)

            TMP = targetUnitsLeft(damage, unit)
            unit['stack'] = TMP[0]
            unit['health_left'] = TMP[1]
            log_message = spell['name'] + ' make ' + str(damage) + ' damage on ' + unit['name']
        if damage < 0:
            unit = healTarget(unit, abs(damage))
            log_message = spell['name'] + ' heal ' + str(abs(damage)) + ' health on ' + unit['name']

    return [unit, log_message]

def maybeSpell(guest_spell, creator_spell):

    if (str(guest_spell) != '0') and (str(guest_spell) != '1'):
        return [guest_spell, 'guest']

    if (str(creator_spell) != '0') and (str(creator_spell) != '1'):
        return [creator_spell, 'creator']

    return False

def damageTarget(units, unit_to_damage, damage_amount):
    for unit in units:
        if unit['name'] == unit_to_damage['name'] and unit['owner'] == unit_to_damage['owner']:
            all_health = (int(unit['stack']) - 1) * int(unit['health']) + int(unit['health_left'])
            all_health = all_health - damage_amount

            if all_health <= 0:
                units.remove(unit)
                return units

            unit_stack = int(all_health / int(unit['health'])) + 1
            unit_health_left = all_health - ((unit_stack - 1) * int(unit['health']))
            unit['health_left'] = unit_health_left
            unit['stack'] = unit_stack
            if unit_health_left == 0:
                unit['stack'] = unit_stack - 1
                unit['health_left'] = int(unit['health'])
            break

    return units

def healTarget(unit_to_heal, heal_amount):#  MAKE ME!!   OVERHEAL CASE!!!
    all_health = (int(unit['stack']) - 1) * int(unit['health']) + int(unit['health_left'])
    all_health = all_health + heal_amount
    unit_stack = int(all_health / int(unit['health'])) + 1
    unit_health_left = all_health - ((unit_stack - 1) * int(unit['health']))
    unit['stack'] = unit_stack
    unit['health_left'] = unit_health_left
    return unit

def luck(attacker, units):
    add_luck = 0
    koeff = 1

    for unit in units:

#   -1 luck arch devil
        if '_24_' in unit['special'] and unit['owner'] != attacker['owner']:
            add_luck = add_luck - 1

    attacker_luck = 4.15 * (int(attacker['luck']) + add_luck)
    if random.randint(1, 100) <= abs(attacker_luck):
        koeff = 1.0 * (2.0 ** (abs(attacker_luck) / attacker_luck))
    
    return koeff

def targetUnitsLeft(damage, target_unit):
    health = int(target_unit['health'])
############################
#   EFFECTS BLOCK!!!
#   age -50% max hp
    if '_neg.4(' in target_unit['effects']:
        health = (health * 0.5)

#   poison -25% max hp each turn (10 turns)
    if '_neg.6(' in target_unit['effects']:
        percentage = 0.25
        turns = 1

        tmp = target_unit['effects'].split('_')
        for value in tmp:
            if 'neg.6(' in value:
                turns = 10 - int(value.split('(')[1].replace(')', ''))
                break

        health = (health * (percentage ** turns))
#   EFFECTS BLOCK!!!
############################
    target_total_health = health * (int(target_unit['stack']) - 1) + int(target_unit['health_left'])
    target_total_health_left = target_total_health - damage

    if target_total_health_left <= 0:
        return [0, 0]

    target_stack_left = int(target_total_health_left / int(target_unit['health'])) + 1
    target_health_left = int((target_stack_left * int(target_unit['health'])) - target_total_health_left)

    return [target_stack_left, target_health_left]

def currentUnitTurn(units):
    for unit in units:
        if (str(unit['turn']) == 'now'):
            return unit

def shadedCells(units):
    for unit in units:
        if (unit['turn'] == 'now'):
            unit_x = int(unit['x'])
            unit_y = int(unit['y'])
            unit_speed = int(unit['speed'])
#   root
            if '_46_' in unit['effects']:
                unit_speed = 0

            TMP_x = 0
            flying = False

            if '_3_' in unit['special']:
                if unit['owner'] == 'guest':
                    TMP_x = 1
                if unit['owner'] == 'creator':
                    TMP_x = -1

            if '_2_' in unit['special']:
                flying = True

            break

    coordinates_of_shaded_cells = []
    for y in range(0, 11):
        for x in range(0,15):
            distance = pointsDistance([int(unit['x']), int(unit['y'])], [x, y])
            if distance <= unit_speed:
                coordinates_of_shaded_cells.append([x, y])

    for unit in units:
        if unit['turn'] == 'now':
            continue

        x = int(unit['x'])
        y = int(unit['y'])
        if [x, y] in coordinates_of_shaded_cells:
            coordinates_of_shaded_cells.remove([x, y])
        if (TMP_x != 0) and ([x + TMP_x, y] in coordinates_of_shaded_cells):
            coordinates_of_shaded_cells.remove([x + TMP_x, y])

        if '_3_' in unit['special']:
            if unit['owner'] == 'guest':
                x = int(unit['x']) - 1
                y = int(unit['y'])
            if unit['owner'] == 'creator':
                x = int(unit['x']) + 1
                y = int(unit['y'])
            if [x, y] in coordinates_of_shaded_cells:
                coordinates_of_shaded_cells.remove([x, y])
            if (TMP_x != 0) and ([x + TMP_x, y] in coordinates_of_shaded_cells):
                coordinates_of_shaded_cells.remove([x + TMP_x, y])

    if not flying:
        unit_coords = [unit_x, unit_y]
        coordinates_of_shaded_cells = possibleCellsForNotFlying(coordinates_of_shaded_cells, unit_coords, unit_speed)
#        coordinates_of_shaded_cells = sorted(possibleCellsForNotFlying(coordinates_of_shaded_cells, unit_coords, unit_speed))

    abs_coordinates_of_shaded_cells = []
    for coordinates in coordinates_of_shaded_cells:
        coords = coordinatesToAbs(coordinates[0], coordinates[1], 76, 64)
        abs_coordinates_of_shaded_cells.append({'x' : coords[0], 'y' : coords[1]})
    return (abs_coordinates_of_shaded_cells, coordinates_of_shaded_cells)
#    return (TEST)

def pointsDistance(point_A, point_B):
    point_A_y = point_A[1]
    point_A_x = point_A[0]
    point_B_y = point_B[1]
    point_B_x = point_B[0]
    delta_y = int(abs(point_A_y - point_B_y))
    koeff = delta_y / 2
    koeff_B = 0
    koeff_A = 0

    if delta_y % 2 == 1:
        koeff_B = 0.5

        if point_A_y % 2 == 1:
            koeff_A = -0.5

        if point_A_y % 2 == 0:
            koeff_A = 0.5

        if (point_A_x + koeff_A) < point_B_x:
            koeff_B = -0.5

    distance = round(abs((point_A_x + koeff_A) - (point_B_x + koeff_B)) + koeff, 1)
    distance_circle = int(((point_A_x - point_B_x) ** 2 + (point_A_y - point_B_y) ** 2 ) ** 0.5)
    if distance < distance_circle:
        distance = distance_circle

    return distance

def topPlayers(players):
    all_players = []
    for player in players:
        tmp = [
            float(player.rating),
            str(player.nick_name),
            int(player.win_count),
            int(player.loose_count),
        ]
        all_players.append(tmp)

    return sorted(all_players)

def showAllHeroInfo(hero):
    tmp = [
        'name : ' + str(hero.nick_name),
        'avatar : ' + str(hero.avatar),
        'rating :' + str(hero.rating),
        'win_count : ' + str(hero.win_count),
        'loose_count : ' + str(hero.loose_count),
        'level : ' + str(hero.level),
        'experience : ' + str(hero.experience),
        'skills : ' + str(hero.skills),
        'special : ' + str(hero.special),
        'attributes : ' + str(hero.attributes),
        'spells : ' + str(hero.spells)
    ]
    return tmp

def showAllUnitsInfo(units):
    tmp = []
    for unit in units:
        message = {
            'castle': str(unit.castle),
            'name': str(unit.name),
            'attack_skill' : str(unit.attack_skill),
            'defense_skill' : str(unit.defense_skill),
            'minimum_damage' : str(unit.minimum_damage),
            'maximum_damage' : str(unit.maximum_damage),
            'health' : str(unit.health),
            'speed' : str(unit.speed),
            'growth' : str(unit.growth),
            'special' : str(unit.special)
        }
        tmp.append(message)
    return tmp

def coordinatesToRelative(x, y):
    cell_size = 42
    circle_rad = int((42 * (3 ** (1.0 / 2.0))) / 2.0)
    for x_cell in range(0, 15):
        for y_cell in range(0, 11):
            coords = coordinatesToAbs(x_cell, y_cell, 0, 20)
            dx = coords[0] - x
            dy = coords[1] - y
            dist = (dx ** 2 + dy ** 2) ** (1.0 / 2.0)
            if dist <= circle_rad:
                if dist != 0:
                    x_vector = dx / dist
                    y_vector = dy / dist
                else:
                    x_vector = 0
                    y_vector = 0
                return [x_cell, y_cell, x_vector, - y_vector]
    return False

def showAllSpellsInfo(spells):
    tmp = []
    for spell in spells:
        message = {
            'name': str(spell.name),
            'effect' : str(spell.effect),
            'damage_type' : str(spell.damage_type),
            'damage_formula' : str(spell.damage_formula),
            'description' : str(spell.description),
            'level' : str(spell.level),
            'cost' : str(spell.cost),
            'cells' : str(spell.cells),
        }
        tmp.append(message)
    return tmp

def currentTurn(units):
    max_speed = -1000
    creator_mp = 0
    guest_mp = 0
    creator_spell = 0
    guest_spell = 0

    for unit in units:

        if unit['turn'] == 'now':
            return [units, creator_mp, guest_mp, creator_spell, guest_spell]

        if (int(unit['turn']) != 0) and ((int(unit['speed']) * int(unit['turn'])) > max_speed):
            if '_neg.8(' in unit['effects']:
                continue

            max_speed = int(unit['speed'])

    for unit in units:

        if '_neg.8(' in unit['effects']:
            continue

        if (int(unit['turn']) != 0) and (int(unit['speed']) == max_speed):
            unit['turn'] = 'now'

            if morale(unit, units) < 0:
                unit['turn'] = 0
                units = currentTurn(units)[0]

            break

    if max_speed == -1000:
        for unit in units:
            unit['turn'] = 1
            unit['retaliation'] = 1
            unit['effects'] = decreaseEffectsDuration(unit)
            creator_spell = 1
            guest_spell = 1

#   wraith regen hp
            if '_28_' in unit['special']:
                unit['health_left'] = int(unit['health'])

#   wraith drain mana
            if '_29_' in unit['special']:
                if unit['owner'] == 'guest':
                    creator_mp = -2
                    guest_mp = 2
                if unit['owner'] == 'creator':
                    creator_mp = 2
                    guest_mp = -2
#   royal griffin
            if '_50_' in unit['special']:
                unit['retaliation'] = 100

        units = currentTurn(units)[0]

    return [units, creator_mp, guest_mp, creator_spell, guest_spell]

def refreshEffect(unit, effect_to_refresh):
    effects = unit['effects'].split('_')
    TMP = getEffectStats(effect_to_refresh)
    force = TMP[0]
    number = TMP[1]
    duration = TMP[2]
    if '' not in effects:
        effects_tmp = ''
        for effect in effects:
            tmp = getEffectStats(effect)

            if (tmp[0] == force) and (tmp[1] == number):
                tmp[2] = duration

            effects_tmp = effects_tmp + '_' + tmp[0] + '.' + str(tmp[1]) + '(' + str(tmp[2]) + ')_'
        unit['effects'] = effects_tmp
    else:
        unit['effects'] = '_' + force + '.' + str(number) + '(' + str(duration) + ')_'

    return unit
                

def decreaseEffectsDuration(unit):
    effects = unit['effects'].split('_')
    if effects:
        effects_tmp = ''
        for effect in effects:
            TMP = getEffectStats(effect)
            force = TMP[0]
            number = TMP[1]
            duration = TMP[2]

            if duration == 1:
                continue

            if force and number and duration:
                effects_tmp = effects_tmp + '_' + force + '.' + str(number) + '(' + str(duration - 1) + ')_'                

    return effects_tmp

def getEffectStats(effect):
    if not effect:
        return ['', '', '']
    TMP = effect.split('.')
    if len(TMP) == 2:
        force = TMP[0]
        number = int(TMP[1].split('(')[0])
        duration = int(TMP[1].split('(')[1].replace(')', ''))
    else:
        force = ''
        number = ''
        duration = ''

    return [force, number, duration]

def dispelEffect(force, number, unit_to_dispel, units):
    for unit in units:
        if unit['name'] == unit_to_dispel['name'] and unit['owner'] == unit_to_dispel['owner']:
            effects = unit['effects'].split('_')
            if effects:
                effects_tmp = ''
                for effect in effects:
                    tmp = getEffectStats(effect)
                    if (tmp[0] == force) and (tmp[1] == number):
                        continue
                    if tmp[0] and tmp[1] and tmp2[2]:
                        effects_tmp = effects_tmp + '_' + tmp[0] + '.' + str(tmp[1]) + '(' + str(tmp[2]) + ')_'
            unit['effects'] = effects_tmp
            break

    return units

def targetList(attacker, attacker_coords, target_coords, units, target):
    tmp = [target]

####    dragon breath
    if ('_12_' in attacker['special']):
        second_target_coords = secondTargetCoords(attacker_coords, target_coords)
        for unit in units:
            if (int(unit['x']) == second_target_coords[0]) and (int(unit['y']) == second_target_coords[1]):
                if unit not in tmp:
                    tmp.append(unit)
                break
            if '_3_' in unit['special']:
                if (unit['owner'] == 'guest') and ((int(unit['x']) - 1) == second_target_coords[0]) and (int(unit['y']) == second_target_coords[1]):
                    if unit not in tmp:
                        tmp.append(unit)
                    break
                if (unit['owner'] == 'creator') and ((int(unit['x']) + 1) == second_target_coords[0]) and (int(unit['y']) == second_target_coords[1]):
                    if unit not in tmp:
                        tmp.append(unit)
                    break

####    attack all nearby units
    if ('_17_' in attacker['special']):
        list_of_possible_cells = []
        list_of_possible_cells.append([attacker_coords[0], attacker_coords[1] - 1])
        list_of_possible_cells.append([attacker_coords[0], attacker_coords[1] + 1])

        if attacker_coords[1] % 2 == 1:
            list_of_possible_cells.append([attacker_coords[0] - 1, attacker_coords[1] - 1])
            list_of_possible_cells.append([attacker_coords[0] - 1, attacker_coords[1] + 1])
        if attacker_coords[1] % 2 == 0:
            list_of_possible_cells.append([attacker_coords[0] + 1, attacker_coords[1] - 1])
            list_of_possible_cells.append([attacker_coords[0] + 1, attacker_coords[1] + 1])

        if attacker['owner'] == 'guest':
            list_of_possible_cells.append([attacker_coords[0] + 1, attacker_coords[1]])
            list_of_possible_cells.append([attacker_coords[0] - 2, attacker_coords[1]])
            if attacker_coords[1] % 2 == 1:
                list_of_possible_cells.append([attacker_coords[0] - 2, attacker_coords[1] - 1])
                list_of_possible_cells.append([attacker_coords[0] - 2, attacker_coords[1] + 1])
            if attacker_coords[1] % 2 == 0:
                list_of_possible_cells.append([attacker_coords[0] - 1, attacker_coords[1] - 1])
                list_of_possible_cells.append([attacker_coords[0] - 1, attacker_coords[1] + 1])
        if attacker['owner'] == 'creator':
            list_of_possible_cells.append([attacker_coords[0] - 1, attacker_coords[1]])
            list_of_possible_cells.append([attacker_coords[0] + 2, attacker_coords[1]])
            if attacker_coords[1] % 2 == 1:
                list_of_possible_cells.append([attacker_coords[0] + 1, attacker_coords[1] - 1])
                list_of_possible_cells.append([attacker_coords[0] + 1, attacker_coords[1] + 1])
            if attacker_coords[1] % 2 == 0:
                list_of_possible_cells.append([attacker_coords[0] + 2, attacker_coords[1] - 1])
                list_of_possible_cells.append([attacker_coords[0] + 2, attacker_coords[1] + 1])

        for unit in units:

            if attacker['owner'] == unit['owner']:
                continue

            unit_coords = [int(unit['x']), int(unit['y'])]
            if unit_coords in list_of_possible_cells:
                if unit not in tmp:
                    tmp.append(unit)

            if '_3_' in unit['special']:
                if unit['owner'] == 'guest':
                    unit_coords = [unit_coords[0] - 1, unit_coords[1]]

                if unit['owner'] == 'creator':
                    unit_coords = [unit_coords[0] + 1, unit_coords[1]]

                if unit_coords in list_of_possible_cells:
                    if unit not in tmp:
                        tmp.append(unit)


####    cerber attack 3 target
    if ('_20_' in attacker['special']):
        if attacker_coords[1] != target_coords[1]:

            if (attacker_coords[0] - target_coords[0]) > 0:
                second_target_coords = [attacker_coords[0] - 1, attacker_coords[1]]
                third_target_coords = [target_coords[0] + 1, target_coords[1]]

            if (attacker_coords[0] - target_coords[0]) < 0:
                second_target_coords = [attacker_coords[0] + 1, attacker_coords[1]]
                third_target_coords = [target_coords[0] - 1, target_coords[1]]

            if (attacker_coords[0] - target_coords[0]) == 0:

                if attacker_coords[1] % 2 == 0:
                    second_target_coords = [attacker_coords[0] - 1, attacker_coords[1]]
                    third_target_coords = [target_coords[0] + 1, target_coords[1]]

                if attacker_coords[1] % 2 == 1:
                    second_target_coords = [attacker_coords[0] + 1, attacker_coords[1]]
                    third_target_coords = [target_coords[0] - 1, target_coords[1]]

        if attacker_coords[1] == target_coords[1]:

            if attacker_coords[1] % 2 == 0:
                add_x = 1

            if attacker_coords[1] % 2 == 1:
                add_x = 0

            if (attacker_coords[0] - target_coords[0]) > 0:
                second_target_coords = [target_coords[0] + add_x, attacker_coords[1] - 1]
                third_target_coords = [target_coords[0] + add_x, attacker_coords[1] + 1]

            if (attacker_coords[0] - target_coords[0]) < 0:
                second_target_coords = [target_coords[0] + add_x - 1, attacker_coords[1] - 1]
                third_target_coords = [target_coords[0] + add_x - 1, attacker_coords[1] + 1]

        list_of_possible_cells = [second_target_coords, third_target_coords]

        for unit in units:
            if attacker['owner'] == unit['owner']:
                continue

            unit_coords = [int(unit['x']), int(unit['y'])]
            if unit_coords in list_of_possible_cells:
                if unit not in tmp:
                    tmp.append(unit)

            if '_3_' in unit['special']:
                if unit['owner'] == 'guest':
                    unit_coords = [unit_coords[0] - 1, unit_coords[1]]

                if unit['owner'] == 'creator':
                    unit_coords = [unit_coords[0] + 1, unit_coords[1]]

                if unit_coords in list_of_possible_cells:
                    if unit not in tmp:
                        tmp.append(unit)

####    wolf riders and crusaders double attack
    if ('_36_' in attacker['special']):
        tmp.append(target)

####    marksman and great elfs shoot twice
    if ('_49_' in attacker['special']):
        if rangeDamageKoeff([int(attacker['x']), int(attacker['y'])], [int(target['x']), int(target['y'])]):
            tmp.append(target)

    return tmp

def secondTargetCoords(attacker_coords, target_coords):   #for breath
    if (target_coords[1] - attacker_coords[1]) == 0:
        x = target_coords[0] + (target_coords[0] - attacker_coords[0])
        y = target_coords[1]
    else:
        y = target_coords[1] + (target_coords[1] - attacker_coords[1])
        if target_coords[1] % 2 == 1:
            x = target_coords[0] + (target_coords[0] - attacker_coords[0] - 1)
        if target_coords[1] % 2 == 0:
            x = target_coords[0] + (target_coords[0] - attacker_coords[0] + 1)

    return [x, y]

def moveUnit(coords, units):
    for unit in units:
        if (str(unit['turn']) == 'now'):

#   dendroid unroot
            if '_46_' in unit['special']:
                if int(unit['x']) != coords[0] or int(unit['y']) != coords[1]:
                    for unit_TMP in units:
                        if (str(unit_TMP['turn']) == 'now'):
                            continue
                        if '_neg.3(' in unit_TMP['effects']:
                            units = dispelEffect('neg', 3, unit_TMP, units)
#   dendroid unroot

            unit['x'] = coords[0]
            unit['y'] = coords[1]

            tmp_x = coords[0]
            tmp_y = coords[1]
            size_y = 100
            if ('_3_' in unit['special']):
                size_y = 100
                if (unit['owner'] == 'guest'):
                    tmp_x = tmp_x - 1
            abs_coords = coordinatesToAbs(tmp_x, tmp_y, 60, size_y)

            unit['x_abs'] = abs_coords[0]
            unit['y_abs'] = abs_coords[1]
            unit['turn'] = 0

            if morale(unit, units) > 0:
                add_turn = 1
                unit['turn'] = 1

            unit_id = str(unit['owner']) + '_' + str(unit['name'])
            unit_abs_coords_new = {'x' : abs_coords[0], 'y' : abs_coords[1]}
            return [units, unit_id, unit_abs_coords_new]

def coordinatesToAbs(x, y, pic_size_x, pic_size_y):
    cell_size = 42
    cell_indent_x = 96
    cell_indent_y = 200
    cos_30 = ((3.0 ** (1.0 / 2.0)) / 2.0)
    sin_30 = 0.5

    if y % 2 == 0:
        add_x = 0 + cell_size * cos_30
    if y % 2 == 1:
        add_x = 0
    x = int(cell_indent_x + 2 * (cell_size * cos_30) * x - (pic_size_x / 2.0) + add_x)
    y = int(cell_indent_y + (cell_size + cell_size * sin_30) * y - (pic_size_y - 20))

    return (x, y)

def damageByFormula(formula, spell_power, magic_special):
    TMP = formula.split('*')[1]
    multiple_koeff = int(TMP.split('+')[0])
    add_koeff = int(TMP.split('+')[1])
    result = int(spell_power) * multiple_koeff + add_koeff

    if 'Sorcery' in magic_special:
        result = int(result * 1.05)

    return result

def maybeAttack(coords, vectors, units, possible_cells, attacker):
    if vectors[0] == 0 and vectors[1] == 0:
        return False

    for unit in units:
        if (int(unit['x']) == coords[0]) and (int(unit['y']) == coords[1]):
            if unit['owner'] == attacker['owner']:
                return False

            if '_1_' in attacker['special']:
                return [[int(attacker['x']), int(attacker['y'])], unit, [int(unit['x']), int(unit['y'])]]

            attacker_cells = nearbyCellByVector(coords, vectors)
            if attacker_cells in possible_cells:
                if '_6_' in attacker['special']:
                    return [[int(attacker['x']), int(attacker['y'])], unit, [int(unit['x']), int(unit['y'])]]
                return [attacker_cells, unit, [int(unit['x']), int(unit['y'])]]

        if '_3_' in unit['special']:
            if unit['owner'] == 'creator':
                x = int(unit['x']) + 1
                y = int(unit['y'])
            if unit['owner'] == 'guest':
                x = int(unit['x']) - 1
                y = int(unit['y'])
            if (x == coords[0]) and (y == coords[1]):
                if unit['owner'] == attacker['owner']:
                    return False

                if '_1_' in attacker['special']:
                    return [[int(attacker['x']), int(attacker['y'])], unit, [int(unit['x']), int(unit['y'])]]

                attacker_cells = nearbyCellByVector(coords, vectors)
                if attacker_cells in possible_cells:
                    if '_6_' in attacker['special']:
                        return [[int(attacker['x']), int(attacker['y'])], unit, [int(unit['x']), int(unit['y'])]]
                    return [attacker_cells, unit, [x, y]]
    return False

def nearbyCellByVector(coords, vectors):
    if vectors[0] > 0:
        if abs(vectors[1]) < 0.5:
            x_cell = coords[0] - 1
            y_cell = coords[1]
        else:
            x_cell = coords[0]
            if coords[1] % 2 == 1:
                x_cell = x_cell - 1
            y_cell = coords[1] + int(vectors[1] / abs(vectors[1]))

    if vectors[0] < 0:
        if abs(vectors[1]) < 0.5:
            x_cell = coords[0] + 1
            y_cell = coords[1]
        else:
            x_cell = coords[0]
            if coords[1] % 2 == 0:
                x_cell = x_cell + 1
            y_cell = coords[1] + int(vectors[1] / abs(vectors[1]))

    return [int(x_cell), int(y_cell)]

def physDamage(attacker, target_unit):
    minimum_damage = int(attacker['minimum_damage'])
    maximum_damage = int(attacker['maximum_damage'])
    damage = random.randint(minimum_damage, maximum_damage)
    stack = int(attacker['stack'])
    attack_skill = int(attacker['attack_skill'])
    defense_skill = int(target_unit['defense_skill'])
    attack_add = 0
    defense_add = 0

#   -80% armor
    if '_39_' in attacker['special']:
        defense_add = -(int(defense_skill * 0.8))

#   desease -2 Att -2 Def
    if '_neg.2(' in target_unit['effects']:
        defense_add = defense_add - 2

    if '_neg.2(' in attacker['effects']:
        attack_add = attack_add - 2

#   curse deal minimum damage
    if '_neg.5(' in attacker['effects']:
        damage = minimum_damage

#   weakness -3 Att
    if '_neg.7(' in attacker['effects']:
        attack_add = attack_add - 3

    delta_skill = int((attack_skill + attack_add) - (defense_skill + defense_add))
    add_damage_koeff = 1

    if delta_skill > 0:
        add_damage_koeff = 1 + (delta_skill * 0.05)
        if add_damage_koeff > 4:
            add_damage_koeff = 4

    if delta_skill < 0:
        add_damage_koeff = 1 - (delta_skill * 0.02)
        if add_damage_koeff < 0.7:
            add_damage_koeff = 0.7

    total_damage = int(damage * stack * add_damage_koeff)

    return total_damage

def morale(current_unit, units):

#   undead havent morale
    if '_26_' in current_unit['special']:
        return 0

    add_morale = 0
    koeff = 0

    for unit in units:

#   -1 morale ghost dragon
        if '_34_' in unit['special'] and unit['owner'] != current_unit['owner']:
            add_morale = add_morale - 1

    unit_morale = (int(current_unit['morale']) + add_morale)

#   morale never below 1 
    if ('_9_' in current_unit['special']) and (unit_morale < 1):
        unit_morale = 1

    if random.randint(1, 100) <= (4.15 * abs(unit_morale)):
        koeff = int(abs(unit_morale) / unit_morale)
    
    return koeff

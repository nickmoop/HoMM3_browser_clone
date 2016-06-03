from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext, loader, Context
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.middleware import csrf
import json
import random
import heroes.calc as calc

from heroes.forms import Login, Registration, MakeUnit, MakeBattle, MakeSpell
from heroes.models import User, Player, AuthUser, Unit, Battle, Spell

my_ip_address = '10.10.3.219'
host_name = 'http://' + my_ip_address

def changePlayer(request):
    global host_name
    token = csrf.get_token(request)

    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login/')

    pk = isLoggedIn(token)
    if request.method == 'POST' and request.is_ajax():
        
        current_player = Player.objects.filter(pk = pk).delete()

        new_player = Player(
            nick_name = str(request.POST.get('nick_name', '')),
            avatar = str(request.POST.get('avatar', '')),
            rating = float(request.POST.get('rating', '')),
            win_count = int(request.POST.get('win_count', '')),
            loose_count = int(request.POST.get('loose_count', '')),
            level = int(request.POST.get('level', '')),
            experience = int(request.POST.get('experience', '')),
            skills = str(request.POST.get('skills', '')),
            special = str(request.POST.get('special', '')),
            attributes = str(request.POST.get('attributes', '')),
            spells = str(request.POST.get('spells', '')),
        )
        new_player.pk = pk
        new_player.save()
        return(JsonResponse({'redirect_url' : host_name + '/heroes/change_player'}))
        #return(JsonResponse({'error_message' : 'ok'}))
    #else:
    #    return(JsonResponse({'error_message' : 'got trouble'}))

    all_players = Player.objects.all()
    for player in all_players:
        if int(player.pk) == int(pk):
            current_player = {
                'nick_name' : str(player.nick_name),
                'avatar' : str(player.avatar),
                'rating' : float(player.rating),
                'win_count' : int(player.win_count),
                'loose_count' : int(player.loose_count),
                'level' : int(player.level),
                'experience' : int(player.experience),
                'skills' : str(player.skills),
                'special' : str(player.special),
                'attributes' : str(player.attributes),
                'spells' : str(player.spells),
            }

    context = RequestContext(request, {'player' : current_player})
    template = loader.get_template('heroes/change_player.html')
    return HttpResponse(template.render(context))

def chooseSpell(request):
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login/')

    all_spells = Spell.objects.all()
    pk = isLoggedIn(token)
    #return(JsonResponse({'error_message' : 'i try to cast'}))
    if request.method == 'POST' and request.is_ajax():
        spells_hero = Player.objects.get(pk = isLoggedIn(token)).spells
        skills_hero = Player.objects.get(pk = isLoggedIn(token)).skills
        special_hero = Player.objects.get(pk = isLoggedIn(token)).special

        #context = RequestContext(request, {'spells' : spells, 'skills' : skills, 'special' : special})
        #template = loader.get_template('heroes/choose_spell.html')
        return(JsonResponse({'error_message' : 'i try to cast'}))
        #return HttpResponse(template.render(context))
#
    spells_hero = Player.objects.get(pk = pk).spells
    skills_hero = eval(Player.objects.get(pk = pk).skills)
    special_hero = eval(Player.objects.get(pk = pk).special)
    spell_power_hero = eval(Player.objects.get(pk = pk).attributes)['SP']

    TMP_spells = []
    magic_skills_hero = []
    magic_special_hero = 'Havent magic special'
    skills_to_show = []

    for magic in ['Air_Magic', 'Water_Magic', 'Fire_Magic', 'Earth_Magic', 'Sorcery']:
        skill_to_append = {}
        if magic != 'Sorcery':
            skill_to_append = {magic : 'bas'}
        for k, v in skills_hero.items():
            if (magic in k):
                skill_to_append = {k : v}
                skills_to_show.append({k : v})
                break
        magic_skills_hero.append(skill_to_append)

    if special_hero == 4:
        magic_special_hero = 'Sorcery (+5% spell damage)'

    for spell in all_spells:
        if spell.name in spells_hero:
            for skill in magic_skills_hero:
                for k, v in skill.items():
                    if spell.damage_type in k:

                        if spell.damage_formula == '0':
                            damage = '0'
                        else:
                            damage = str(calc.damageByFormula(eval(spell.damage_formula)[v], spell_power_hero, magic_special_hero))

                        if spell.effect == '0':
                            effect = '0'
                        else:
                            effect = eval(spell.effect)[v] + '(' +str(spell_power_hero) + ')'

                        TMP_spells.append({
                            'name':spell.name,
                            'effect':effect,
                            'cells':eval(spell.cells)[v],
                            'damage_type':spell.damage_type,
                            'damage':damage,
                            'level':spell.level,
                            'cost':spell.cost,
                            'description':spell.description,

                        })
                    break

    context = RequestContext(request, {'spells' : TMP_spells, 'skills' : skills_to_show, 'special' : magic_special_hero, 'spell_power' : spell_power_hero})
    template = loader.get_template('heroes/choose_spell.html')
    return HttpResponse(template.render(context))
#
   # return redirect(host_name + '/heroes/login/')

def battle(request):
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login/')

    current_battle = currentPlayerBattle(isLoggedIn(token))
    if current_battle:
        battle_name = current_battle.name
        units = eval(current_battle.units)
        TMP = calc.currentTurn(units)
        units = TMP[0]

        if TMP[1] == 1 and TMP[2] == 1:
            current_battle.creator_current_mp = str(int(current_battle.creator_current_mp) + TMP[1])
            current_battle.guest_current_mp = str(int(current_battle.guest_current_mp) + TMP[2])
            current_battle. save()

        if TMP[3] != 0 or TMP[4] != 0:
            current_battle.creator_spell = str(TMP[3])
            current_battle.guest_spell = str(TMP[4])
            current_battle. save()

#       YOUR TURN OR NOT??
        current_turn_owner = calc.currentUnitTurn(units)['owner']
#        if not your turn:
 #           context = RequestContext(request, {'battle_name' : battle_name, 'units' : units, 'log_message' : current_battle.log.split('$$$$$')})
 #           template = loader.get_template('heroes/battle.html')
#            return HttpResponse(template.render(context))

        shaded_cells = calc.shadedCells(units)
        abs_shaded_cells = shaded_cells[0]
        cells_shaded_cells = shaded_cells[1]

        if request.method == 'POST' and request.is_ajax():

############################################

            if request.POST.get('choosen_spell_name', ''):

                spell_to_cast = {
                    'name' : request.POST.get('choosen_spell_name', ''),
                    'effect' : request.POST.get('effect', ''),
                    'damage_type' : request.POST.get('damage_type', ''),
                    'damage' : request.POST.get('damage', ''),
                    'cells' : request.POST.get('cells', ''),
                    'level' : request.POST.get('level', ''),
                    'cost' : request.POST.get('cost', '')
                }

                if (current_turn_owner == 'guest') and (current_battle.guest_spell != '0'):
                    if int(current_battle.guest_current_mp) >= int(request.POST.get('cost', '')):
                        current_battle.guest_spell = str(spell_to_cast)
                        current_battle.save()

                if (current_turn_owner == 'creator') and (current_battle.creator_spell != '0'):
                    if int(current_battle.creator_current_mp) >= int(request.POST.get('cost', '')):
                        current_battle.creator_spell = str(spell_to_cast)
                        current_battle.save()

                return(JsonResponse({'redirect_url' : host_name + '/heroes/battle', 'error_message' : 'i try to cast ' + str(request.POST.get('choosen_spell_name', ''))}))

############################################

            if request.POST.get('del', '') == 'del':
                deleteBattle(request)
                return(JsonResponse({'redirect_url' : host_name + '/heroes/search_battle'}))
                #return(JsonResponse({'error_message' : 'i try to delete'}))

            if request.POST.get('spell', '') == 'spell':
                #TMP = chooseSpell(request)
                return(JsonResponse({'redirect_url' : host_name + '/heroes/choose_spell'}))
                #return(JsonResponse({'error_message' : 'i try to cast'}))

            if (not request.POST.get('x', '')) or (not request.POST.get('y', '')):
                return(JsonResponse({'error_message' : 'not click x not click y'}))

            click_x = int(request.POST.get('x', ''))
            click_y = int(request.POST.get('y', ''))
            if (click_x < 90) or (click_x > 1165) or (click_y < 160) or (click_y > 835):
                return(JsonResponse({'error_message' : 'click not on field'}))

            TMP = calc.coordinatesToRelative(click_x, click_y)
            if not TMP:
                return(JsonResponse({'error_message' : 'got trouble calc.coordinatesToRelative'}))
            coords = [TMP[0], TMP[1]]

########################################### CAST SPELL IF HAVE SPELL!!!!

            try_to_cast_spell = calc.maybeSpell(current_battle.guest_spell, current_battle.creator_spell)
            if try_to_cast_spell:
                spell = try_to_cast_spell[0]
                spell_owner = try_to_cast_spell[1]
                TMP = calc.trySpell(spell, spell_owner, coords, units)
                current_battle.units = TMP[0]
                if spell_owner == 'guest':
                    current_battle.guest_spell = '0'
                    current_battle.guest_current_mp = str(int(current_battle.guest_current_mp) + TMP[1])
                    current_battle.creator_current_mp = str(int(current_battle.creator_current_mp) + TMP[2])
                if spell_owner == 'creator':
                    current_battle.creator_spell = '0'
                    current_battle.creator_current_mp = str(int(current_battle.guest_current_mp) + TMP[1])
                    current_battle.guest_current_mp = str(int(current_battle.guest_current_mp) + TMP[2])
                    
                current_battle.log = current_battle.log + TMP[3]
                current_battle.save()
                return(JsonResponse({'redirect_url' : host_name + '/heroes/battle'}))
            
########################################### CAST SPELL IF HAVE SPELL!!!!

            if coords in cells_shaded_cells:
                TMP = calc.moveUnit(coords, units)
                current_battle.units = str(TMP[0])
                current_battle.save()
                unit_id = TMP[1]
                unit_abs_coords_new = TMP[2]
                return(JsonResponse({
                    'unit_id' : unit_id,
                    'coordinates_x' : str(unit_abs_coords_new['x']),
                    'coordinates_y' : str(unit_abs_coords_new['y'])
                }))
            else:
                vectors = [TMP[2], TMP[3]]
                attacker = calc.currentUnitTurn(units)
                TMP_FOR_ATTACK = calc.maybeAttack(coords, vectors, units, cells_shaded_cells, attacker)
                if TMP_FOR_ATTACK:
                    new_attacker_coords = TMP_FOR_ATTACK[0]
                    target_unit = TMP_FOR_ATTACK[1]
                    target_unit_coords = TMP_FOR_ATTACK[2]

                    TMP = calc.moveUnit(new_attacker_coords, units)
                    current_battle.units = str(TMP[0])
                    current_battle.save()
                    unit_id = TMP[1]
                    unit_abs_coords_new = TMP[2]

                    target_list = calc.targetList(attacker, new_attacker_coords, target_unit_coords, units, target_unit)
                    for target in target_list:
                        attackUnit(attacker, target, current_battle)
                    if not ('_5_' in attacker['special']) and (str(target_unit['retaliation']) != '0'):
                        range_damage_koeff = calc.rangeDamageKoeff([int(attacker['x']), int(attacker['y'])], [int(target_unit['x']), int(target_unit['y'])])
                        if ('_1_' in attacker['special']) and range_damage_koeff:
                            pass
                        else:
                            target_list = calc.targetList(target_list[0], target_unit_coords, new_attacker_coords, units, attacker)
########################################MAKE ME!!!!
                            units = eval(current_battle.units)
                            for unit in units:
                                if (unit['name'] == target_unit['name']) and (unit['owner'] == target_unit['owner']):
                                    unit['retaliation'] = (int(unit['retaliation']) - 1)
                                    current_battle.units = str(units)
                                    current_battle.save()
                                    break
########################################MAKE ME!!!!
                            for target in target_list:
                                attackUnit(target_unit, target, current_battle)

                    return(JsonResponse({
                        'unit_id' : unit_id,
                        'coordinates_x' : str(unit_abs_coords_new['x']),
                        'coordinates_y' : str(unit_abs_coords_new['y'])
                    }))
                else:
                    return(JsonResponse({'error_message' : 'cant attack or move'}))
                TMP = calc.moveUnit(coords, units)
                current_battle.units = str(TMP[0])
                current_battle.save()
                unit_id = TMP[1]
                unit_abs_coords_new = TMP[2]
                return(JsonResponse({
                    'unit_id' : unit_id,
                    'coordinates_x' : str(unit_abs_coords_new['x']),
                    'coordinates_y' : str(unit_abs_coords_new['y'])
                }))

        context = RequestContext(request, {'battle_name' : battle_name, 'units' : units, 'shaded_cells' : abs_shaded_cells, 'log_message' : current_battle.log.split('$$$$$'), 'creator_spell' : current_battle.creator_spell, 'guest_spell' : current_battle.guest_spell})
        template = loader.get_template('heroes/battle.html')
        return HttpResponse(template.render(context))
    else:
        return redirect(host_name + '/heroes/search_battle/')

def attackUnit(attacker, target_unit, current_battle):

    phys_damage = calc.physDamage(attacker, target_unit)
    damage = phys_damage    ####    TMP!!!!!
    target_effects = target_unit['effects']
    stack_add = 0
############################
#   SPECIALS BLOCK!!!

#   archers 0.5 in mellee 0.5 after 10 hexes range
    if '_1_' in attacker['special']:
        range_damage_koeff = calc.rangeDamageKoeff([int(attacker['x']), int(attacker['y'])], [int(target_unit['x']), int(target_unit['y'])])

        if not range_damage_koeff:
            if not '_7_' in attacker['special']:
                damage = 0.5 * damage
        else:
            damage = range_damage_koeff * damage

#   150% damage to titans
    if ('_11_' in attacker['special']) and (target_unit['name'] == 'Titan'):
        damage = 1.5 * damage

#   cast weakness
    if ('_13_' in attacker['special']):
        if not '_neg.7(' in target_effects:
            spell = {
                'name' : 'Weakness',
                'effect' : 'neg.7(3)',
                'damage_type' : 'Water',
                'damage' : '0',
                'cells' : 'target',
                'level' : '2',
                'cost' : '0'
            }
            coords = [int(target_unit['x']), int(target_unit['y'])]
            units = eval(current_battle.units)
            TMP = calc.trySpell(str(spell), attacker['owner'], coords, units)
            current_battle.units = str(TMP[0])
            current_battle.log = current_battle.log + str(TMP[3])
            current_battle.save()

#   remove all positive spells
    if ('_14_' in attacker['special']):
        for effect in target_effects.split('_'):
            if 'pos.' in effect:
                TMP = getEffectStats(effect)#[force, number, duration]
                units = eval(current_battle.units)
                units = calc.dispelEffect(TMP[0], TMP[1], target_unit, units)
                current_battle.units = str(units)
                current_battle.log = current_battle.log + '$$$$$ All positive effects dispeled $$$$$'
                current_battle.save()

#   10% chance to kill top creature per 10 units
    if ('_15_' in attacker['special']):
        chance = int(int(attacker['stack']) / 10) * 10
        if random.randint(0, 100) <= chance:
            stack_add = -1

#   20% chance to poison
    if ('_16_' in attacker['special']):
        if random.randint(0, 100) <= 20:
            spell = {
                'name' : 'Poison',
                'effect' : 'neg.6(10)',
                'damage_type' : 'Water',
                'damage' : '0',
                'cells' : 'target',
                'level' : '1',
                'cost' : '0'
            }
            coords = [int(target_unit['x']), int(target_unit['y'])]
            units = eval(current_battle.units)
            TMP = calc.trySpell(str(spell), attacker['owner'], coords, units)
            current_battle.units = str(TMP[0])
            current_battle.log = current_battle.log + str(TMP[3])
            current_battle.save()

#   150% damage to master genies
    if ('_22_' in attacker['special']) and (target_unit['name'] == 'Master_Genie'):
        damage = 1.5 * damage

#   150% damage to archangels
    if ('_25_' in attacker['special']) and (target_unit['name'] == 'Archangel'):
        damage = 1.5 * phys_damage

#   20% chance to desease
    if ('_27_' in attacker['special']):
        if random.randint(0, 100) <= 20:
            spell = {
                'name' : 'Disease',
                'effect' : 'neg.2(3)',
                'damage_type' : '',
                'damage' : '0',
                'cells' : 'target',
                'level' : '1',
                'cost' : '0'
            }
            coords = [int(target_unit['x']), int(target_unit['y'])]
            units = eval(current_battle.units)
            TMP = calc.trySpell(str(spell), attacker['owner'], coords, units)
            current_battle.units = str(TMP[0])
            current_battle.log = current_battle.log + str(TMP[3])
            current_battle.save()

#   vampires regen
    if ('_30_' in attacker['special']):
########
        units = eval(current_battle.units)
        units.remove(attacker)
        unit = calc.healTarget(attacker, damage)
        units.append(unit)
        current_battle.units = str(units)
        current_battle.save()
########

#   20% chance to curse enemy
    if ('_32_' in attacker['special']):
        if random.randint(0, 100) <= 20:
            spell = {
                'name' : 'Curse',
                'effect' : 'neg.5(3)',
                'damage_type' : 'Fire',
                'damage' : '0',
                'cells' : 'target',
                'level' : '1',
                'cost' : '0'
            }
            coords = [int(target_unit['x']), int(target_unit['y'])]
            units = eval(current_battle.units)
            TMP = calc.trySpell(str(spell), attacker['owner'], coords, units)
            current_battle.units = str(TMP[0])
            current_battle.log = current_battle.log + str(TMP[3])
            current_battle.save()

#   20% chance to do double damage
    if ('_33_' in attacker['special']):
        if random.randint(0, 100) <= 20:
            damage = damage * 2

#   20% chance to age enemy
    if ('_35_' in attacker['special']):
        if random.randint(0, 100) <= 20:
            spell = {
                'name' : 'Age',
                'effect' : 'neg.4(3)',
                'damage_type' : '',
                'damage' : '0',
                'cells' : 'target',
                'level' : '1',
                'cost' : '0'
            }
            coords = [int(target_unit['x']), int(target_unit['y'])]
            units = eval(current_battle.units)
            TMP = calc.trySpell(str(spell), attacker['owner'], coords, units)
            current_battle.units = str(TMP[0])
            current_battle.log = current_battle.log + str(TMP[3])
            current_battle.save()

#   20% chance to do thunder
    if ('_38_' in attacker['special']):
        if random.randint(0, 100) <= 20:
            thunder_damage = (10 * int(attacker['stack']))
            spell = {
                'name' : 'Thunder',
                'effect' : '0',
                'damage_type' : '',
                'damage' : str(thunder_damage),
                'cells' : 'target',
                'level' : '1',
                'cost' : '0'
            }
            coords = [int(target_unit['x']), int(target_unit['y'])]
            units = eval(current_battle.units)
            TMP = calc.trySpell(str(spell), attacker['owner'], coords, units)
            current_battle.units = str(TMP[0])
            current_battle.log = current_battle.log + str(TMP[3])
            current_battle.save()

#   150% damage to efreet sultan
    if ('_42_' in attacker['special']) and (target_unit['name'] == 'Efreet_Sultan'):
        damage = 1.5 * damage

#   150% damage to black dragon
    if ('_44_' in attacker['special']) and (target_unit['name'] == 'Black_Dragon'):
        damage = 1.5 * damage

#   root enemy (dendroids)
    if ('_46_' in attacker['special']):
        spell = {
            'name' : 'Root',
            'effect' : 'neg.3(10)',
            'damage_type' : '',
            'damage' : '0',
            'cells' : 'target',
            'level' : '6',
            'cost' : '0'
        }
        coords = [int(target_unit['x']), int(target_unit['y'])]
        units = eval(current_battle.units)
        TMP = calc.trySpell(str(spell), attacker['owner'], coords, units)
        current_battle.units = str(TMP[0])
        current_battle.log = current_battle.log + str(TMP[3])
        current_battle.save()

#   +5% damage per cell (champions)
    if ('_51_' in attacker['special']):
        x_attacker = int(attacker['x'])
        y_attacker = int(attacker['y'])
        x_target = int(target_unit['x'])
        y_target = int(target_unit['y'])

        distance = int(calc.pointsDistance([x_attacker, y_attacker], [x_target, y_target]))
        if distance < 0:
            distance = 0
        damage = damage * (1 + distance * 0.05)

#   150% damage to arch devil
    if ('_52_' in attacker['special']) and (target_unit['name'] == 'Arch_Devil'):
        damage = 1.5 * damage

#   -50% damage to paralysed units
    if '_neg.8(' in target_unit['effects']:
        damage = damage * 0.5
        current_battle.units = str(calc.dispelEffect('neg', 8, target_unit, eval(current_battle.units)))
        current_battle.save()

#   20% chance to paralyze
    if '_8_' in attacker['special']:
        if '_1_' in attacker['special'] and range_damage_koeff:
            pass
        elif random.randint(0, 100) <= 20:
            spell = {
                'name' : 'Paralyze',
                'effect' : 'neg.8(3)',
                'damage_type' : '',
                'damage' : '0',
                'cells' : 'target',
                'level' : '1',
                'cost' : '0'
            }
            coords = [int(target_unit['x']), int(target_unit['y'])]
            units = eval(current_battle.units)
            TMP = calc.trySpell(str(spell), attacker['owner'], coords, units)
            current_battle.units = str(TMP[0])
            current_battle.log = current_battle.log + str(TMP[3])
            current_battle.save()

#   SPECIALS BLOCK!!!
############################

    units = eval(current_battle.units)
    damage = int((calc.luck(attacker, units) * damage))
    TMP = calc.targetUnitsLeft(damage, target_unit)

    for unit in units:
        if unit['name'] == target_unit['name'] and unit['owner'] == target_unit['owner']:
            unit['stack'] = TMP[0] + stack_add
            unit['health_left'] = TMP[1]
            if TMP[0] == 0 and TMP[1] == 0:
                units.remove(unit)
            break

############################
#   fire shield efreet
    if '_23_' in target_unit['special']:
        damage = int(damage * 0.5)
        units = str(calc.damageTarget(units, attacker, damage))#    MAKE ME!!!!!!
############################

    current_battle.units = str(units)
    current_battle.log = current_battle.log + '$$$$$' + (str(attacker['name']) + ' attack ' + str(target_unit['name']) + ' for ' + str(damage) + ' damage')
    current_battle.save()

    return

def clickBattle(request):
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login/')

    if request.method == 'POST' and request.is_ajax():
        click_x = int(request.POST.get('x', ''))
        click_y = int(request.POST.get('y', ''))
        coords = recalcCoordinatesToRelative(click_x, click_y)
        return(JsonResponse({'error_message' : 'x:' + str(coords[0]) + ' y:' + str(coords[1])}))

    return redirect(host_name + '/heroes/login/')  

def makeBattle(request):
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login/')

    if request.method == 'POST' and request.is_ajax():
        form = MakeBattle(request.POST)
        if form.is_valid():
############################        MAKE ME!!!!!!
            try:
                if Battle.objects.get(name = form.cleaned_data['name']):
                    return(JsonResponse({'error_message' : 'battle_name already exsist'}))
            except:
                pass
############################        MAKE ME!!!!!!
            pk = isLoggedIn(token)
            new_battle = Battle(
                name = form.cleaned_data['name'],
                state = 'empty',
                creator_pk = pk,
                guest_pk = '',
                creator_castle = form.cleaned_data['creator_castle'],
                guest_castle = 'None',
                growth = form.cleaned_data['growth'],
                units = '{0}',
                log = 'Battle start! $$$$$',
                creator_spell = '',
                guest_spell = '',
                creator_current_mp = 0,
                guest_current_mp = 0,
            )
            new_battle.pk = pk
            new_battle.save()
            return(JsonResponse({'redirect_url' : host_name + '/heroes/search_battle'}))
            #return(JsonResponse({'error_message' : 'make battle ' + str(pk)}))
        else:
            return(JsonResponse({'error_message' : 'got trouble'}))

    template = loader.get_template('heroes/make_battle.html')
    context = RequestContext(request, processors = [makeBattleProc])
    return HttpResponse(template.render(context))

def searchBattle(request):
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login/')

    if request.method == 'POST' and request.is_ajax():
        battle_name = request.POST.get('connect_to', '')
        if addGuestToBattle(battle_name, isLoggedIn(token)):
            return(JsonResponse({'redirect_url' : host_name + '/heroes/start_battle'}))
        else:
            return(JsonResponse({'error_message' : str(battle_name) + ' not empty ' + str(isLoggedIn(token))}))

    all_empty_battles = showEmptyBattles()
    template = loader.get_template('heroes/search_battle.html')
    context = RequestContext(request, {'all_empty_battles' : all_empty_battles})
    return HttpResponse(template.render(context))

def addGuestToBattle(battle_name, guest_pk):
    all_battles = Battle.objects.all()
    removePlayerFromALLBattles(str(guest_pk))
    for battle in all_battles:
        if battle.name == str(battle_name) and battle.state == 'empty':
            guests = battle.guest_pk
            guests = guests + str(guest_pk) + ','
            battle.guest_pk = guests
            battle.save()
            return True

    return False

def removePlayerFromALLBattles(player_pk):
    all_battles = Battle.objects.all()
    for battle in all_battles:
        guests = battle.guest_pk.split(',')
        creator = str(battle.creator_pk)
        if player_pk in guests:
            guests.remove(player_pk)
            tmp = ''
            for guest in guests:
                tmp = tmp + str(guest) + ','
            battle.guest_pk = tmp
            battle.save()
        if creator == player_pk:
            battle.delete()

def index(request):
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login/')
    else:
        return redirect(host_name + '/heroes/castle/')

def login(request):
    global host_name
    token = csrf.get_token(request)
    if isLoggedIn(token):
        return redirect(host_name + '/heroes/castle/')

    if request.method == 'POST' and request.is_ajax():
        form = Login(request.POST)
        if form.is_valid():
            user_name_to_check = form.cleaned_data['user_name']
            password_to_check = form.cleaned_data['password']

            users = User.objects.all()
            for user in users:
                if user.user_name == user_name_to_check:
                    if user.password == password_to_check:
####                REDIRECT!!!
                        loginUser(user.pk, token)
                        return(JsonResponse({'redirect_url' : host_name + '/heroes/castle'}))
####                REDIRECT!!!
                    else:
                        return(JsonResponse({'error_message' : str(user.password) + '<p></p>' + str(password_to_check) + str(token)}))
            return(JsonResponse({'error_message' : 'no user'}))

    template = loader.get_template('heroes/login.html')
    context = RequestContext(request, processors = [loginProc])
    return HttpResponse(template.render(context))

def register(request):
    global host_name
    if request.method == 'POST' and request.is_ajax():
        form = Registration(request.POST)
        if form.is_valid():
            new_user_nick_name = form.cleaned_data['user_name']
            new_user_email = form.cleaned_data['email']
            new_user_password = form.cleaned_data['password']
            try:
                if User.objects.get(user_name = new_user_nick_name):
                    return(JsonResponse({'error_message' : 'nick_name already exsist'}))
                if User.objects.get(email = new_user_email):
                    return(JsonResponse({'error_message' : 'email already exsist'}))
            except:
                pass

            config_file = open('/home/nick/mysite/heroes/config.dat', 'r')
            max_pk = int(config_file.readlines()[0]) + 1
            config_file.close()

            config_file = open('/home/nick/mysite/heroes/config.dat', 'w')
            config_file.write(str(max_pk))
            config_file.close()
            
            new_user = User(user_name = new_user_nick_name, email = new_user_email, password = new_user_password)
            new_user.pk = max_pk
            new_user.save()

            new_player = Player(
                nick_name = new_user_nick_name,
                avatar = 'default',
                rating = 1000,
                win_count = 0,
                loose_count = 0,
                level = 0,
                experience = 0,
                skills = '',
                special = '',
                attributes = str({'Att':'0', 'Def':'0', 'SP':'0', 'Kno':'0',}),
                spells = ''
            )
            new_player.pk = max_pk
            new_player.save()
####                REDIRECT!!!
            token = csrf.get_token(request)
            loginUser(new_user.pk, token)
            return(JsonResponse({'redirect_url' : host_name + '/heroes/castle'}))
####                REDIRECT!!!
    template = loader.get_template('heroes/registration.html')
    context = RequestContext(request, processors = [registrationProc])
    return HttpResponse(template.render(context))

def castle(request):
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login')

    if request.method == 'POST' and request.is_ajax():
        return(JsonResponse({'redirect_url' : host_name + '/heroes'}))

    template = loader.get_template('heroes/castle.html')

    pk = isLoggedIn(token)

    try:
        current_user = Player.objects.get(pk = pk)
        current_user_name = current_user.nick_name
    except:
        current_user_name = 'Nigga'
    message = 'Hello ' + str(current_user_name) + ' ' + str(pk) + '!'
    context = RequestContext(request, {'message' : message, 'all_users' : showAllLoggedInUsers()})
    return HttpResponse(template.render(context))

def logout(request):
    global host_name
    token = csrf.get_token(request)
    if token:
        logoutUser(token)
        return(JsonResponse({'redirect_url' : host_name + '/heroes'}))
    else:
        return(JsonResponse({'error_message' : 'logout unsucces'}))

def logoutUser(token):
    AuthUser.objects.filter(token = token).delete()

def isLoggedIn(token):
    current_users = AuthUser.objects.all()
    for user in current_users:
        if user.token == token:
            return(user.pk)
    return(False)

def loginUser(pk, token):
    current_users = AuthUser.objects.all()
    for user in current_users:
        if str(user.pk) == pk:
            user.token = token
            user.save()
            return()
    new_auth_user = AuthUser(token = token)
    new_auth_user.pk = pk
    new_auth_user.save()
    return()

def loginProc(request):
    return {
       'form' : Login(request.POST),
    }

def registrationProc(request):
    return {
       'form' : Registration(request.POST),
    }

def makeUnitProc(request):
    return {
       'form' : MakeUnit(request.POST),
    }

def makeSpellProc(request):
    return {
       'form' : MakeSpell(request.POST),
    }

def makeBattleProc(request):
    return {
       'form' : MakeBattle(request.POST),
    }

def makeUnit(request):
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/login/')

    if request.method == 'POST' and request.is_ajax():
        form = MakeUnit(request.POST)
        if form.is_valid():            
            new_unit = Unit(
                castle = form.cleaned_data['castle'],
                name = form.cleaned_data['name'],
                attack_skill = form.cleaned_data['attack_skill'],
                defense_skill = form.cleaned_data['defense_skill'],
                minimum_damage = form.cleaned_data['minimum_damage'],
                maximum_damage = form.cleaned_data['maximum_damage'],
                health = form.cleaned_data['health'],
                speed = form.cleaned_data['speed'],
                growth = form.cleaned_data['growth'],
                special = form.cleaned_data['special']
            )
            new_unit.save()
            return(JsonResponse({'error_message' : 'added'}))
        else:
            return(JsonResponse({'error_message' : 'got trouble'}))

    all_units = Unit.objects.all()
    units = calc.showAllUnitsInfo(all_units)

    template = loader.get_template('heroes/make_unit.html')
    context = RequestContext(request, {'units' : units}, processors = [makeUnitProc])
    return HttpResponse(template.render(context))

def stats(request):
    global host_name
    token = csrf.get_token(request)
    pk = isLoggedIn(token)
    if not pk:
        return redirect(host_name + '/login/')

    hero = calc.showAllHeroInfo(Player.objects.get(pk = pk))

    template = loader.get_template('heroes/stats.html')
    context = RequestContext(request, {'hero' : hero})
    return HttpResponse(template.render(context))

def info(request):
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/login/')        

    template = loader.get_template('heroes/info.html')
    context = RequestContext(request, {'castles' : ['test', 'test_non_exist']})
    return HttpResponse(template.render(context))

def leaderboard(request):
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/login/')

    all_players = Player.objects.all()
    top_players = calc.topPlayers(all_players)[:25]

    template = loader.get_template('heroes/leaderboard.html')
    context = RequestContext(request, {'players' : top_players})
    return HttpResponse(template.render(context))

def showEmptyBattles():
    tmp = []
    all_battles = Battle.objects.all()
    for battle in all_battles:
        if battle.state == 'empty':
            pk = battle.creator_pk
            creator_name = Player.objects.get(pk = pk).nick_name
            message = [
                str(battle.name),
                str(battle.creator_castle),
                str(battle.growth),
                str(creator_name)
            ]
            tmp.append(message)
    return tmp

def currentPlayerBattle(pk):
    all_battles = Battle.objects.all()
    for battle in all_battles:
        if battle.state == 'in_battle':
            creator_pk = str(battle.creator_pk)
            guest_pk = str(battle.guest_pk)
            if creator_pk == str(pk) or guest_pk == str(pk):
                return (battle)
    return False

def showAllLoggedInUsers():
    current_users = AuthUser.objects.all()
    tmp = []
    for user in current_users:
        tmp.append([str(user.pk), str(user.token)])
    return(tmp)

def changeUnit(request):
    global host_name
    token = csrf.get_token(request)

    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login/')

    if request.method == 'POST' and request.is_ajax():
        current_unit_castle = request.POST.get('current_unit_castle', '')
        current_unit_name = request.POST.get('current_unit_name', '')
        Unit.objects.filter(castle = current_unit_castle, name = current_unit_name).delete()

        new_unit = Unit(
            castle = request.POST.get('castle', ''),
            name = request.POST.get('name', ''),
            attack_skill = request.POST.get('attack_skill', ''),
            defense_skill = request.POST.get('defense_skill', ''),
            minimum_damage = request.POST.get('minimum_damage', ''),
            maximum_damage = request.POST.get('maximum_damage', ''),
            health = request.POST.get('health', ''),
            speed = request.POST.get('speed', ''),
            growth = request.POST.get('growth', ''),
            special = request.POST.get('special', '')
        )
        new_unit.save()
        return(JsonResponse({'redirect_url' : host_name + '/heroes/make_unit'}))
        #return(JsonResponse({'error_message' : 'ok'}))
    else:
        return(JsonResponse({'error_message' : 'got trouble'}))

    return redirect(host_name + '/heroes/make_unit')

def startBattle(request):
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login/')
###########################
    if request.method == 'POST' and request.is_ajax():
        guest_castle = request.POST.get('guest_castle', '')
        all_battles = Battle.objects.all()
        pk = isLoggedIn(token)
        for battle in all_battles:
            guests_pk = battle.guest_pk
            if (str(pk) in guests_pk.split(',')) or (int(pk) in guests_pk.split(',')):
                battle.state = 'in_battle'
                battle.guest_pk = str(pk)
                battle.guest_castle = guest_castle
                battle.units = str(TMPUnitsStats(battle))
                battle.creator_current_mp = 100 #TMP
                battle.guest_current_mp = 100   #TMP
                battle.creator_spell = '1'
                battle.guest_spell = '1'
                battle.save()
                break
        return(JsonResponse({'redirect_url' : host_name + '/heroes/battle/'}))
###########################
    all_battles = Battle.objects.all()
    pk = isLoggedIn(token)
    context = RequestContext(request)
    for battle in all_battles:
        guests_pk = battle.guest_pk
        creator_pk = battle.creator_pk
        if str(pk) == str(creator_pk):
            context = RequestContext(request, {'growth' : str(battle.growth), 'creator_castle' : battle.creator_castle, 'creator_name' : str(Player.objects.get(pk = battle.creator_pk).nick_name), 'battle_name' : battle.name})
            break
        if (str(pk) in guests_pk.split(',')) or (int(pk) in guests_pk.split(',')):
            context = RequestContext(request, {'growth' : str(battle.growth), 'creator_castle' : battle.creator_castle, 'creator_name' : str(Player.objects.get(pk = battle.creator_pk).nick_name), 'guest' : True, 'battle_name' : battle.name})
            break

    template = loader.get_template('heroes/start_battle.html')
    return HttpResponse(template.render(context))

def deleteBattle(request):  ################      MAKE ME!!!!
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login/')

    if request.method == 'POST' and request.is_ajax():
        pk = str(isLoggedIn(token))
        all_battles = Battle.objects.all()
        for battle in all_battles:
            if (str(battle.state) == 'in_battle') and (str(battle.creator_pk) == pk or str(battle.guest_pk) == pk) :
                battle.delete()
                return(JsonResponse({'redirect_url' : host_name + '/heroes/search_battle'}))
        return(JsonResponse({'error_message' : 'got trouble'}))

    return redirect(host_name + '/heroes/search_battle/')
                            ################      MAKE ME!!!!

def TMPUnitsStats(current_battle):
    creator_castle = current_battle.creator_castle
    guest_castle = current_battle.guest_castle
    battle_growth = current_battle.growth

    all_players = Player.objects.all()
    for player in all_players:
        if int(player.pk) == int(current_battle.guest_pk):
            guest_player = player
        if int(player.pk) == int(current_battle.creator_pk):
            creator_player = player


    guest_att = int(eval(guest_player.attributes)['Att'])
    guest_def = int(eval(guest_player.attributes)['Def'])
    guest_luck = 0
    if 'Luck' in guest_player.skills:
        luck = eval(guest_player.skills)['Luck']
        if luck == 'bas':
            add_luck = 1
        elif luck == 'adv':
            add_luck = 2
        elif luck == 'exp':
            add_luck = 3
        guest_luck = guest_luck + add_luck
    guest_morale = 1
    if 'Leadership' in guest_player.skills:
        Leadership = eval(guest_player.skills)['Leadership']
        if Leadership == 'bas':
            add_morale = 1
        elif Leadership == 'adv':
            add_morale = 2
        elif Leadership == 'exp':
            add_morale = 3
        guest_morale = guest_morale + add_morale
    creator_att = int(eval(creator_player.attributes)['Att'])
    creator_def = int(eval(creator_player.attributes)['Def'])
    creator_luck = 0
    if 'Luck' in creator_player.skills:
        luck = eval(creator_player.skills)['Luck']
        if luck == 'bas':
            add_luck = 1
        elif luck == 'adv':
            add_luck = 2
        elif luck == 'exp':
            add_luck = 3
        creator_luck = creator_luck + add_luck
    creator_morale = 0
    if 'Leadership' in creator_player.skills:
        Leadership = eval(creator_player.skills)['Leadership']
        if Leadership == 'bas':
            add_morale = 1
        elif Leadership == 'adv':
            add_morale = 2
        elif Leadership == 'exp':
            add_morale = 3
        creator_morale = creator_morale + add_morale
    
    i_creator = 0
    i_guest = 0

    list_of_all_units = []
    all_units = Unit.objects.all()
    
    for unit in all_units:
        if unit.castle == creator_castle:
            x = 14
            if '_3_' in unit.special:
                x = 13
            coords_abs = calc.coordinatesToAbs(x, i_creator, 60, 100)
            if '_3_' in unit.special:
                coords_abs = calc.coordinatesToAbs(x, i_creator, 60, 100)

            retaliation = 1
            if '_50_' in unit.special:
                retaliation = 100

            unit_to_append = {
                'owner' : 'creator',
                'turn' : str(1),
#####
                'attack_skill' : str(int(unit.attack_skill) + creator_att),
                'defense_skill' : str(int(unit.defense_skill) + creator_def),
                'minimum_damage' : str(int(unit.minimum_damage)),
                'maximum_damage' : str(int(unit.maximum_damage)),
                'health' : str(int(unit.health)),
                'health_left' : str(int(unit.health)),
                'stack' : str(int(unit.growth) * int(battle_growth)),
                'luck' : str(0 + creator_luck),
                'morale' : str(1 + creator_morale),
                'effects' : str(''),
                'retaliation' : retaliation,
                'resistance' : str(5),
####
                'speed' : str(unit.speed),
                'x' : str(x),
                'y' : str(i_creator),
                'x_abs' : str(coords_abs[0]),
                'y_abs' : str(coords_abs[1]),
                'name' : unit.name,
                'castle' : unit.castle,
                'special' : unit.special,
                'picture' : 'heroes/units/' + unit.castle + '/' + unit.name + '_creator.png'
            }
            list_of_all_units.append(unit_to_append)
            i_creator = i_creator + 1
        if unit.castle == guest_castle:
            x = 0
            if '_3_' in unit.special:
                x = 1
            coords_abs = calc.coordinatesToAbs(x, i_guest, 60, 100)
            if '_3_' in unit.special:
                coords_abs = calc.coordinatesToAbs(x - 1, i_guest, 60, 100)

            retaliation = 1
            if '_50_' in unit.special:
                retaliation = 100

            unit_to_append = {
                'owner' : 'guest',
                'turn' : str(1),
####
                'attack_skill' : str(int(unit.attack_skill) + guest_att),
                'defense_skill' : str(int(unit.defense_skill) + guest_def),
                'minimum_damage' : str(int(unit.minimum_damage)),
                'maximum_damage' : str(int(unit.maximum_damage)),
                'health' : str(int(unit.health)),
                'health_left' : str(int(unit.health)),
                'stack' : str(int(unit.growth) * int(battle_growth)),
                'luck' : str(0 + guest_luck),
                'morale' : str(1 + guest_morale),
                'effects' : str(''),
                'retaliation' : retaliation,
                'resistance' : str(5),
####
                'speed' : str(unit.speed),
                'x' : str(x),
                'y' : str(i_guest),
                'x_abs' : str(coords_abs[0]),
                'y_abs' : str(coords_abs[1]),
                'name' : unit.name,
                'castle' : unit.castle,
                'special' : unit.special,
                'picture' : 'heroes/units/' + unit.castle + '/' + unit.name + '_guest.png'
            }
            list_of_all_units.append(unit_to_append)
            i_guest = i_guest + 1

    return (list_of_all_units)

def changeSpell(request):
    global host_name
    token = csrf.get_token(request)

    if not isLoggedIn(token):
        return redirect(host_name + '/heroes/login/')

    if request.method == 'POST' and request.is_ajax():
        current_spell_name = request.POST.get('current_spell_name', '')
        Spell.objects.filter(name = current_spell_name).delete()

        new_spell = Spell(
            name = request.POST.get('name', ''),
            effect = request.POST.get('effect', ''),
            cells = request.POST.get('cells', ''),
            damage_type = request.POST.get('damage_type', ''),
            damage_formula = request.POST.get('damage_formula', ''),
            level= request.POST.get('level', ''),
            description = request.POST.get('description', ''),
            cost = request.POST.get('cost', ''),
        )
        new_spell.save()
        return(JsonResponse({'redirect_url' : host_name + '/heroes/make_spell'}))
        #return(JsonResponse({'error_message' : 'ok'}))
    else:
        return(JsonResponse({'error_message' : 'got trouble'}))

    return redirect(host_name + '/heroes/make_spell')

def makeSpell(request):
    global host_name
    token = csrf.get_token(request)
    if not isLoggedIn(token):
        return redirect(host_name + '/login/')

    if request.method == 'POST' and request.is_ajax():
        form = MakeSpell(request.POST)
        if form.is_valid():            
            new_spell = Spell(
                name = form.cleaned_data['name'],
                effect = form.cleaned_data['effect'],
                cells = form.cleaned_data['cells'],
                damage_type = form.cleaned_data['damage_type'],
                damage_formula = form.cleaned_data['damage_formula'],
                level= form.cleaned_data['level'],
                description = form.cleaned_data['description'],
                cost = form.cleaned_data['cost'],
            )
            new_spell.save()
            return(JsonResponse({'error_message' : 'added'}))
 #       else:
  #          return(JsonResponse({'error_message' : 'got trouble'}))
    all_spells = Spell.objects.all()
    spells = calc.showAllSpellsInfo(all_spells)

    template = loader.get_template('heroes/make_spell.html')
    context = RequestContext(request, {'spells' : spells}, processors = [makeSpellProc])
    return HttpResponse(template.render(context))

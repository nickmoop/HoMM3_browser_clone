from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from HoMM3_browser_clone.settings import HOST_NAME
from heroes_3 import forms
from heroes_3.models import (
    Battles, Players, check_username_password, is_logged_in, get_user_by_token,
    register_new_user, create_battle
)
from heroes_core.Spell import ALL_SPELLS, BattleSpell
from heroes_core.Unit import (
    BattleUnit, add_units_to_battle, get_shaded_cells
)
from heroes_core.helper_methods import (
    get_csrf_token_from_request, coordinates_to_relative
)
from heroes_core.TMP_some_constants import CREATOR, GUEST


class Index(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return redirect('user_login')


class Login(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        form = forms.Login(request.POST)
        if form.is_valid():
            user = check_username_password(form)
            if user:
                token = get_csrf_token_from_request(request)
                user.update_user_token(token)

                return JsonResponse(
                    {'redirect_url': '{}/castle'.format(HOST_NAME)})
            else:
                return JsonResponse(
                    {'error_message': 'wrong use name or password'})

        return JsonResponse({'error_message': 'Invalid form'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.Login()

        return context


class Logout(TemplateView):
    template_name = 'logout.html'

    @is_logged_in
    def get(self, request, *args, **kwargs):
        token = get_csrf_token_from_request(request)
        user = get_user_by_token(token)
        if user:
            user.update_user_token(None)

        return JsonResponse({'redirect_url': '{}/login'.format(HOST_NAME)})


class Registration(TemplateView):
    template_name = 'registration.html'

    def post(self, request, *args, **kwargs):
        form = forms.Registration(request.POST)
        if form.is_valid():
            token = get_csrf_token_from_request(request)
            if register_new_user(form, token):
                registration_result = JsonResponse(
                    {'redirect_url': '{}/castle'.format(HOST_NAME)})
            else:
                registration_result = JsonResponse(
                    {'error_message': 'user name or email already exsist'})
        else:
            registration_result = JsonResponse(
                {'error_message': 'form invalid'})

        return registration_result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.Registration()

        return context


class UserCastle(TemplateView):
    template_name = 'castle.html'

    @is_logged_in
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        token = get_csrf_token_from_request(request)
        context['user'] = get_user_by_token(token)
        context['tmp_token'] = token

        return self.render_to_response(context)


class UserStats(TemplateView):
    template_name = 'stats.html'

    @is_logged_in
    def get(self, request, *args, **kwargs):
        token = get_csrf_token_from_request(request)
        user = get_user_by_token(token)
        self.extra_context = {'player_info': user.player.info}

        return super().get(request, *args, **kwargs)


class Information(TemplateView):
    template_name = 'information.html'

    @is_logged_in
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LeaderBoard(TemplateView):
    template_name = 'leaderboard.html'

    @is_logged_in
    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'players': Players.objects.order_by('-rating')[:10]}

        return super().get(request, *args, **kwargs)


class SearchBattle(TemplateView):
    template_name = 'search_battle.html'

    @is_logged_in
    def post(self, request, *args, **kwargs):
        battle_pk = request.POST['connect_to']
        if battle_pk:
            battle = Battles.objects.get(pk=battle_pk)
            if battle:
                token = get_csrf_token_from_request(request)
                user = get_user_by_token(token)
                if user.battle is None:
                    battle.guest = user.player
                    battle.guest_castle = request.POST['guest_castle']
                    add_units_to_battle(battle, CREATOR)
                    add_units_to_battle(battle, GUEST)
                    battle.log = ''
                    battle.state = 'in_game'
                    battle.save()
                    user.update_battle(battle)
                    user.player.current_mp = user.player.maximum_mp
                    user.player.save()
                else:
                    return JsonResponse(
                        {'error_message': 'you already waiting for battle'})

        return JsonResponse(
            {'redirect_url': '{}/battle'.format(HOST_NAME)})

    @is_logged_in
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_empty_battles'] = Battles.get_empty_battles()

        return context


class CreateBattle(TemplateView):
    template_name = 'create_battle.html'

    @is_logged_in
    def post(self, request, *args, **kwargs):
        token = get_csrf_token_from_request(request)
        user = get_user_by_token(token)
        form = forms.MakeBattle(request.POST)

        if form.is_valid():
            new_battle = create_battle(form, user)
        else:
            return JsonResponse(
                {'error_message': 'something wrong with form'})

        if new_battle:
            return JsonResponse(
                {'redirect_url': '{}/search_battle'.format(HOST_NAME)})
        else:
            return JsonResponse(
                {'error_message': 'something wrong with battle creation'})

    @is_logged_in
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.MakeBattle()

        return context


class UserBattle(TemplateView):
    template_name = 'battle.html'

    @is_logged_in
    def post(self, request, *args, **kwargs):
        click_x, click_y = int(request.POST['x']), int(request.POST['y'])

        if click_x < 90 or click_x > 1165 or click_y < 160 or click_y > 835:
            return JsonResponse({'error_message': 'click not on field'})

        new_cell, vector = coordinates_to_relative([click_x, click_y])
        if not new_cell:
            return JsonResponse(
                {'error_message': 'got trouble calc.coordinatesToRelative'})

        token = get_csrf_token_from_request(request)
        user = get_user_by_token(token)
        battle = user.battle
        if battle is None:
            return redirect('user_search_battle')

        units = BattleUnit.from_json(battle.units)
        unit_to_move = BattleUnit.get_unit_to_move(units)

        if getattr(battle, unit_to_move.role) != user.player:
            return JsonResponse(
                {'redirect_url': '{}/battle'.format(HOST_NAME)})

        spell_to_cast = user.player.spell_to_cast
        if spell_to_cast:
            spells = user.player.make_battle_spells(ALL_SPELLS)
            if spell_to_cast in spells.keys():
                user.player.cast_spell(spells[spell_to_cast], units, new_cell)
                battle.update_units(units)
                battle.save()

                return JsonResponse(
                    {'redirect_url': '{}/battle'.format(HOST_NAME)})

        shaded_cells_abs, shaded_cells = get_shaded_cells(units, unit_to_move)

        if new_cell in shaded_cells and shaded_cells[new_cell] != 'red':
            unit_to_move.move(new_cell, units)
            battle.update_units(units)
        else:
            new_cell, target_unit = unit_to_move.maybe_attack_other_unit(
                new_cell, vector, units, shaded_cells)

            if new_cell and target_unit:
                unit_to_move.move(new_cell, units)
                attack_log_message = unit_to_move.attack(target_unit, units)
                battle.log += attack_log_message
                battle.update_units(units)

        return JsonResponse({'redirect_url': '{}/battle'.format(HOST_NAME)})

    @is_logged_in
    def get(self, request, *args, **kwargs):
        token = get_csrf_token_from_request(request)
        user = get_user_by_token(token)
        battle = user.battle
        if battle is None:
            return redirect('user_search_battle')

        units = BattleUnit.from_json(battle.units)

        left_roles = set()
        for unit in units.values():
            left_roles.add(unit.role)

        if len(left_roles) == 1:
            battle.calculate_rating(list(left_roles)[0])
            battle.delete()

            return redirect('user_search_battle')

        unit_to_move = BattleUnit.get_unit_to_move(units)
        if not unit_to_move:
            battle.next_round(units)
            unit_to_move = BattleUnit.get_unit_to_move(units)

        if getattr(battle, unit_to_move.role) == user.player:
            shaded_cells_abs, shaded_cells = get_shaded_cells(
                units, unit_to_move)
            spell_to_cast = user.player.spell_to_cast
        else:
            shaded_cells_abs = None
            spell_to_cast = None

        self.extra_context = {
            'battle': battle,
            'battle_log': battle.log.split('\n'),
            'shaded_cells': shaded_cells_abs,
            'casting_spell_name': spell_to_cast,
            'player_mp': user.player.current_mp
        }

        return super().get(request, *args, **kwargs)


class DeleteBattle(TemplateView):
    template_name = 'battle.html'

    @is_logged_in
    def post(self, request, *args, **kwargs):
        token = get_csrf_token_from_request(request)
        user = get_user_by_token(token)
        battle = user.battle
        battle.delete()

        return JsonResponse(
            {'redirect_url': '{}/castle'.format(HOST_NAME)})


class ChooseSpell(TemplateView):
    template_name = 'choose_spell.html'

    @is_logged_in
    def post(self, request, *args, **kwargs):
        cast_spell_name = request.POST.get('cast_spell_name', None)
        if cast_spell_name:
            token = get_csrf_token_from_request(request)
            player = get_user_by_token(token).player
            player.spell_to_cast = cast_spell_name
            player.save()

        return JsonResponse({'redirect_url': '{}/battle'.format(HOST_NAME)})

    @is_logged_in
    def get(self, request, *args, **kwargs):
        token = get_csrf_token_from_request(request)
        user = get_user_by_token(token)
        spells = user.player.make_battle_spells(ALL_SPELLS)
        self.extra_context = {'spells': BattleSpell.to_json(spells)}

        return super().get(request, *args, **kwargs)

from django.http import JsonResponse
from django.views import View

from heroes_3.models import (
    login_user_by_password, register_new_user, get_user_by_token,
)
from heroes_core.helper_methods import get_csrf_token_from_request


class Help(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'help text there': 'help text there'})


class Login(View):
    def post(self, request, *args, **kwargs):
        token = login_user_by_password(request)

        return JsonResponse({'token': token})


class Registration(View):
    def post(self, request, *args, **kwargs):
        user = register_new_user(request)
        if not user:
            return JsonResponse({'status': 'error'})

        return JsonResponse({
            'status': 'ok',
            'user_name': user.user_name,
            'email': user.email,
            'password': user.password,
            'token': user.token
        })


class UserStats(View):
    def get(self, request, *args, **kwargs):
        token = get_csrf_token_from_request(request)
        user = get_user_by_token(token)
        if not user:
            return JsonResponse({'status': 'error'})

        return JsonResponse(user.player.info)

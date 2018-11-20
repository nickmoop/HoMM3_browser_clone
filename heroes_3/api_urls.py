from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from heroes_3.views_api import Help, Login, Registration, UserStats


urlpatterns = [
    path('help', Help.as_view(), name='api_help'),
    path('login', csrf_exempt(Login.as_view()), name='api_login'),
    path('stats', UserStats.as_view(), name='api_stats'),
    path(
        'registration', csrf_exempt(Registration.as_view()),
        name='api_registration'
    ),
]

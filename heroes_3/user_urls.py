from django.urls import path

from heroes_3.views import (
    UserCastle, Login, Logout, Index, Registration, UserStats, LeaderBoard,
    Information, SearchBattle, CreateBattle, UserBattle, DeleteBattle,
    ChooseSpell
)


urlpatterns = [
    path('', Index.as_view(), name='user_index'),
    path('login', Login.as_view(), name='user_login'),
    path('logout', Logout.as_view(), name='user_logout'),
    path('registration', Registration.as_view(), name='user_registration'),
    path('castle', UserCastle.as_view(), name='user_castle'),
    path('stats', UserStats.as_view(), name='user_stats'),
    path('leaderboard', LeaderBoard.as_view(), name='user_leaderboard'),
    path('information', Information.as_view(), name='user_information'),
    path('search_battle', SearchBattle.as_view(), name='user_search_battle'),
    path('create_battle', CreateBattle.as_view(), name='user_create_battle'),
    path('battle', UserBattle.as_view(), name='user_battle'),
    path('delete_battle', DeleteBattle.as_view(), name='user_delete_battle'),
    path('choose_spell', ChooseSpell.as_view(), name='user_choose_spell'),
]

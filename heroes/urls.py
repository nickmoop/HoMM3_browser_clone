from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from heroes import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration', views.register),
    url(r'^login', views.login),
    url(r'^castle', views.castle),
    url(r'^logout', views.logout),
    url(r'^info', views.info),
    url(r'^stats', views.stats),
    url(r'^leaderboard', views.leaderboard),
    url(r'^search_battle', views.searchBattle),
    url(r'^make_unit', views.makeUnit),
    url(r'^make_battle', views.makeBattle),
    url(r'^start_battle', views.startBattle),
    url(r'^battle', views.battle),
    url(r'^change_unit', views.changeUnit),
    url(r'^delete_battle', views.deleteBattle),
    url(r'^click_battle', views.clickBattle),
    url(r'^choose_spell', views.chooseSpell),
    url(r'^make_spell', views.makeSpell),
    url(r'^change_spell', views.changeSpell),
    url(r'^change_player', views.changePlayer),
]

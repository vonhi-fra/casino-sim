from django.urls import path
from . import views
from . import bot_views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-player/', views.create_player, name='create_player'),
    path('play/<int:player_id>/', views.play_game, name='play_game'),
    path('roulette/<int:player_id>/', views.play_roulette, name='play_roulette'),
    path('bot/<int:player_id>/', bot_views.bot_play, name='bot_play'),
    path('bot-stats/<int:player_id>/', bot_views.bot_statistics, name='bot_statistics'),

]
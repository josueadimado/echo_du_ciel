"""
URL configuration for lyrics app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.setlist_view, name='setlist'),
    path('songs/', views.songs_list_view, name='songs_list'),
    path('song/<slug:slug>/', views.song_detail_view, name='song_detail'),
    path('programme/', views.program_view, name='program'),
    path('programme/download/', views.download_program_view, name='download_program'),
    
    # Projection
    path('screen/', views.screen_view, name='screen'),
    
    # Control
    path('control/', views.control_view, name='control'),
    path('control/set-song/<int:song_id>/', views.control_set_song_view, name='control_set_song'),
    path('control/next/', views.control_next_view, name='control_next'),
    path('control/prev/', views.control_prev_view, name='control_prev'),
    
    # API
    path('api/state/', views.api_state_view, name='api_state'),
    path('api/song/<int:song_id>/lyrics/', views.api_song_lyrics_view, name='api_song_lyrics'),
]

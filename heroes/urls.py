from django.urls import path, include
from heroes.apps import HeroesConfig
from heroes.views import HeroList, HeroDetail, main_view, HeroListView, HeroDetailView, HeroCreateView, HeroUpdateView, \
    HeroDeleteView, HeroStatusListView, HeroStatusDetailView, HeroStatusCreateView, HeroStatusUpdateView, \
    HeroStatusDeleteView

app_name = HeroesConfig.name

urlpatterns = [

    path('', main_view, name='home'),

    path('heroes/', HeroListView.as_view(), name='hero_list'),
    path('heroes/<int:pk>/', HeroDetailView.as_view(), name='hero'),
    path('heroes/create/', HeroCreateView.as_view(), name='hero_create'),
    path('heroes/<int:pk>/update/', HeroUpdateView.as_view(), name='hero_update'),
    path('heroes/<int:pk>/delete/', HeroDeleteView.as_view(), name='hero_delete'),

    path('heroes_status/', HeroStatusListView.as_view(), name='hero_status_list'),
    path('heroes_status/<int:pk>/', HeroStatusDetailView.as_view(), name='hero_status'),
    path('heroes_status/create/', HeroStatusCreateView.as_view(), name='hero_status_create'),
    path('heroes_status/<int:pk>/update/', HeroStatusUpdateView.as_view(), name='hero_status_update'),
    path('heroes_status/<int:pk>/delete/', HeroStatusDeleteView.as_view(), name='hero_status_delete'),
]

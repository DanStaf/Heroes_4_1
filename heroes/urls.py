from django.urls import path, include
from heroes.apps import HeroesConfig
import heroes.views as heroes_views

app_name = HeroesConfig.name

urlpatterns = [

    path('', heroes_views.main_view, name='home'),

    path('heroes/', heroes_views.HeroListView.as_view(), name='hero_list'),
    path('heroes/<int:pk>/', heroes_views.HeroDetailView.as_view(), name='hero'),
    path('heroes/create/', heroes_views.HeroCreateView.as_view(), name='hero_create'),
    path('heroes/<int:pk>/update/', heroes_views.HeroUpdateView.as_view(), name='hero_update'),
    path('heroes/<int:pk>/delete/', heroes_views.HeroDeleteView.as_view(), name='hero_delete'),

    path('heroes_status/', heroes_views.HeroStatusListView.as_view(), name='hero_status_list'),
    path('heroes_status/<int:pk>/', heroes_views.HeroStatusDetailView.as_view(), name='hero_status'),
    path('heroes_status/create/', heroes_views.HeroStatusCreateView.as_view(), name='hero_status_create'),
    path('heroes_status/<int:pk>/update/', heroes_views.HeroStatusUpdateView.as_view(), name='hero_status_update'),
    path('heroes_status/<int:pk>/delete/', heroes_views.HeroStatusDeleteView.as_view(), name='hero_status_delete'),

    path('parents/', heroes_views.ParentListView.as_view(), name='parent_list'),
    path('parents/<int:pk>/', heroes_views.ParentDetailView.as_view(), name='parent'),
    path('parents/create/', heroes_views.ParentCreateView.as_view(), name='parent_create'),
    path('parents/<int:pk>/update/', heroes_views.ParentUpdateView.as_view(), name='parent_update'),
    path('parents/<int:pk>/delete/', heroes_views.ParentDeleteView.as_view(), name='parent_delete'),

    path('parents_status/', heroes_views.ParentStatusListView.as_view(), name='parent_status_list'),
    path('parents_status/<int:pk>/', heroes_views.ParentStatusDetailView.as_view(), name='parent_status'),
    path('parents_status/create/', heroes_views.ParentStatusCreateView.as_view(), name='parent_status_create'),
    path('parents_status/<int:pk>/update/', heroes_views.ParentStatusUpdateView.as_view(), name='parent_status_update'),
    path('parents_status/<int:pk>/delete/', heroes_views.ParentStatusDeleteView.as_view(), name='parent_status_delete'),

]

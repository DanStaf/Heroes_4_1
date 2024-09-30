from django.urls import path, include
from heroes.apps import HeroesConfig
from heroes.views import HeroList, HeroDetail, main_view

app_name = HeroesConfig.name

urlpatterns = [

    path('', main_view, name='home'),

    path('heroes/', HeroList.as_view(), name='hero_list'),
    path('heroes/<int:pk>/', HeroDetail.as_view(), name='hero'),
    #path('heroes/create/', LessonCreateApiView.as_view(), name='lesson_create'),
    #path('heroes/<int:pk>/delete/', LessonDestroyApiView.as_view(), name='lesson_delete'),
    path('heroes/<int:pk>/update/', HeroDetail.as_view(), name='hero_update'),
]

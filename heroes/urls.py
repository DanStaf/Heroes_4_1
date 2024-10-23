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

    path('branches/', heroes_views.BranchListView.as_view(), name='branch_list'),
    path('branches/<int:pk>/', heroes_views.BranchDetailView.as_view(), name='branch'),
    path('branches/create/', heroes_views.BranchCreateView.as_view(), name='branch_create'),
    path('branches/<int:pk>/update/', heroes_views.BranchUpdateView.as_view(), name='branch_update'),
    path('branches/<int:pk>/delete/', heroes_views.BranchDeleteView.as_view(), name='branch_delete'),

    path('teams/', heroes_views.TeamListView.as_view(), name='team_list'),
    path('teams/<int:pk>/', heroes_views.TeamDetailView.as_view(), name='team'),
    path('teams/create/', heroes_views.TeamCreateView.as_view(), name='team_create'),
    path('teams/<int:pk>/update/', heroes_views.TeamUpdateView.as_view(), name='team_update'),
    path('teams/<int:pk>/delete/', heroes_views.TeamDeleteView.as_view(), name='team_delete'),

    path('trainings/', heroes_views.TrainingListView.as_view(), name='training_list'),
    path('trainings/<int:pk>/', heroes_views.TrainingDetailView.as_view(), name='training'),
    path('trainings/create/', heroes_views.TrainingCreateView.as_view(), name='training_create'),
    path('trainings/<int:pk>/update/', heroes_views.TrainingUpdateView.as_view(), name='training_update'),
    path('trainings/<int:pk>/delete/', heroes_views.TrainingDeleteView.as_view(), name='training_delete'),

    path('payment_types/', heroes_views.PaymentTypeListView.as_view(), name='payment_type_list'),
    path('payment_types/<int:pk>/', heroes_views.PaymentTypeDetailView.as_view(), name='payment_type'),
    path('payment_types/create/', heroes_views.PaymentTypeCreateView.as_view(), name='payment_type_create'),
    path('payment_types/<int:pk>/update/', heroes_views.PaymentTypeUpdateView.as_view(), name='payment_type_update'),
    path('payment_types/<int:pk>/delete/', heroes_views.PaymentTypeDeleteView.as_view(), name='payment_type_delete'),

    path('payments/', heroes_views.PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', heroes_views.PaymentDetailView.as_view(), name='payment'),
    path('payments/create/', heroes_views.PaymentCreateView.as_view(), name='payment_create'),
    path('payments/<int:pk>/update/', heroes_views.PaymentUpdateView.as_view(), name='payment_update'),
    path('payments/<int:pk>/delete/', heroes_views.PaymentDeleteView.as_view(), name='payment_delete'),

]

from rest_framework import routers
from django.urls import path
# from users.views import UserViewSet

from users.views import UserResetPasswordView, RegisterView, UserDeleteView, UserProfileView, UserListView, \
    user_change_active, UserChangePasswordView
from users.apps import UsersConfig

from django.contrib.auth.views import LoginView, LogoutView

"""from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)"""

app_name = UsersConfig.name

# router_user = routers.DefaultRouter()
# router_user.register("", UserViewSet, basename='user')
"""
example:
prefix="users"
URL pattern: ^users/$ Name: 'user-list'
URL pattern: ^users/{pk}/$ Name: 'user-detail'
"""

urlpatterns = [

    # path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    # path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),

    # path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('password_reset/', UserResetPasswordView.as_view(), name='password_reset'),

    path('register/', RegisterView.as_view(), name='register'),
    # path('email_confirm/<str:token>/', email_verification, name='email_confirm'),
    path('delete/', UserDeleteView.as_view(), name='user_delete'),

    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', UserResetPasswordView.as_view(), name='password_reset'),

    path('password_change/', UserChangePasswordView.as_view(), name='password_change'),

    path('', UserListView.as_view(), name='user-list'),
    path('change_active/<int:pk>/', user_change_active, name='change_active'),

]

# urlpatterns += router_user.urls

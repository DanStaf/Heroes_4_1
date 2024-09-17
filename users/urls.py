from rest_framework import routers
from django.urls import path

from users.views import UserViewSet
from users.apps import UsersConfig

"""from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)"""

app_name = UsersConfig.name

router_user = routers.DefaultRouter()
router_user.register("", UserViewSet, basename='user')

urlpatterns = [

    # path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    # path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),

]

urlpatterns += router_user.urls

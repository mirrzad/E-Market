from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

app_name = 'account_api'

router = routers.SimpleRouter()
router.register('user', views.UserViewSet, basename='User')

urlpatterns = [
    path('register/', views.RegisterApiView.as_view(), name='register-api'),
    path('api_token_auth/', ObtainAuthToken.as_view(), name='token_auth_api'),
    path('api_token_auth/delete/', views.DeleteAuthTokenView.as_view(), name='token_auth_delete_api'),

    path('token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns += router.urls

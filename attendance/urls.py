from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/me/', views.MeView.as_view(), name='me'),
    path('login/', views.TokenObtainPairWithRoleView.as_view(), name='token_obtain_pair'),
    path('user-list/', views.GetUserList.as_view(), name='get_user_list'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]

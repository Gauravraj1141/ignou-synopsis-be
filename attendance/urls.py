from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/me/', views.MeView.as_view(), name='me'),
    path('login/', views.TokenObtainPairWithRoleView.as_view(), name='token_obtain_pair'),
    path('user-list/', views.GetUserList.as_view(), name='get_user_list'),
    path('update-status/', views.UpdateUserStatusAPIView.as_view()),
    path('register-face/', views.RegisterFaceAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('mark-attendance/', views.MarkAttendanceApiView.as_view()),
    path('attendance/report/', views.AttendanceReportAPIView.as_view()),
    path('admin/attendance/', views.AdminAttendanceReportAPIView.as_view()),
    path('users/<uuid:user_id>/delete/', views.DeleteUserAPIView.as_view()),
]

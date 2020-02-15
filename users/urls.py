from django.contrib.auth import views as auth_views
from django.urls import path
from.views import (
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    UserUpdateView,
    UserPasswordChangeView,
    UserPasswordChangeDoneView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView,
    users_activate,
    validate_email,
    validate_username,
)

urlpatterns = [
    path('', UserLoginView.as_view(), name='users-login'),
    path('login/', UserLoginView.as_view(), name='users-login'),
    path('logout/', UserLogoutView.as_view(), name='users-logout'),
    path('register/', UserRegisterView.as_view(), name='users-register'),
    path('activate/<uidb64>/<token>/', users_activate, name='users-activate'),
    path('<slug:slug>/', UserUpdateView.as_view(), name='users-profile'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password-change'),
    path('password-change/done/', UserPasswordChangeDoneView.as_view(), name='password-change-done'),
    path('password-reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', UserPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
    path('password_reset/complete/', UserPasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('ajax/validate_email/', validate_email, name='validate-email'),
    path('ajax/validate_username/', validate_username, name='validate-username'),
]

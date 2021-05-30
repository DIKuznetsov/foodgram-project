from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/',
         auth_views.LoginView.as_view(template_name='users/authForm.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='users/changePassword.html',
        success_url=reverse_lazy('users/password_change_done')),
        name='change_password'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view()),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/resetPassword.html'), name='reset_password'),
    path(r'', include('django.contrib.auth.urls')),
]

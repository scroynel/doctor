from django.urls import path, reverse_lazy

from .views import LoginUser, ProfileUser, RegisterUser, UserPasswordChangeView
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import UserPasswordResetForm, UserSetPasswordFrom

app_name = 'users'

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name = 'users/password_change_done.html'), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(
        template_name = 'users/password_reset_form.html',
        form_class = UserPasswordResetForm,
        email_template_name = 'users/password_reset_email.html',
        success_url = reverse_lazy('users:password_reset_done')
    ), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name = 'users/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name = 'users/password_reset_confirm.html',
        form_class = UserSetPasswordFrom,
        success_url = reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name = 'users/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('profile/<int:pk>/', ProfileUser.as_view(), name='profile'),
    # path('profile/edit/<slug:edit_profile>/', ProfileUser.as_view(), name='profile_edit'),
]
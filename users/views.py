from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, UserLocation, UserActivation
from django.utils import timezone
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
)


def get_user_location(request):
    """
    This function captures the user's IP Address, User-Agent, Country and City
    """
    values = {}

    # Get IP Address of user
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""

    # Get User Agent of user
    try:
        user_agent = request.META.get("HTTP_USER_AGENT")
    except:
        user_agent = ""

    # Trace user location using Geoip API
    from django.contrib.gis.geoip2 import GeoIP2
    g = GeoIP2()

    # Get Country of user
    try:
        country = g.country_name(ip)
    except:
        country = ""

    # Get City of user
    try:
        city = g.city(ip)['city']
    except:
        city = ""

    values['ip'] = ip
    values['user_agent'] = user_agent
    values['country'] = country
    values['city'] = city

    return values


# Enabling login for user
class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/users_login.html'
    success_message = "Welcome! You were successfully logged in."


# Enabling logout for user
class UserLogoutView(LogoutView):
    template_name = 'users/users_logout.html'


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = CustomUser
    template_name = 'users/users_register_modal.html'
    form_class = CustomUserCreationForm
    success_message = "An email has been sent to '%(email)s' for verification. " \
                      "Your account will be activated once email verification is completed."
    success_url = reverse_lazy('users-login')

    def form_valid(self, form):
        user = form.save(commit=False)
        # Ensure user is not active to prevent from accessing the site till
        # email verification is completed
        is_active = False
        # Save user data to database
        user.save()

        # Update User Activation tracking details
        UserActivation.objects.get_or_create(
            user=user,
            # Set email verification deadline as 7 days from registration date
            activation_deadline=timezone.now() + timezone.timedelta(days=7),
            # Set sent email flag to True
            email_sent=True,
            created_date=timezone.now(),
            activation_date=None
        )

        # Capture User location details
        UserLocation.objects.get_or_create(
            user=user,
            ip=get_user_location(self.request)['ip'],
            user_agent=get_user_location(self.request)['user_agent'],
            country=get_user_location(self.request)['country'],
            city=get_user_location(self.request)['city']
        )

        # Prepare email notification details
        subject = f"LordSipraSays | Activate Your Account | {form.cleaned_data['email']}"
        to = form.cleaned_data['email']
        from_email = settings.EMAIL_HOST_USER
        body = render_to_string(
            'users/account_activation_email.html', {
                'user': user,
                'domain': self.request.get_host,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
        )

        # Send email to registered user
        send_email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to],
        )
        
        send_email.content_subtype = "html"
        send_email.send(fail_silently=False)

        return super().form_valid(form)


def users_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        token = default_token_generator.make_token(user)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.validation_token = f"{uidb64} : {token}"
        user.is_active = True

        UserActivation.objects.select_related('user').filter(user=user).update(activation_date=timezone.now())

        user.save()

        messages.success(request, "Your email has been verified successfully! Please login to access the website.")
        return redirect('users-login')
    else:
        messages.error(request, "Your email could not be verified. Please contact the site Admin.")
        return render(request, 'users/users_login.html')


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = 'users/users_profile.html'
    form_class = CustomUserChangeForm
    success_message = "Profile updated successfully."

    def get_queryset(self):
        return CustomUser.objects.filter(username=self.request.user)


@login_required
def password_change(request):
    from django.contrib.auth import update_session_auth_hash

    form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('blog-home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {
        "form": form,
    }
    return render(request, "users/password_change_form.html", context)


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password-change-done')


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
    # success_url = reverse_lazy('blog-home')


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password-reset-done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password-reset-complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


def validate_email(request):
    email = request.GET.get('email')
    data = {
        'status': 200,
        'is_taken': CustomUser.objects.filter(email__iexact=email).only('email').exists()
    }
    return JsonResponse(data)


def validate_username(request):
    username = request.GET.get('username')
    data = {
        'status': 200,
        'is_taken': CustomUser.objects.filter(username__iexact=username).only('username').exists()
    }
    return JsonResponse(data)

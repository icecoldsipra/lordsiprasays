from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserLocation, LoggedInUser


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm  # To update user details
    add_form = CustomUserCreationForm  # To create new user

    list_display = ('username', 'pk', 'email', 'slug', 'first_name', 'last_name', 'country', 'date_joined', 'email_sent',
                    'activation_deadline', 'activation_date', 'ip_address', 'user_agent', 'last_login', 'is_active',
                    'is_staff', 'is_superuser')

    list_filter = ('is_active', 'is_staff', 'is_superuser')

    # Break down how various fields appear in the Admin panel
    fieldsets = (
        (None, {'fields': ('username', 'email', 'slug', 'ip_address', 'user_agent', 'date_joined', 'last_login')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # To enable signup-like form in admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name', 'country')  # Add search bar in Admin panel
    ordering = ['-date_joined']  # Sort in descending order
    filter_horizontal = ()


# Reference the CustomUser model as User
User = get_user_model()


class UserLocationAdmin(admin.ModelAdmin):
    class Meta:
        model = UserLocation

    list_display = ['user', 'ip', 'user_agent', 'country', 'timestamp']
    # list_filter = ['tag']
    # search_fields = ['tag']  # Add search bar in Admin panel
    readonly_fields = ['ip', 'user_agent', 'country', 'timestamp']
    # prepopulated_fields = {'slug': ('title', )} # Automatically updates 'slug' field based on title
    ordering = ['-timestamp']  # Sort in descending order


class LoggedInUserAdmin(admin.ModelAdmin):
    class Meta:
        model = LoggedInUser

    list_display = ['user', 'session_key', 'timestamp']
    # list_filter = ['tag']
    # search_fields = ['tag']  # Add search bar in Admin panel
    readonly_fields = ['session_key', 'timestamp']
    # prepopulated_fields = {'slug': ('title', )} # Automatically updates 'slug' field based on title
    ordering = ['-timestamp']  # Sort in descending order


# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserLocation, UserLocationAdmin)
admin.site.register(LoggedInUser, LoggedInUserAdmin)

admin.site.site_header = "Blog Manager"
admin.site.site_title = "Blog Manager Portal"
admin.site.index_title = "Welcome to Blog Manager Portal!"

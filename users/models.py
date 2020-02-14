from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    nickname = models.CharField("Nickname", unique=True, max_length=25, help_text="Enter a nickname")
    email = models.EmailField("Email", unique=True, max_length=100, help_text="Enter Valid Email ID")
    first_name = models.CharField("First Name", max_length=255, help_text="Enter Your First Name")
    last_name = models.CharField("Last Name", max_length=255, blank=True, default='', help_text="Enter Your Last Name")
    slug = models.SlugField("Slug", unique=True, max_length=255, default='')
    country = models.CharField("Country", max_length=100, blank=True, default='')
    ip_address = models.CharField("IP Address", max_length=35, blank=True, default='')
    user_agent = models.CharField("User Agent", max_length=255, blank=True, default='')
    image = models.ImageField("Image", upload_to='users', default='default.png', blank=True,
                              help_text="Upload Your Profile Pic")
    email_sent = models.BooleanField("Email Sent", blank=True, null=True, default=False)
    activation_deadline = models.DateTimeField("Activation Deadline", blank=True, null=True, default=None)
    activation_date = models.DateTimeField("Activation Date", blank=True, null=True, default=None)
    is_active = models.BooleanField("Is Active", default=True)  # Can login
    is_staff = models.BooleanField("Is Staff", default=False)  # Admin but non-superuser
    is_superuser = models.BooleanField("Is Superuser", default=False)  # Superuser
    date_joined = models.DateTimeField("Date Joined", auto_now_add=True)  # Sets value to current date and time

    class Meta:
        verbose_name = 'Registered User'
        verbose_name_plural = 'Registered Users'

    # Username and password are required by default
    # set email as the default username for authentication
    USERNAME_FIELD = 'nickname'
    # Can add additional fields which will be asked during superuser creation
    # These fields should also be included in the create_user() function in CustomUserManager class
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager()

    # def __str__(self):
    #    return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        else:
            return self.first_name

    def get_short_name(self):
        if self.first_name:
            return self.first_name
    
    def get_nickname(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        # Simplest possible answer: Yes, always
        return self.is_staff

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        # Simplest possible answer: Yes, always
        return self.is_staff

    def get_absolute_url(self):
        return reverse('users-profile', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        slug = slugify(self.get_full_name())
        unique_slug = slug
        num = 1
        while CustomUser.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class UserLocation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ip = models.CharField("IP Address", max_length=20, blank=True, default='')
    user_agent = models.CharField("User Agent", max_length=255, blank=True, default='')
    country = models.CharField("Country", max_length=50, blank=True, default='')
    city = models.CharField("City", max_length=50, blank=True, default='')
    timestamp = models.DateTimeField("Timestamp", auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.ip}"


# Model to store the list of logged in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='logged_in_user')
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

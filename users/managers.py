from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    # Specify all the required fields here
    def create_user(self, nickname, email, first_name, last_name, password, is_active=True, is_staff=False, is_superuser=False,
                    **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        # Raise exception if user does not have an email
        if not email:
            raise ValueError("Users must provide an email address.")
        # Raise exception if user does not have a password
        if not nickname:
            raise ValueError("Users must enter a nickname.")
        # Raise exception if user does not have a password
        if not password:
            raise ValueError("Users must enter a password.")
        # Raise exception if user does not enter a first name
        if not first_name:
            raise ValueError("Users must provide first name.")

        user = self.model(
            nickname=nickname,
            email=self.normalize_email(email),  # Converts all characters of email field to lower cases
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields

        )

        user.set_password(password)  # Change user password
        user.save(using=self._db)
        return user

    def create_staffuser(self, nickname, email, first_name, last_name, password, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """

        user = self.create_user(
            nickname=nickname,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_active=True,
            is_staff=True,
            is_superuser=False
        )
        return user

    def create_superuser(self, nickname, email, first_name, last_name, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """

        user = self.create_user(
            nickname=nickname,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        return user

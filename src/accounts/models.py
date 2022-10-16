import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("Email address"), null=True, unique=True)
    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Account creation date")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("custom_user")
        verbose_name_plural = _("custom_users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self):
        return str(self.email)


class Profile(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, primary_key=True)
    phone_number = PhoneNumberField(_("Phone number"), blank=True, null=True, help_text="Contact phone number")
    date_created = models.DateTimeField(auto_now=True, null=True, editable=False, verbose_name="Modified date")
    photo = models.ImageField(
        default="profiles_avatars/empty_avatar.png",
        null=True,
        blank=True,
        upload_to="profiles_avatars/%Y/%m/%d/",
        verbose_name="Avatar",
    )
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address")

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    part = models.ForeignKey(to="catalogue.Part", related_name="comment", on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)

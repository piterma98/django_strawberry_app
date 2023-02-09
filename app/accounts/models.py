from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.mixins import BaseModel


class CustomUser(BaseModel, AbstractUser):
    """CustomUser model."""

    email = models.EmailField(
        _("email address"), unique=True, validators=[validate_email]
    )

    def __str__(self) -> str:
        return self.email

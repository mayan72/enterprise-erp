from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN"
        NORMAL_USER = "NORMAL_USER"

    role = models.CharField(max_length=20, choices=Roles.choices)

    def is_super_admin(self):
        return self.role == self.Roles.SUPER_ADMIN

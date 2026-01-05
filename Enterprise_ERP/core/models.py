from django.db import models

class ERPModule(models.Model):
    code = models.CharField(max_length=50, unique=True)   # medical, electronics, grocery
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default="layers")
    is_legacy = models.BooleanField(default=False)
    legacy_app_label = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

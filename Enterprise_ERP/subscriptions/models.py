from django.conf import settings
from django.db import models
from django.utils import timezone


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    #IMPORTANT: use STRING reference with app label
    erp_module = models.ForeignKey(
        "subscriptions.ErpModule",
        on_delete=models.PROTECT,
        related_name="subscriptions"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    # ✅ ADD THIS
    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE


class ErpModule(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    url_namespace = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True) 

    is_active = models.BooleanField(default=True)

    #TEMPORARY DEFAULT
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
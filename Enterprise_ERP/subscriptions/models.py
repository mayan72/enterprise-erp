from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"

    class Plan(models.TextChoices):
        ONE_MONTH = "1M", "1 Month"
        THREE_MONTHS = "3M", "3 Months"
        ONE_YEAR = "1Y", "1 Year"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    erp_module = models.ForeignKey(
        "core.ERPModule",
        on_delete=models.PROTECT,
        related_name="subscriptions"
    )

    plan = models.CharField(
        max_length=2,
        choices=Plan.choices,
        default=Plan.THREE_MONTHS   
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE and (
            self.expires_at is None or self.expires_at >= timezone.now()
        )

    def set_expiry_from_plan(self):
        now = timezone.now()

        if self.plan == self.Plan.ONE_MONTH:
            self.expires_at = now + timedelta(days=30)
        elif self.plan == self.Plan.THREE_MONTHS:
            self.expires_at = now + timedelta(days=90)
        elif self.plan == self.Plan.ONE_YEAR:
            self.expires_at = now + timedelta(days=365)



class ERPModule(models.Model):
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
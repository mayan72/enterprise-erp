from django.db import models
# from subscriptions.models import Tenant
from accounts.models import User


# class Medicine(models.Model):
#     tenant = models.ForeignKey(
#         Tenant,
#         on_delete=models.CASCADE,
#         related_name="medicines"
#     )

#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     stock = models.IntegerField(default=0)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     created_by = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="medicines_created"
#     )

#     updated_by = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="medicines_updated"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["name"]
#         unique_together = ("tenant", "name")  # Prevent same medicine name inside same tenant

#     def __str__(self):
#         return f"{self.name} ({self.tenant.name})"


class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

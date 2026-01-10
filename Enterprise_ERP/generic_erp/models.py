from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# class BulkUploadRecord(models.Model):
#     UPLOAD_TYPES = (
#         ("products", "Products"),
#         ("stock", "Stock"),
#         ("billing", "Billing"),
#     )

#     tenant_id = models.CharField(max_length=50)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     erp_code = models.CharField(max_length=50)
#     upload_type = models.CharField(max_length=20, choices=UPLOAD_TYPES)

#     business_date = models.DateField(null=True, blank=True)

#     row_data = models.JSONField()
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=["tenant_id", "user", "erp_code"]),
#             models.Index(fields=["upload_type"]),
#             models.Index(fields=["business_date"]),
#         ]

#     def __str__(self):
#         return f"{self.erp_code} | {self.upload_type} | {self.uploaded_at}"



from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BulkUploadRecord(models.Model):
    tenant_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    erp_code = models.CharField(max_length=50)
    upload_type = models.CharField(max_length=20)

    business_date = models.DateField(null=True, blank=True)

    # ✅ NUMERIC FIELD FOR BILLING (VERY IMPORTANT)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    # ✅ ALWAYS JSON
    row_data = models.JSONField(default=dict)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.erp_code} | {self.upload_type} | {self.uploaded_at}"



class DailySalesSummary(models.Model):
    tenant_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    erp_code = models.CharField(max_length=50)
    sale_date = models.DateField()

    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    class Meta:
        unique_together = ("tenant_id", "user", "erp_code", "sale_date")

    def __str__(self):
        return f"{self.sale_date} - {self.total_amount}"

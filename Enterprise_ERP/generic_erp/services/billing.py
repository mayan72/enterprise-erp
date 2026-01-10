from django.db.models import Sum
from generic_erp.models import BulkUploadRecord, DailySalesSummary


def update_daily_summary(tenant_id, request, erp_code, sale_date):
    total = (
        BulkUploadRecord.objects
        .filter(
            tenant_id=tenant_id,
            # user=user,
            user=request.effective_user,
            erp_code=erp_code,
            upload_type="billing",
            business_date=sale_date
        )
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    DailySalesSummary.objects.update_or_create(
        tenant_id=tenant_id,
        # user=user,
        user=request.effective_user,
        erp_code=erp_code,
        sale_date=sale_date,
        defaults={"total_amount": total}
    )

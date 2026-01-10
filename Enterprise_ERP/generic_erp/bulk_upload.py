import pandas as pd
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from core.mixins import (
    TenantContextMixin,
    ModuleAccessRequiredMixin,
    UserDataMixin,
)
from core.models import ERPModule
from generic_erp.models import BulkUploadRecord
from generic_erp.services.billing import update_daily_summary


class BulkUploadView(
    TenantContextMixin,
    ModuleAccessRequiredMixin,
    UserDataMixin,
    View
):
    template_name = "generic_erp/upload_page.html"

    def dispatch(self, request, *args, **kwargs):
        # ✅ REQUIRED FOR ModuleAccessRequiredMixin
        self.module_code = kwargs.get("erp_code")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, erp_code, upload_type):
        erp = get_object_or_404(
            ERPModule,
            code=erp_code,
            is_active=True
        )

        records = BulkUploadRecord.objects.filter(
            tenant_id=request.tenant.id,
            # user=request.user,
            user=request.effective_user,
            erp_code=erp.code,
            upload_type=upload_type
        ).order_by("-uploaded_at")[:50]

        return render(
            request,
            self.template_name,
            {
                "erp": erp,
                "upload_type": upload_type,
                "records": records,
            }
        )

    def post(self, request, erp_code, upload_type):
        erp = get_object_or_404(
            ERPModule,
            code=erp_code,
            is_active=True
        )

        file = request.FILES["file"]
        business_date = request.POST.get("business_date")

        df = pd.read_excel(file)

        records = []

        for _, row in df.iterrows():
            row_dict = row.to_dict()

            # ✅ HARD SAFETY: row_data MUST be dict
            if not isinstance(row_dict, dict):
                row_dict = {}

            amount_value = None

            # ✅ Extract Amount ONLY for billing
            if upload_type == "billing":
                raw_amount = row_dict.get("Amount")
                try:
                    amount_value = float(raw_amount) if raw_amount is not None else 0
                except (TypeError, ValueError):
                    amount_value = 0

            records.append(
                BulkUploadRecord(
                    tenant_id=request.tenant.id,
                    # user=request.user,
                    user=request.effective_user,
                    erp_code=erp.code,
                    upload_type=upload_type,
                    business_date=business_date,
                    amount=amount_value,
                    row_data=row_dict
                )
            )

        BulkUploadRecord.objects.bulk_create(records)

        # ✅ SAFE AGGREGATION (NO JSON TOUCH)
        if upload_type == "billing":
            update_daily_summary(
                request.tenant.id,
                request.user,
                erp.code,
                business_date
            )

        return redirect(
            "generic_erp:bulk-upload",
            erp_code=erp.code,
            upload_type=upload_type
        )

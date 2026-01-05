from django.views.generic import TemplateView
from subscriptions.models import Subscription
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from subscriptions.models import Subscription
from django.views import View
from core.models import ERPModule
from core.utils import get_effective_user


class DashboardView(TemplateView):
    template_name = "core/dashboard.html"

    def get(self, request, *args, **kwargs):
        user = get_effective_user(request)

        if not user.is_authenticated:
            return redirect("accounts:login")

        # REAL super admin (not viewing as user)
        if (
            request.user.is_super_admin()
            and user == request.user
        ):
            return redirect("core:admin_dashboard")

        # USER DASHBOARD (normal OR viewed-as)
        try:
            subscription = user.subscription
        except Subscription.DoesNotExist:
            return redirect("core:no_subscription")

        if not subscription.is_active:
            return redirect("core:no_subscription")

        erp = subscription.erp_module

        # LEGACY ERP
        if erp.is_legacy:
            return redirect(f"{erp.legacy_app_label}:home")

        # GENERIC ERP
        return redirect("generic_erp:home", erp_code=erp.code)


class ERPDispatcherView(View):
    def get(self, request, erp_code):
        erp = get_object_or_404(
            ERPModule,
            code=erp_code,
            is_active=True   # ✅ FIXED
        )

        # OLD ERP
        if erp.is_legacy:
            return redirect(f"/{erp.legacy_app_label}/")

        # NEW ERP
        # return redirect("generic-erp-home", erp_code=erp.code)
        return redirect("generic_erp:home", erp_code=erp.code)

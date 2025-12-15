from django.views.generic import TemplateView
from subscriptions.models import Subscription
from django.shortcuts import redirect
from django.views.generic import TemplateView
from subscriptions.models import Subscription


class DashboardView(TemplateView):
    template_name = "core/dashboard.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect("accounts:login")

        # SUPER ADMIN → NEW ADMIN UI
        if user.is_super_admin():
            return redirect("core:admin_dashboard")

        # NORMAL USER → ERP
        try:
            subscription = user.subscription
        except Subscription.DoesNotExist:
            return redirect("accounts:login")

        if not subscription.is_active:
            # return redirect("accounts:login")
            return redirect("core:no_subscription")

        return redirect(f"{subscription.erp_module.url_namespace}:home")


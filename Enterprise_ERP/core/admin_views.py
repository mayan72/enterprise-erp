from django.views.generic import TemplateView, ListView, FormView
from django.urls import reverse_lazy
from django.db import transaction

from accounts.models import User
from subscriptions.models import Subscription
from core.forms import AdminUserCreateForm
from core.mixins import SuperAdminRequiredMixin
from subscriptions.models import ErpModule
from core.forms import ErpModuleCreateForm
from django.views.generic import CreateView, ListView



class AdminDashboardView(SuperAdminRequiredMixin, TemplateView):
    template_name = "core/admin/dashboard.html"


class AdminUserListView(SuperAdminRequiredMixin, ListView):
    template_name = "core/admin/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return (
            User.objects
            .select_related("subscription__erp_module")
            .order_by("-id")
        )

from django.db import transaction
from accounts.models import User
from subscriptions.models import Subscription


class AdminUserCreateView(SuperAdminRequiredMixin, FormView):
    template_name = "core/admin/user_create.html"
    form_class = AdminUserCreateForm
    success_url = reverse_lazy("core:admin_user_list")

    @transaction.atomic
    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
            role=User.Roles.NORMAL_USER,
            is_active=form.cleaned_data["is_active"],
        )

        Subscription.objects.create(
            user=user,
            erp_module=form.cleaned_data["erp_module"],
            status=Subscription.Status.ACTIVE,
        )

        return super().form_valid(form)

from django.views.generic import UpdateView
from subscriptions.models import Subscription


class AdminUserSubscriptionUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = Subscription
    fields = ["erp_module", "status"]
    template_name = "core/admin/subscription_edit.html"
    success_url = reverse_lazy("core:admin_user_list")

class ErpModuleCreateView(SuperAdminRequiredMixin, CreateView):
    model = ErpModule
    form_class = ErpModuleCreateForm
    template_name = "core/admin/erp_create.html"
    success_url = reverse_lazy("core:admin_erp_list")


from django.views.generic import ListView, View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from core.mixins import SuperAdminRequiredMixin
from subscriptions.models import ErpModule


class ErpModuleListView(SuperAdminRequiredMixin, ListView):
    model = ErpModule
    template_name = "core/admin/erp_list.html"
    context_object_name = "modules"


class ToggleErpStatusView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        erp = get_object_or_404(ErpModule, pk=pk)
        erp.is_active = not erp.is_active
        erp.save(update_fields=["is_active"])
        return redirect("core:admin_erp_list")

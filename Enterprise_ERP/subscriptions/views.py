from django.views.generic import ListView, CreateView, UpdateView
# from django.urls import reverse_lazy
# from core.mixins import RoleRequiredMixin
from .models import ERPModule

# class ErpModuleListView(RoleRequiredMixin, ListView):
#     model = ERPModule
#     template_name = "subscriptions/erp_module_list.html"
#     required_roles = ("SUPER_ADMIN",)


# class ErpModuleCreateView(RoleRequiredMixin, CreateView):
#     model = ERPModule
#     fields = ["code", "name", "description", "app_label", "url_namespace", "is_active"]
#     template_name = "subscriptions/erp_module_form.html"
#     success_url = reverse_lazy("subscriptions:erp_module_list")
#     required_roles = ("SUPER_ADMIN",)

#     def form_valid(self, form):
#         try:
#             return super().form_valid(form)
#         except Exception as exc:
#             # Wrap error for clean UX and log if required
#             form.add_error(None, "Could not create ERP module. Contact support.")
#             return self.form_invalid(form)


class ErpModuleCreateView(CreateView):
    model = ERPModule
    fields = ["code", "name", "description", "app_label", "url_namespace", "is_active"]
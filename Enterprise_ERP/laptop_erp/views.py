from django.views.generic import TemplateView
from core.mixins import ModuleAccessRequiredMixin

class LaptopHomeView(ModuleAccessRequiredMixin, TemplateView):
    template_name = "laptop_erp/home.html"
    required_roles = ("TENANT_USER", "SUPER_ADMIN")
    module_code = "laptop"

from django.views.generic import TemplateView
from core.mixins import ModuleAccessRequiredMixin

class JewelleryHomeView(ModuleAccessRequiredMixin, TemplateView):
    template_name = "jewellery_erp/home.html"
    required_roles = ("TENANT_USER", "SUPER_ADMIN")
    module_code = "jewellery"

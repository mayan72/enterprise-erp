from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from core.mixins import UserDataMixin
from core.models import ERPModule

class GenericERPHomeView(UserDataMixin, TemplateView):
    template_name = "generic_erp/home.html"

    def dispatch(self, request, *args, **kwargs):
        self.erp = get_object_or_404(
            ERPModule,
            code=kwargs["erp_code"],
            is_active=True,
            is_legacy=False
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["erp"] = self.erp
        return context

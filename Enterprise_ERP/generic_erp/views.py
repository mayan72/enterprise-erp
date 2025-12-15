from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from core.mixins import UserDataMixin

# Create your views here.
class GenericERPHomeView(UserDataMixin, TemplateView):
    template_name = "generic_erp/home.html"

    def dispatch(self, request, *args, **kwargs):
        self.erp = get_object_or_404(
            ERPModule,
            code=kwargs["erp_code"],
            active=True
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["erp"] = self.erp
        return context

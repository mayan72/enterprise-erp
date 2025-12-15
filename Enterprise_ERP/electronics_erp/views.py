from django.views.generic import ListView, TemplateView
from core.mixins import UserDataMixin
from .models import Electronics


class ElectronicsHomeView(TemplateView):
    template_name = "electronics_erp/home.html"
    module_code = "electronics"


class ElectronicsListView(UserDataMixin, ListView):
    model = Electronics
    template_name = "electronics_erp/electronics_list.html"
    context_object_name = "object_list"

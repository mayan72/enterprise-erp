from django.views.generic import ListView, TemplateView
from core.mixins import ModuleAccessRequiredMixin, UserDataMixin
from .models import Medicine



class MedicalHomeView(ModuleAccessRequiredMixin, TemplateView):
    template_name = "medical_erp/home.html"
    module_code = "medical"


# class MedicineListView(ModuleAccessRequiredMixin, TenantDataMixin, ListView):
#     model = Medicine
#     template_name = "medical_erp/medicine_list.html"
#     module_code = "medical"


# class MedicineListView(UserDataMixin, ListView):
#     model = Medicine

class MedicineListView(ModuleAccessRequiredMixin, UserDataMixin, ListView):
    model = Medicine
    template_name = "medical_erp/medicine_list.html"
    module_code = "medical"



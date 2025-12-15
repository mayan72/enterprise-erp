from django.urls import path
from .views import MedicalHomeView, MedicineListView

app_name = "medical_erp"

urlpatterns = [
    path("", MedicalHomeView.as_view(), name="home"),
    path("medicines/", MedicineListView.as_view(), name="medicine_list"),
]

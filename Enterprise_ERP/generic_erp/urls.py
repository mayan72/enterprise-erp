from django.urls import path
from .views import GenericERPHomeView

app_name = "generic_erp"

urlpatterns = [
    path("<str:erp_code>/", GenericERPHomeView.as_view(), name="home"),
]

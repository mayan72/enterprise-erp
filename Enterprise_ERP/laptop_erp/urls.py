from django.urls import path
from .views import LaptopHomeView

app_name = "laptop_erp"

urlpatterns = [
    path("", LaptopHomeView.as_view(), name="home"),
]

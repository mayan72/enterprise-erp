from django.urls import path
from .views import ElectronicsHomeView, ElectronicsListView

app_name = "electronics_erp"

urlpatterns = [
    path("", ElectronicsHomeView.as_view(), name="home"),
    path("list/", ElectronicsListView.as_view(), name="electronics_list"),
]

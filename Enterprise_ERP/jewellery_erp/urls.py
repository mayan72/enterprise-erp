from django.urls import path
from .views import JewelleryHomeView

app_name = "jewellery_erp"

urlpatterns = [
    path("", JewelleryHomeView.as_view(), name="home"),
]

from django.urls import path
from .views import GenericERPHomeView
from .bulk_upload import BulkUploadView

app_name = "generic_erp"

urlpatterns = [
    path("<str:erp_code>/", GenericERPHomeView.as_view(), name="home"),
    path(
        "<str:erp_code>/upload/<str:upload_type>/",
        BulkUploadView.as_view(),
        name="bulk-upload"
    ),

]



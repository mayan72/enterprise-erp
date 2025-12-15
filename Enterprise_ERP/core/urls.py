from django.urls import path
from core.admin_views import (
    AdminDashboardView,
    AdminUserListView,
    AdminUserCreateView,
    ToggleErpStatusView,
)

app_name = "core"

urlpatterns = [
    path("admin/dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("admin/users/", AdminUserListView.as_view(), name="admin_user_list"),
    path("admin/users/create/", AdminUserCreateView.as_view(), name="admin_user_create"),
]


from core.admin_views import (
    ErpModuleCreateView,
    ErpModuleListView,
)

urlpatterns += [
    # path("admin/erps/", ErpModuleListView.as_view(), name="admin_erp_list"),
    path("admin/erps/create/", ErpModuleCreateView.as_view(), name="admin_erp_create"),
    
    path("admin/erps/", ErpModuleListView.as_view(), name="admin_erp_list"),
    path("admin/erps/<int:pk>/toggle/", ToggleErpStatusView.as_view(), name="admin_erp_toggle"),
]



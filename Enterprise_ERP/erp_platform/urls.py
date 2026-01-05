"""
URL configuration for erp_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.urls import path, include

# urlpatterns = [
#     path("accounts/", include("accounts.urls", namespace="accounts")),
#     path("", include("core.urls", namespace="core")),  # dashboard, landing

#     # ERP modules as tabs, each with its own URL namespace
#     path("medical/", include("medical_erp.urls", namespace="medical_erp")),
#     path("electronics/", include("electronics_erp.urls", namespace="electronics_erp")),
#     path("jewellery/", include("jewellery_erp.urls", namespace="jewellery_erp")),
#     path("laptop/", include("laptop_erp.urls", namespace="laptop_erp")),
# ]

from django.contrib import admin
from django.urls import path, include
from core.views import DashboardView, ERPDispatcherView

urlpatterns = [
    path("", DashboardView.as_view(), name="root_dashboard"),

    path("accounts/", include("accounts.urls")),

    path("medical/", include("medical_erp.urls")),
    path("electronics/", include("electronics_erp.urls")),

    path("", include("core.urls")),  # super admin urls
    path("erp/<str:erp_code>/", ERPDispatcherView.as_view(), name="erp-dispatch"),
    path("generic/", include("generic_erp.urls")),
]

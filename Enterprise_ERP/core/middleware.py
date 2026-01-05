# from django.core.exceptions import PermissionDenied
# from subscriptions.models import Subscription

# class ModuleAccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if not request.user.is_authenticated:
#             return self.get_response(request)

#         if request.user.is_super_admin():
#             return self.get_response(request)

#         try:
#             subscription = request.user.subscription
#         except Subscription.DoesNotExist:
#             raise PermissionDenied("No subscription")

#         if not subscription.erp_module.is_active:
#             raise PermissionDenied("ERP module is inactive")

#         return self.get_response(request)

# from django.core.exceptions import PermissionDenied


# class ModuleAccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if not request.user.is_authenticated:
#             return self.get_response(request)

#         if request.path.startswith(("/admin/", "/accounts/", "/static/")):
#             return self.get_response(request)

#         if hasattr(request.user, "is_super_admin") and request.user.is_super_admin():
#             return self.get_response(request)

#         # Lazy import (safe)
#         from subscriptions.models import Subscription

#         try:
#             subscription = Subscription.objects.select_related(
#                 "erp_module"
#             ).get(user=request.user)
#         except Subscription.DoesNotExist:
#             raise PermissionDenied("No active subscription")

#         # ✅ FIXED FIELD NAME
#         if not subscription.erp_module.is_active:
#             raise PermissionDenied("ERP module is inactive")

#         return self.get_response(request)


from django.core.exceptions import PermissionDenied


class ModuleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # 1. Allow unauthenticated users
        if not request.user.is_authenticated:
            return self.get_response(request)

        # 2. Allow system paths
        if request.path.startswith((
            "/accounts/",
            "/admin/",
            "/static/",
            "/",                 # 🔑 CRITICAL: allow dashboard entry
        )):
            return self.get_response(request)

        # 3. Super admin bypass
        if hasattr(request.user, "is_super_admin") and request.user.is_super_admin():
            return self.get_response(request)

        # 4. Now enforce subscription ONLY for ERP paths
        from subscriptions.models import Subscription

        try:
            sub = request.user.subscription
        except Subscription.DoesNotExist:
            raise PermissionDenied("No subscription")

        # Guard against broken FK safely
        if not sub.is_active or sub.erp_module_id is None:
            raise PermissionDenied("No active subscription")

        return self.get_response(request)


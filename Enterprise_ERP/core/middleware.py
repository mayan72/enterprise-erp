from django.core.exceptions import PermissionDenied

# class ModuleAccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         return self.get_response(request)

#     def process_view(self, request, view_func, view_args, view_kwargs):
#         user = request.user

#         # Skip checks for anonymous users or super admin
#         if not user.is_authenticated or user.is_super_admin():
#             return None

#         # Only protect ERP module views
#         module_code = getattr(view_func.view_class, "module_code", None)
#         if module_code is None:
#             return None  # normal non-ERP view

#         subscription = getattr(user, "subscription", None)
#         if not subscription or subscription.erp_module.code != module_code:
#             raise PermissionDenied("You do not have access to this ERP module.")

#         return None


from django.core.exceptions import PermissionDenied
from subscriptions.models import Subscription

class ModuleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        if request.user.is_super_admin():
            return self.get_response(request)

        try:
            subscription = request.user.subscription
        except Subscription.DoesNotExist:
            raise PermissionDenied("No subscription")

        if not subscription.erp_module.is_active:
            raise PermissionDenied("ERP module is inactive")

        return self.get_response(request)

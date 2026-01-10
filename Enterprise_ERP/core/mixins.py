from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from subscriptions.models import Subscription

from django.contrib.auth import get_user_model

User = get_user_model()


class RoleRequiredMixin(LoginRequiredMixin):
    """
    Restrict access based on User.role.
    """
    required_roles: tuple[str, ...] = ()

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return self.handle_no_permission()

        if self.required_roles and user.role not in self.required_roles:
            raise PermissionDenied("You do not have permission to access this view.")
        return super().dispatch(request, *args, **kwargs)


class ModuleAccessRequiredMixin(RoleRequiredMixin):
    """
    Enforce that the user has an active subscription to a given ERP module.
    Usage: set module_code = "medical" etc.
    """
    module_code: str | None = None

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return self.handle_no_permission()

        if user.is_super_admin():
            # Super Admin can access all modules
            # return super(RoleRequiredMixin, self).dispatch(request, *args, **kwargs)
            return super().dispatch(request, *args, **kwargs)

        if not self.module_code:
            raise PermissionDenied("Module code is not configured for this view.")

        try:
            subscription: Subscription = user.subscription
        except Subscription.DoesNotExist:
            raise PermissionDenied("You do not have any active ERP subscription.")

        if not subscription.is_active:
            raise PermissionDenied("Your subscription is inactive or expired.")

        if subscription.erp_module.code != self.module_code:
            raise PermissionDenied("You do not have access to this ERP module.")

        return super().dispatch(request, *args, **kwargs)

class UserDataMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_super_admin():
            return qs

        return qs.filter(user=user)


from django.core.exceptions import PermissionDenied

class SuperAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Login required")

        if not request.user.is_super_admin():
            raise PermissionDenied("Super Admin access only")

        return super().dispatch(request, *args, **kwargs)

def get_effective_user(request):
    if (
        request.user.is_authenticated
        and request.user.is_super_admin()
        and request.session.get("viewing_user_id")
    ):
        try:
            return User.objects.get(id=request.session["viewing_user_id"])
        except User.DoesNotExist:
            pass

    return request.user

# class TenantContextMixin:
#     """
#     In this ERP system:
#     Tenant = Subscription (User + ERPModule)
#     """

#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return super().dispatch(request, *args, **kwargs)

#         # Handle super-admin impersonation
#         effective_user = get_effective_user(request)

#         # Super admin without impersonation has no tenant context
#         if effective_user.is_super_admin() and effective_user == request.user:
#             request.tenant = None
#             return super().dispatch(request, *args, **kwargs)

#         try:
#             subscription = effective_user.subscription
#         except Subscription.DoesNotExist:
#             raise PermissionDenied("Tenant could not be resolved: no subscription")

#         if not subscription.is_active:
#             raise PermissionDenied("Tenant subscription is inactive or expired")

#         # 🔑 Tenant IS the subscription
#         request.tenant = subscription

#         return super().dispatch(request, *args, **kwargs)

class TenantContextMixin:
    """
    Tenant = Subscription of the effective user
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        effective_user = get_effective_user(request)

        # Super admin without impersonation → no tenant context
        if effective_user.is_super_admin() and effective_user == request.user:
            request.tenant = None
            request.effective_user = effective_user
            return super().dispatch(request, *args, **kwargs)

        try:
            subscription = effective_user.subscription
        except Exception:
            raise PermissionDenied("No active subscription for selected user")

        if not subscription.is_active:
            raise PermissionDenied("Subscription inactive or expired")

        # ✅ Tenant = subscription
        request.tenant = subscription
        request.effective_user = effective_user

        return super().dispatch(request, *args, **kwargs)

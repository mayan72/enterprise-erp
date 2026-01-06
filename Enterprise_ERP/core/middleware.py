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


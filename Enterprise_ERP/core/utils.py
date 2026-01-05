from accounts.models import User

def get_effective_user(request):
    """
    If super admin is viewing another user's dashboard,
    return that user. Otherwise return request.user.
    """
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

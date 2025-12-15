import logging
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, RedirectView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from .forms import LoginForm

auth_logger = logging.getLogger("auth_logger")

class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = "/"   # ✅ SINGLE ENTRY POINT

    def form_valid(self, form) -> HttpResponse:
        request: HttpRequest = self.request
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        ip = self._get_client_ip(request)

        try:
            user = authenticate(request, username=username, password=password)
            if user is None:
                auth_logger.warning(
                    "AUTH_FAILED username=%s ip=%s",
                    username,
                    ip,
                )
                form.add_error(None, "Invalid username or password.")
                return self.form_invalid(form)

            if not user.is_active:
                auth_logger.warning(
                    "AUTH_INACTIVE user_id=%s ip=%s",
                    user.id,
                    ip,
                )
                form.add_error(None, "Account is inactive.")
                return self.form_invalid(form)

            login(request, user)
            auth_logger.info(
                "AUTH_SUCCESS user_id=%s role=%s ip=%s",
                user.id,
                user.role,
                ip,
            )
            return super().form_valid(form)

        except Exception as exc:
            auth_logger.error(
                "AUTH_ERROR username=%s ip=%s error=%s",
                username,
                ip,
                str(exc),
                exc_info=True,
            )
            form.add_error(None, "An internal error occurred. Please try again.")
            return self.form_invalid(form)


    @staticmethod
    def _get_client_ip(request: HttpRequest) -> str:
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")


class LogoutView(RedirectView):
    pattern_name = "accounts:login"

    def get(self, request: HttpRequest, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        ip = LoginView._get_client_ip(request)
        try:
            if user:
                auth_logger.info(
                    "LOGOUT user_id=%s role=%s ip=%s",
                    user.id,
                    getattr(user, "role", None),
                    ip,
                )
            logout(request)
        except Exception as exc:
            auth_logger.error(
                "LOGOUT_ERROR user_id=%s ip=%s error=%s",
                getattr(user, "id", None),
                ip,
                str(exc),
                exc_info=True,
            )
        return super().get(request, *args, **kwargs)

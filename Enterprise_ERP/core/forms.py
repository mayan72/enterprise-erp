from django import forms
from subscriptions.models import ErpModule


class AdminUserCreateForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    erp_module = forms.ModelChoiceField(
        queryset=ErpModule.objects.filter(is_active=True)
    )
    is_active = forms.BooleanField(required=False, initial=True)

from django import forms
from subscriptions.models import ErpModule


class ErpModuleCreateForm(forms.ModelForm):
    class Meta:
        model = ErpModule
        fields = [
            "code",
            "name",
            "app_label",
            "url_namespace",
            "description",
            "is_active",
        ]

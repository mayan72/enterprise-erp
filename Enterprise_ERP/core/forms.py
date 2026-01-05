from django import forms
from core.models import ERPModule


# class AdminUserCreateForm(forms.Form):
#     erp_module = forms.ModelChoiceField(
#         queryset=ERPModule.objects.filter(is_active=True),
#         required=True
#     )


from subscriptions.models import Subscription

class AdminUserCreateForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    is_active = forms.BooleanField(required=False, initial=True)

    erp_module = forms.ModelChoiceField(
        queryset=ERPModule.objects.filter(is_active=True)
    )

    plan = forms.ChoiceField(
        choices=Subscription.Plan.choices,
        required=True,
        initial=Subscription.Plan.THREE_MONTHS,
        label="Subscription Plan"
    )


class ErpModuleCreateForm(forms.ModelForm):
    class Meta:
        model = ERPModule
        fields = (
            "name",
            "code",
            "icon",
            "is_active",
        )

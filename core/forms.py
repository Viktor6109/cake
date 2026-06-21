from django import forms
from django.contrib.auth import authenticate

from .models import Client


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Придумайте пароль"}),
        min_length=8,
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"}),
    )

    class Meta:
        model = Client
        fields = ["name", "email", "phone"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ваше имя"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 (999) 123-45-67"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data is None:
            return cleaned_data

        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self._user = None

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data is None:
            return None

        email = cleaned_data.get("email", "").lower()
        password = cleaned_data.get("password")
        if email and password:
            self._user = authenticate(self.request, username=email, password=password)
            if self._user is None:
                raise forms.ValidationError("Неверный email или пароль.")
            if not self._user.is_active:
                raise forms.ValidationError("Аккаунт заблокирован.")
        return cleaned_data

    def get_user(self):
        return self._user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "phone", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ваше имя"}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 (999) 123-45-67"}),
            "address": forms.Textarea(
                attrs={"placeholder": "Адрес доставки", "rows": 3}
            ),
        }

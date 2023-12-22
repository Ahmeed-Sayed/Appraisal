from django import forms
import re
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import EmployeeMore

User = get_user_model()


def validate_phone_number(value):
    pattern = r"^(011|012|010|015)\d{8}$"
    if not re.match(pattern, value):
        raise ValidationError(
            "Phone number must start with 011, 012, 010, or 015 and be 11 digits long."
        )
    return value


def validate_password1(value):
    regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"
    result = re.match(regex, value)
    if result is None:
        raise ValidationError(
            "Password must be at least 8 characters long, have one uppercase character, one lowercase character, and at least one digit."
        )
    return result


class EmployeeMoreForm(forms.ModelForm):
    class Meta:
        model = EmployeeMore
        fields = ["empSupervisor", "departmentManager"]


class CombinedForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    firstName = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    lastName = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    phoneNumber = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    role = forms.ChoiceField(
        choices=(
            ("employee", "employee"),
            ("supervisor", "supervisor"),
            ("departmentManager", "departmentManager"),
            ("hrEmployee", "hrEmployee"),
        ),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    empSupervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(role=User.Roles.supervisor),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    departmentManager = forms.ModelChoiceField(
        queryset=User.objects.filter(role=User.Roles.departmentManager),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self):
        user = User.objects.create(
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data["firstName"],
            last_name=self.cleaned_data["lastName"],
            phoneNumber=self.cleaned_data["phoneNumber"],
            address=self.cleaned_data["address"],
            role=self.cleaned_data["role"],
        )
        user.set_password(self.cleaned_data["password1"])
        user.save()

        if self.cleaned_data["role"] == "employee":
            EmployeeMore.objects.create(
                user=user,
                empSupervisor=self.cleaned_data.get("empSupervisor"),
                departmentManager=self.cleaned_data.get("departmentManager"),
            )

        return user

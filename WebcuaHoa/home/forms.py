from django import forms
from home.models import KhachHang
from home.models import TaiKhoan


class RegisterForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = "__all__"


class TaikhoanForm(forms.ModelForm):
    class Meta:
        model = TaiKhoan
        fields = "__all__"


class LoginForm(forms.ModelForm):
    class Meta:
        model = TaiKhoan
        fields = "__all__"

from django.contrib import admin
from .models import KhachHang, NhanVien, TaiKhoan, VeXe, XeKhach

# Register your models here.
admin.site.register(KhachHang)
admin.site.register(NhanVien)
admin.site.register(XeKhach)
admin.site.register(VeXe)
admin.site.register(TaiKhoan)

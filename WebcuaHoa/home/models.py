from django.db import models


# Create your models here.
class KhachHang(models.Model):
    SDT = models.CharField(primary_key=True, max_length=10)
    TenKH = models.CharField(max_length=50)
    DiaChi = models.CharField(max_length=50)
    class Meta:
        db_table = "home_khachhang"


class NhanVien(models.Model):
    MaNV = models.AutoField(primary_key=True)
    HoTen = models.CharField(max_length=50)
    DiaChi = models.CharField(max_length=50)
    SDT = models.CharField(max_length=10)
    class Meta:
        db_table = "home_nhanvien"


class XeKhach(models.Model):
    BienSoXe = models.CharField(primary_key=True, max_length=20)
    GioXuatBen = models.DateTimeField()
    MaNV = models.ForeignKey(NhanVien,on_delete=models.CASCADE)
    class Meta:
        db_table = "home_xekhach"


class VeXe(models.Model):
    MaHD = models.AutoField(primary_key=True)
    SDT = models.CharField(max_length=10)
    TenKH = models.ForeignKey(KhachHang, default=None,on_delete=models.CASCADE)
    ChoNgoi = models.CharField(max_length=5)
    NgBan = models.DateField()
    GioXuatBen = models.DateTimeField()
    Giave = models.BinaryField()
    BienSoXe = models.CharField(max_length=20)
    class Meta:
        db_table = "home_vexe"


class TaiKhoan(models.Model):
    TenTk = models.CharField(max_length=20)
    MatKhau = models.CharField(max_length=20)
    class Meta:
        db_table = "home_taikhoan"


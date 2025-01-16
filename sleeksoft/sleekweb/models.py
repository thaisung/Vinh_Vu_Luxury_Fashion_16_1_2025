# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils.text import slugify

# Create your models here.

class User(AbstractUser):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Quản lý tài khoản Đăng Nhập"
    AbstractUser._meta.get_field('email').blank = False
    AbstractUser._meta.get_field('email').blank = False
    AbstractUser._meta.get_field('username').blank = False
    AbstractUser._meta.get_field('username').blank = False
    AbstractUser._meta.get_field('password').blank = False
    AbstractUser._meta.get_field('password').blank = False
    
    is_manage = models.BooleanField('Quản lý',blank=True, null=True,default=False)
    Avatar = models.ImageField(upload_to='User_photo', default="User_image/user_empty.png", null=True,blank=True)
    Full_name = models.CharField('Họ và tên', max_length=255,blank=True, null=True)
    OTP = models.CharField('Mã Otp',max_length=255, null=True,blank=True)
    Phone_number = models.CharField('Số điện thoại',max_length=255, null=True,blank=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['is_staff']),
            models.Index(fields=['Full_name']),
            models.Index(fields=['is_manage']),
        ]
        
class Address_order(models.Model):
    customerName = models.CharField('Họ và tên', max_length=255,blank=True, null=True)
    customerEmail = models.CharField('Email', max_length=255,blank=True, null=True)
    customerMobile = models.CharField('Số đt', max_length=255,blank=True, null=True)
    customerAddress = models.CharField('Địa chỉ cụ thể', max_length=255,blank=True, null=True)
    customerCity = models.CharField('Tỉnh', max_length=255,blank=True, null=True)
    customerDistrict = models.CharField('Huyện', max_length=255,blank=True, null=True)
    ward = models.CharField('Xã', max_length=255,blank=True, null=True)
    description = models.TextField('Ghi chú', blank=True, null=True)
    Belong_User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address',blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Belong_User']),
            models.Index(fields=['customerName']),
        ]
        
class Website(models.Model):
    Name = models.CharField('Tên Website', max_length=255,blank=True, null=True)
    Logo = models.ImageField(upload_to='Website_photo', null=True,blank=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Name']),
        ]
        
class Category_product(models.Model):
    Name = models.CharField('Tên Danh mục mẹ', max_length=255,blank=True, null=True)
    Slug = models.SlugField('Slug', max_length=255, unique=True, blank=True, null=True)
    Arrange = models.IntegerField('Thứ tự xuất hiện',blank=True, null=True,default=0)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Name']),
        ]
        
class Category_product_child(models.Model):
    Name = models.CharField('Tên Danh mục con', max_length=255,blank=True, null=True)
    Slug = models.SlugField('Slug', max_length=255, unique=True, blank=True, null=True)
    Belong_Category_product = models.ForeignKey(Category_product, on_delete=models.CASCADE, related_name='category_product_detail',blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Name']),
        ]
        
class Trademark(models.Model):
    Name = models.CharField('Tên thương hiệu', max_length=255,blank=True, null=True)
    Slug = models.SlugField('Slug', max_length=255, unique=True, blank=True, null=True)
    Avatar = models.ImageField(upload_to='Trademark_photo', null=True,blank=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Name']),
        ]
        
class Product(models.Model):
    Name = models.CharField('Tên sản phẩm', max_length=255,blank=True, null=True)
    Slug = models.SlugField('Slug', max_length=255, unique=True, blank=True, null=True)
    Price = models.CharField('Giá', max_length=255,blank=True, null=True)
    Description = models.TextField('Mô tả sản phẩm',blank=True, null=True)
    Discount = models.IntegerField('giảm giá',blank=True, null=True)
    Price_Discount = models.CharField('Giá sau giảm', max_length=255,blank=True, null=True)
    Belong_Category_product_child = models.ForeignKey(Category_product_child, on_delete=models.CASCADE, related_name='category_product_child_detail',blank=True, null=True)
    Belong_Trademark = models.ForeignKey(Trademark, on_delete=models.SET_NULL, related_name='category_product_child_detail',blank=True, null=True)
    Quantity_buy = models.IntegerField('Số lượng đã bán', blank=True, null=True,default=0)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Name']),
        ]
  
class Size_product(models.Model):
    Size = models.CharField('Kích thước', max_length=255,blank=True, null=True)
    Quantity = models.IntegerField('Số lượng trong kho', blank=True, null=True)
    Belong_Product_Size = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_size_detail',blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Size']),
        ]
        
class Photo_product(models.Model):
    Photo = models.ImageField(upload_to='Product_photo', null=True,blank=True)
    Belong_Product_Photo = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_photo_detail',blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Belong_Product_Photo']),
        ]
        
class Cart(models.Model):
    Belong_User = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_detail_cart',blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Belong_User']),
        ]
        
class Product_Cart(models.Model):
    Belong_Cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_detail',blank=True, null=True)
    Quantity = models.CharField('Số lượng dự định mua', max_length=255,blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Belong_Cart']),
        ]
        
        
class Order(models.Model):
    Code = models.CharField('Mã đơn hàng', max_length=255,blank=True, null=True)
    customerName = models.CharField('Họ và tên', max_length=255,blank=True, null=True)
    customerEmail = models.CharField('Email', max_length=255,blank=True, null=True)
    customerMobile = models.CharField('Số đt', max_length=255,blank=True, null=True)
    customerAddress = models.CharField('Địa chỉ cụ thể', max_length=255,blank=True, null=True)
    customerCity = models.CharField('Tỉnh', max_length=255,blank=True, null=True)
    customerDistrict = models.CharField('Huyện', max_length=255,blank=True, null=True)
    ward = models.CharField('Xã', max_length=255,blank=True, null=True)
    description = models.TextField('Ghi chú', blank=True, null=True)
    Data = models.JSONField('dữ liệu đơn hàng',blank=True, null=True)
    Belong_User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_detail_order',blank=True, null=True)
    Status = models.CharField('Trạng thái đơn hàng', max_length=255,blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Status']),
            models.Index(fields=['Belong_User']),
        ]
        
class Product_Order(models.Model):
    Belong_Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_detail',blank=True, null=True)
    Quantity = models.CharField('Số lượng mua', max_length=255,blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['Belong_Order']),
        ]
        



class Campaign(models.Model):
    Name = models.CharField('Tên chiến dịch', max_length=255,blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Link_KH = models.BooleanField('Link KH',blank=True, null=True,default=True)
    So_DT = models.BooleanField('So_DT',blank=True, null=True,default=False)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    Belong_User = models.ManyToManyField(User,related_name='list_campaign',blank=True)
    Belong_User_Delete = models.ManyToManyField(User,related_name='list_campaign_delete_data',blank=True)
    class Meta:
        indexes = [
            models.Index(fields=['Name']),
        ]
        
class Lead(models.Model):
    Name = models.CharField('Họ và tên khách hàng', max_length=255,blank=True, null=True)
    Phone_number = models.CharField('Số đt khách hàng', max_length=255,blank=True, null=True)
    Area = models.CharField('Khu vực', max_length=255,blank=True, null=True,default='')
    Product = models.CharField('Sản phẩm', max_length=255,blank=True, null=True,default='')
    Demand = models.CharField('Nhu cầu', max_length=255,blank=True, null=True,default='')
    Status = models.CharField('Tình trạng', max_length=255,blank=True, null=True)
    Note = models.TextField('Ghi chú',blank=True, null=True,default='')
    Status_lead = models.CharField('Trạng thái khách hàng', max_length=255,blank=True, null=True ,default='Chưa tư vấn')
    Source = models.CharField('Nguồn nhập',max_length=255,blank=True, null=True,default='')
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    Belong_Campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='list_campaign',blank=True, null=True)
    Belong_User = models.ForeignKey(User,on_delete=models.SET_NULL, related_name='list_lead',blank=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['Name']),
            models.Index(fields=['Belong_Campaign']),
            models.Index(fields=['Belong_User']),
        ]
        
class Report(models.Model):
    report = models.TextField('Báo cáo của NV',blank=True, null=True,default='')
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    Belong_Lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='list_report',blank=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['Belong_Lead']),
        ]
        
class History(models.Model):
    history = models.TextField('Ghi chú lịch sử CSKH của NV',blank=True, null=True,default='')
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    Belong_Lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='list_history',blank=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['Belong_Lead']),
        ]

class Select_setting(models.Model):
    Area = models.TextField('Danh sách lựa chọn khu vực',blank=True, null=True,default='')
    Product = models.TextField('Danh sách lựa chọn sản phẩm',blank=True, null=True,default='')
    Demand = models.TextField('Danh sách lựa chọn nhu cầu',blank=True, null=True,default='')
    Source = models.TextField('Danh sách lựa chọn nguồn',blank=True, null=True,default='')
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    
class Email_setting(models.Model):
    EMAIL_HOST = models.CharField(max_length=255,blank=True, null=True,default='')
    EMAIL_USE_TLS = models.BooleanField(blank=True, null=True,default=True)
    EMAIL_USE_SSL = models.BooleanField(blank=True, null=True,default=True)
    EMAIL_PORT = models.CharField(max_length=255,blank=True, null=True,default='')
    EMAIL_HOST_USER = models.CharField(max_length=255,blank=True, null=True,default='')
    EMAIL_HOST_PASSWORD = models.CharField( max_length=255,blank=True, null=True,default='')
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    

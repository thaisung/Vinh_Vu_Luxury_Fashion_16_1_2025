from ..models import *

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator


from django.http import HttpResponse
import requests
import time

from django.db import models
from django.utils import timezone

import os

from datetime import datetime

from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from datetime import datetime
from django.contrib import messages
import random
import string
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

# from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

import random
import string

import base64

import time
from django.http import JsonResponse

import re
import json

from django.conf import settings
from django.db.models import Q

import datetime

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

from types import SimpleNamespace

def format_number(number):
    """
    Định dạng một số nguyên hoặc số thực thành chuỗi có dấu chấm ngăn cách mỗi 3 chữ số.

    :param number: Số cần định dạng (int hoặc float)
    :return: Chuỗi định dạng với dấu chấm ngăn cách
    """
    try:
        number = int(number)
        # Đảm bảo số là số nguyên hoặc số thực
        if isinstance(number, (int, float)):
            # Sử dụng f-string để định dạng và thay dấu phẩy thành dấu chấm
            return f"{number:,.0f}".replace(",", ".")
        else:
            raise ValueError("Giá trị đầu vào phải là số nguyên hoặc số thực.")
    except Exception as e:
        return f"Lỗi: {e}"
    
def format_cart(cart_items):
    Cart_user = {'data': [], 'total_quantity': 0, 'total_money': 0,'count':0}
    for i in cart_items:
        try:
            product = Product.objects.get(pk=i['id'])  # Lấy sản phẩm từ database
        except Product.DoesNotExist:
            continue  # Bỏ qua nếu sản phẩm không tồn tại

        if product.Discount > 0:
            total_money = format_number(int(i['quantity'])*int(product.Price_Discount))
        else:
            total_money = format_number(int(i['quantity'])*int(product.Price))

        obj_cart = {
            'product': product,
            'size': i['size'],
            'quantity': int(i['quantity']),
            'pk':i['pk'],
            'total_money':total_money
        }
        Cart_user['data'].append(obj_cart)

    # Tính tổng số lượng và tổng tiền
    for i in Cart_user['data']:
        Cart_user['total_quantity'] += i['quantity']
        if i['product'].Discount > 0:
            Cart_user['total_money'] += i['quantity'] * int(i['product'].Price_Discount)
        else:
            Cart_user['total_money'] += i['quantity'] * int(i['product'].Price)
    Cart_user['total_money'] = format_number(Cart_user['total_money'])
    Cart_user['count'] =  len(Cart_user['data'])
    for i in Cart_user['data']:
        i['product'].Price = format_number(i['product'].Price)
        i['product'].Price_Discount = format_number(i['product'].Price_Discount)
    return Cart_user



def order_cl(request):
    if request.method == 'GET':
        context = {}

        list_obj_website = Website.objects.all()
        if list_obj_website:
            context['obj_website'] = list_obj_website[0]
        list_obj_email = Email_setting.objects.all()
        if list_obj_email:
            context['obj_email'] = list_obj_email[0]
            
        # Lấy giỏ hàng từ cookie
        cart = request.COOKIES.get('cart', '[]')
        try:
            cart_items = json.loads(cart)
        except json.JSONDecodeError:
            cart_items = []  # Nếu cookie không hợp lệ, đặt giỏ hàng mặc định là rỗng

        # Tạo phản hồi render trang
        response = render(request, 'sleekweb/client/home.html', context, status=200)

        # Lưu giỏ hàng (nếu chưa tồn tại cookie)
        if not cart_items:
            response.set_cookie('cart', json.dumps([]), max_age=3600 * 24 * 7)  # Cookie tồn tại 7 ngày
        
        cart = request.COOKIES.get('cart', '[]')
        try:
            cart_items = json.loads(cart)
        except json.JSONDecodeError:
            cart_items = []  # Nếu cookie không hợp lệ, đặt giỏ hàng mặc định là rỗng
        
        # Tính toán thông tin giỏ hàng
        Cart_user = {'data': [], 'total_quantity': 0, 'total_money': 0,'count':0}
        for i in cart_items:
            try:
                product = Product.objects.get(pk=i['id'])  # Lấy sản phẩm từ database
            except Product.DoesNotExist:
                continue  # Bỏ qua nếu sản phẩm không tồn tại

            obj_cart = {
                'product': product,
                'size': i['size'],
                'quantity': int(i['quantity']),
                'pk':i['pk']
            }
            Cart_user['data'].append(obj_cart)

        # Tính tổng số lượng và tổng tiền
        for i in Cart_user['data']:
            Cart_user['total_quantity'] += i['quantity']
            if i['product'].Discount > 0:
                Cart_user['total_money'] += i['quantity'] * int(i['product'].Price_Discount)
            else:
                Cart_user['total_money'] += i['quantity'] * int(i['product'].Price)
        context['Cart_user'] = Cart_user
        Cart_user['count'] =  len(Cart_user['data'])
        for i in Cart_user['data']:
            i['product'].Price = format_number(i['product'].Price)
            i['product'].Price_Discount = format_number(i['product'].Price_Discount)
            
        # Lấy tất cả danh mục lớn
        context['List_Category_product'] = Category_product.objects.all()
        context['List_Category_product'] = list(context['List_Category_product'])
                
        for category in context['List_Category_product']:
            print('category:',category)
            # Lấy 3 sản phẩm đầu tiên cho danh mục lớn
            category.list_product = Product.objects.filter(
                Belong_Category_product_child__Belong_Category_product=category
            ).order_by('Creation_time')[:3]
            
            # Lấy tất cả sản phẩm cho danh mục lớn
            category.list_product_home = Product.objects.filter(
                Belong_Category_product_child__Belong_Category_product=category
            ).order_by('Creation_time')
            
            # Gán photo_1 và photo_2 cho từng sản phẩm
            for product in category.list_product_home:
                photos = product.product_photo_detail.all()
                product.photo_1 = photos.first()  # Ảnh đầu tiên
                product.photo_2 = photos[1] if photos.count() > 1 else None  # Ảnh thứ 2 (nếu có)
                
                # Kiểm tra hết hàng
                total_quantity = product.product_size_detail.aggregate(
                    total=models.Sum('Quantity')
                )['total'] or 0
                product.is_out_of_stock = total_quantity == 0  # True nếu hết hàng
                
        # Tạo danh mục giả lập "Sale"
        sale_category = SimpleNamespace(
            id="9999999999999999",  # Đặt một giá trị giả định cho id
            Name="SUPER SALE",
            Slug="super-sale",
            list_product_home=Product.objects.filter(Discount__gt=0).order_by('Creation_time'),
            # list_product = Product.objects.filter(Discount__gt=0).order_by('Creation_time')[:3]
        )
        # Gán photo_1 và photo_2 cho từng sản phẩm
        for product in sale_category.list_product_home:
            photos = product.product_photo_detail.all()
            product.photo_1 = photos.first()  # Ảnh đầu tiên
            product.photo_2 = photos[1] if photos.count() > 1 else None  # Ảnh thứ 2 (nếu có)
            
            # Kiểm tra hết hàng
            total_quantity = product.product_size_detail.aggregate(
                total=models.Sum('Quantity')
            )['total'] or 0
            product.is_out_of_stock = total_quantity == 0  # True nếu hết hàng
        
        context['List_Category_product'].append(sale_category)
            
        context['List_Order'] = Order.objects.filter(Belong_User=request.user)
        for i in context['List_Order']:
            i.Data = format_cart(i.Data)
            print('Data:',i.Data)
            
        context['List_Product_Love'] = Product.objects.all()
        print('List_Product_Love:',context['List_Product_Love'])
        for product in context['List_Product_Love']:
            photos = product.product_photo_detail.all()
            product.photo_1 = photos.first()  # Ảnh đầu tiên
            product.photo_2 = photos[1] if photos.count() > 1 else None  # Ảnh thứ 2 (nếu có)
            
            # Kiểm tra hết hàng
            total_quantity = product.product_size_detail.aggregate(
                total=models.Sum('Quantity')
            )['total'] or 0
            product.is_out_of_stock = total_quantity == 0  # True nếu hết hàng
            product.Price = format_number(product.Price)
            product.Price_Discount = format_number(product.Price_Discount)
        return render(request, 'sleekweb/client/order.html', context, status=200)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            customerName = request.POST.get('customerName')
            customerEmail = request.POST.get('customerEmail')
            customerMobile = request.POST.get('customerMobile')
            customerAddress = request.POST.get('customerAddress')
            customerCity = request.POST.get('customerCityId')
            print('lc',customerCity)
            customerDistrict = request.POST.get('customerDistrictId')
            print('lc',customerDistrict)
            ward = request.POST.get('customerWardId')
            print('lc',ward)
            paymentMethod = request.POST.get('paymentMethod')
            description = request.POST.get('description')
            user = request.user
            # list_Address = Address_order.objects.filter(Belong_User=user)
            # if list_Address :
            #     Address = list_Address[0]
            #     Address.customerName = customerName
            #     Address.customerEmail = customerEmail
            #     Address.customerMobile = customerMobile
            #     Address.customerAddress = customerAddress
            #     Address.customerCity = customerCity
            #     Address.customerDistrict = customerDistrict
            #     Address.ward = ward
            #     Address.description = description
            #     Address.save()
            # else:
            #     Address = Address_order.objects.create(
            #         customerName = customerName,
            #         customerEmail = customerEmail,
            #         customerMobile = customerMobile,
            #         customerAddress = customerAddress,
            #         customerCity = customerCity,
            #         customerDistrict = customerDistrict,
            #         ward = ward,
            #         description = description
            #     )
            cart = request.COOKIES.get('cart', '[]')
            try:
                cart_items = json.loads(cart)
            except json.JSONDecodeError:
                cart_items = []  # Nếu cookie không hợp lệ, đặt giỏ hàng mặc định là rỗng
            if cart_items:
                Order.objects.create(
                    customerName = customerName,
                    customerEmail = customerEmail,
                    customerMobile = customerMobile,
                    customerAddress = customerAddress,
                    customerCity = customerCity,
                    customerDistrict = customerDistrict,
                    ward = ward,
                    description = description,
                    Data = cart_items,
                    Belong_User = user,
                    paymentMethod = paymentMethod,
                    Code = ''.join(random.choices('0123456789', k=8)),
                    Status = 'Chờ xác nhận'
                )
                return JsonResponse({'success': True, 'message': 'Đặt hàng thành công.'},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': True, 'message': 'Không thể đặt hàng với đơn hàng trống sản phẩm.'},json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'success': True, 'message': 'Đăng nhập tài khoản trước khi đặt hàng.'},json_dumps_params={'ensure_ascii': False})
           
def delete_order_cl(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        obj_order = Order.objects.get(pk=id)
        if obj_order.Status == 'Chờ xác nhận':
            obj_order.delete()
        return redirect('order_cl')
    else:
        return redirect('order_cl')
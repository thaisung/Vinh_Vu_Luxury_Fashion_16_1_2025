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

from django.core.mail import send_mail
from django.forms.models import model_to_dict
from django.core.mail import send_mail,EmailMessage

def format_number(number):
    print('number:',number)
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

def getpassword_cl(request):
    if request.method == 'GET':
        context = {}
        
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

        list_obj_website = Website.objects.all()
        if list_obj_website:
            context['obj_website'] = list_obj_website[0]
        list_obj_email = Email_setting.objects.all()
        if list_obj_email:
            context['obj_email'] = list_obj_email[0]

        context['List_Category_product'] = Category_product.objects.all()
        
        for category in context['List_Category_product']:
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
        
        return render(request, 'sleekweb/client/getpassword.html', context, status=200)
    elif request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            try:
                user = User.objects.get(username = username)
                otp = random.randint(10000000, 99999999)
                user.OTP = otp
                user.save()
                if user:
                    email = username
                    subject = f'Thông báo từ hệ thống CSKH'
                    message = f"""
                    <html>
                    <body>
                        <p><strong>Mã OTP để lấy lại mật khẩu của bạn là:</strong></p>
                        <p>{otp}</p>
                    </body>
                    </html>
                    """

                    email = EmailMessage(subject, message, to=[email])
                    email.content_subtype = "html"  # Đặt định dạng nội dung email là HTML
                    email.send()
                return JsonResponse({'success': True, 'message': 'Gửi mã OTP thành công.'})
            except:
                user = None
                return JsonResponse({'success': False, 'message': 'Email không tồn tại.'})
        else:
            return JsonResponse({'success': False, 'message': 'Email không không hợp lệ !'})
    else:
        return redirect('getpassword_cl')

def reset_pasword_cl(request):
    if request.method == 'GET':
        context = {}
        
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

        list_obj_website = Website.objects.all()
        if list_obj_website:
            context['obj_website'] = list_obj_website[0]
        list_obj_email = Email_setting.objects.all()
        if list_obj_email:
            context['obj_email'] = list_obj_email[0]

        context['List_Category_product'] = Category_product.objects.all()
        
        for category in context['List_Category_product']:
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
        
        print('context:',context)
        return render(request, 'sleekweb/client/reset_pasword.html', context, status=200)
    elif request.method == 'POST':
        context = {}
        print('context:',context)
        otp = request.POST.get('otp')
        new_pw = request.POST.get('new_pw')
        try:
            user = User.objects.get(OTP = otp)
            if user:
                user.OTP = ''
                user.password = make_password(new_pw)
                user.save()
                return JsonResponse({'success': True,'message': 'Đổi mật khẩu thành công tài khoản. Đăng nhập ngay'})
            else:
                return JsonResponse({'success': False, 'message': 'Mã OTP không chính xác'})
        except:
            user = None
            return JsonResponse({'success': False, 'message': 'Mã OTP không chính xác'})
    else:
        return JsonResponse({'success': False, 'message': 'Không tồn tại phương thức.'})
    
    
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

def search_cl(request):
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

        s = request.GET.get('s')
        f_size = request.GET.get('f_size')
        f_trademark = request.GET.get('f_trademark')
        f_arrange = request.GET.get('f_arrange')
        if s :
            print('s:',s)
        # Lấy tất cả danh mục lớn
            context['List_Product_filter'] = Product.objects.filter(Q(Name__icontains=s)).order_by('-id')
            context['s'] = s
        else:
            context['List_Product_filter'] = Product.objects.all()
        print('List_Product_filter:',context['List_Product_filter'])
        if f_size:
                context['f_size'] = f_size
                context['List_Product_filter'] = context['List_Product_filter'].filter(product_size_detail__Size=f_size)
        if f_trademark:
            context['f_trademark'] = f_trademark
            context['List_Product_filter'] = context['List_Product_filter'].filter(Belong_Trademark__Name=f_trademark)
        if f_arrange:
            context['f_arrange'] = f_arrange
            if f_arrange == '':
                # Sản phẩm mới nhất
                context['List_Product_filter'] = context['List_Product_filter'].order_by('Creation_time')

            if f_arrange == 'priceDesc':
                # Sản phẩm giá giảm dần
                context['List_Product_filter'] = context['List_Product_filter'].order_by('Price_Discount')

            if f_arrange == 'priceAsc':
                # Sản phẩm giá tăng dần
                context['List_Product_filter'] = context['List_Product_filter'].order_by('-Price_Discount')

            if f_arrange == 'discount':
                # Sản phẩm giảm giá (Discount > 0)
                context['List_Product_filter'] = context['List_Product_filter'].filter(Discount__gt=0).order_by('Discount') 
        
        for product in context['List_Product_filter']:
            photos = product.product_photo_detail.all()
            product.photo_1 = photos.first()  # Ảnh đầu tiên
            product.photo_2 = photos[1] if photos.count() > 1 else None  # Ảnh thứ 2 (nếu có)
            
            # Kiểm tra hết hàng
            total_quantity = product.product_size_detail.aggregate(
                total=models.Sum('Quantity')
            )['total'] or 0
            product.is_out_of_stock = total_quantity == 0  # True nếu hết hàng
        print('List_Product_filter1:',context['List_Product_filter'])
        context['List_Trademark'] = Trademark.objects.all()
        context['List_Size_product'] = Size_product.objects.all()
        context['List_Size_product'] = {s.Size: s for s in context['List_Size_product']}.values()
        context['List_Category_product'] = Category_product.objects.all()
        context['List_Category_product'] = list(context['List_Category_product'])
        for category in context['List_Category_product']:
            # Lấy 3 sản phẩm đầu tiên cho danh mục lớn
            category.list_product = Product.objects.filter(
                Belong_Category_product_child__Belong_Category_product=category
            ).order_by('Creation_time')[:3]
            
        # Gán photo_1 và photo_2 cho từng sản phẩm
        for product in context['List_Product_filter']:
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
        
        #Sử dụng Paginator để chia nhỏ danh sách (10 là số lượng mục trên mỗi trang)
        paginator = Paginator(context['List_Product_filter'], settings.PAGE)
        context['num_pages'] = int(paginator.num_pages)
        # Lấy số trang hiện tại từ URL, nếu không mặc định là trang 1
        p = request.GET.get('p')
        page_obj = paginator.get_page(p)
        context['List_Product_filter'] = page_obj
        print('list_product_home th:',context['List_Product_filter'])
        # Tạo danh sách các số trang
        page_list = list(range(1, paginator.num_pages + 1))
        context['page_list'] = page_list
        print('page_list:',page_list)
        if p :
            context['p']=int(p)
        else:
            context['p']=1
            
        # Tính phạm vi các trang hiển thị, trang hiện tại ở giữa
        total_pages = paginator.num_pages
        current_page = page_obj.number

        # Xác định phạm vi 5 trang
        start_page = max(current_page - 2, 1)  # Ít nhất là 1
        end_page = min(current_page + 2, total_pages)  # Không vượt quá tổng số trang

        # Điều chỉnh nếu số lượng trang hiển thị không đủ 5
        if end_page - start_page < 4:
            if start_page == 1:  # Nếu bắt đầu từ trang 1, mở rộng phạm vi kết thúc
                end_page = min(start_page + 4, total_pages)
            elif end_page == total_pages:  # Nếu kết thúc ở trang cuối, lùi phạm vi bắt đầu
                start_page = max(end_page - 4, 1)

        custom_page_range = range(start_page, end_page + 1)
        context['custom_page_range'] = custom_page_range
            
        
        context['List_Category_product'].append(sale_category)

        return render(request, 'sleekweb/client/search.html', context, status=200)
    else:
        return redirect('search_cl')
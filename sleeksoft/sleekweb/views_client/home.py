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

def home_cl(request):
    if request.method == 'GET':
        print('re:',request.path)
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
        
        return render(request, 'sleekweb/client/home.html', context, status=200)
    else:
        return redirect('home_cl')

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
def get_category_product_child_cl(request,pk):
    if request.method == 'GET':
        print('pkpk;',pk)
        obj_product=Category_product_child.objects.get(pk=pk)
        list_product = obj_product.category_product_child_detail.all()
        for product in list_product:
                photos = product.product_photo_detail.all()
                product.photo_1 = photos.first()  # Ảnh đầu tiên
                product.photo_2 = photos[1] if photos.count() > 1 else None  # Ảnh thứ 2 (nếu có)
                
                # Kiểm tra hết hàng
                total_quantity = product.product_size_detail.aggregate(
                    total=models.Sum('Quantity')
                )['total'] or 0
                product.is_out_of_stock = total_quantity == 0  # True nếu hết hàng
        thumbnail = ''
        # Tạo danh sách các thẻ <option> cho thương hiệu
        for idx,k in enumerate(list_product):
            sale = ''
            stock = ''
            size = ''
            price = ''
            product_saleNew = ''
            link = ''
            if k.Discount > 0:
                sale = """<div class="goodsli-discount goodsli-promo">sale</div>"""
            else:
                sale = ''
            if k.is_out_of_stock:
                stock = """<div class="out-of-stock">Hết hàng</div>"""
            else:
                stock = ''
                link = link+f"""
                <div class="actionLoop visible-lg tp_button">
                    <a class="quickView styleBtnBuy notClick" data-id="{k.id}"><i
                            class="fa fa-shopping-cart"></i> Mua nhanh</a>
                    <a class="styleBtnBuy" target=""
                        href="/detail-product/{k.Slug}/"><i
                            class="fa fa-eye"></i> Xem chi tiết</a>
                </div>
                """
            for s in k.product_size_detail.all():
                size = size +f"""
                <a
                href="https://cuongpopauth.com/dep-alexander-mcqueen-xanh-reu-663563-w4tm6-3211-41-p40776045.html"
                class="text-main" value="40776045" title="41">
                {s.Size}</a>"""
            
            if k.Discount > 0:
                price = price + f"""
                            <p class="pro-price highlight tp_product_price">
                                <span class="priceSale format-number">{format_number(k.Price_Discount)}₫</span>
                                <span class="pro-price-del"><del
                                        class="compare-price format-number">{format_number(k.Price)}₫</del></span>
                            </p>
                        """
                product_saleNew = product_saleNew+f"""
                <div class="product-saleNew">Giảm {format_number(k.Discount)}%</div>
                """
            else:
                price = price + f"""
                            <p class="pro-price highlight tp_product_price">
                                <span class="priceSale format-number">{format_number(k.Price)}₫</span>
                            </p>
                            """
            
            thumbnail = thumbnail + f"""
                    <div class="product-resize col-xs-6 col-sm-3 pro-loop" data-id="40776044">
                            <div class="product-block" data-anmation="1">
                                {sale}
                                <div class="product-img image-resize">
                                    <a href="https://cuongpopauth.com/dep-alexander-mcqueen-xanh-reu-663563-w4tm6-3211-p40776044.html"
                                        target="" class="p-img-box added">
                                        <picture>
                                            <source media="(max-width: 767px)"
                                                srcset="{k.photo_1.Photo.url}">
                                            <source media="(min-width: 768px)"
                                                srcset="{k.photo_1.Photo.url}">
                                            <img height="280" width="280" class="img-loop lazyload" data-sizes="auto"
                                                src="https://web.nvnstatic.net/img/lazyLoading.gif?v=3"
                                                data-src="{k.photo_1.Photo.url}"
                                                alt="{k.Name}"
                                                fetchpriority="high">
                                        </picture>
                                        <picture><img class="img-loop img-hover"
                                                src="{k.photo_2.Photo.url}"
                                                alt="{k.photo_2.Photo.url}">
                                        </picture>
                                    </a>
                                    {stock}
                                </div>

                                <div class="product-info">
                                    <div class="product-detail clearfix">
                                        <div class="product-size-cus" psid="40776044">
                                            {size}
                                            </div>
                                        <div class="box-pro-detail">
                                            <h3 class="pro-name">
                                                <a href="https://cuongpopauth.com/dep-alexander-mcqueen-xanh-reu-663563-w4tm6-3211-p40776044.html"
                                                    target="" class="tp_product_name">{k.Name}</a>
                                            </h3>
                                            <div class="box-pro-prices">
                                                {price}
                                            </div>
                                        </div>
                                    </div>

                                    <div class="frameSale">
                                        <div class="activeLabelStatus  icpercent">
                                            {product_saleNew}
                                        </div>
                                    </div>


                                </div>
                                {link}
                            </div>
                        </div>
            """
        html_content=f"""
        {thumbnail}
                     """
        return HttpResponse(html_content, content_type="text/html")
    
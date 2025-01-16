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
def cart_cl(request):
    if request.method == 'GET':
        context = {}
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
        context['Cart_user'] = Cart_user
        Cart_user['total_money'] = format_number(Cart_user['total_money'])
        Cart_user['count'] =  len(Cart_user['data'])
        for i in Cart_user['data']:
            i['product'].Price = format_number(i['product'].Price)
            i['product'].Price_Discount = format_number(i['product'].Price_Discount)              
        
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
        return render(request, 'sleekweb/client/cart.html', context, status=200)

def add_product_cart_cl(request):
    if request.method == 'POST':
        id = request.POST.get('id_product_cart')
        size = request.POST.get('size_product_cart')
        quantity = request.POST.get('quantity')

        # Đảm bảo các tham số bắt buộc được gửi
        if not (id and size and quantity):
            return JsonResponse({'error': 'Thiếu tham số bắt buộc'}, status=400)

        # Tạo đối tượng sản phẩm cần thêm vào giỏ hàng
        obj_add = {'id': id, 'size': size, 'quantity': quantity,'pk':f'{id}_{size}_{quantity}'}
        print('obj_add:',obj_add)

        # Lấy giỏ hàng từ cookie
        cart = request.COOKIES.get('cart', '[]')
        try:
            cart_items = json.loads(cart)  # Chuyển từ JSON thành danh sách
        except json.JSONDecodeError:
            cart_items = []  # Nếu cookie không hợp lệ, giỏ hàng mặc định là rỗng
            
        print('cart_items:',cart_items)

        # Kiểm tra nếu sản phẩm đã tồn tại trong giỏ hàng
        product_exists = False
        for item in cart_items:
            if item['pk'] == f'{id}_{size}_{quantity}':
                product_exists = True
                break

        # Nếu sản phẩm chưa tồn tại, thêm vào giỏ hàng
        if not product_exists:
            cart_items.append(obj_add)

        print('cart_items_1:',cart_items)
        # Tính toán thông tin giỏ hàng
        Cart_user = {'data': [], 'total_quantity': 0, 'total_money': 0}
        print('Cart_user:',Cart_user)
        for i in cart_items:
            try:
                product = Product.objects.get(pk=i['id'])  # Lấy sản phẩm từ database
            except Product.DoesNotExist:
                continue  # Bỏ qua nếu sản phẩm không tồn tại

            obj_cart = {
                'product': product,
                'size': i['size'],
                'quantity': int(i['quantity']),
            }
            Cart_user['data'].append(obj_cart)
        print('Cart_user_1:',Cart_user)
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
            
        print('Cart_user_2:',Cart_user)
        
        product_html = ''
        for i in Cart_user['data']:
            print('thai_photot:',i['product'].product_photo_detail.all().first())
            product_html = product_html+f"""
            <tr class="item_2">
            <td class="img">
                    <a href="/ao-khoac-nike-ngoc-lamxanhtrang-hm0198464-s-p40777530.html">
                        <img class="lazyautosizes ls-is-cached lazyloaded" data-sizes="auto" 
                        src="{i['product'].product_photo_detail.all().first().Photo.url}" 
                        data-src="{i['product'].product_photo_detail.all().first().Photo.url}" 
                        alt="{i['product'].Name} - {i['size']}" sizes="100px">
                    </a>
                                                </td>
                                        <td>
                <a class="pro-title-view" href="">ÁO KHOÁC NIKE NGỌC LAM/XANH/TRẮNG HM0198-464 - {i['size']}</a>
                <span class="pro-price-view">
                    3,500,000                            ₫
                                            <i> x {i['quantity']}</i>

                                                </span>
                <span class="pro-quantity-view">{i['quantity']}</span>
                <span class="remove_link remove-cart removePro">
                <a href="" class="cart_remove_pd" data-pk="{i['product'].id}_{i['size']}_{i['quantity']}">Xóa</a>
            </span>
            </td>
                        </tr>
            """
        # Tạo phản hồi
        html_content = f"""
        <div class="site-nav-container-last">
        <input type="hidden" id="totalCartItems_hidden" value="8">
        
        <p class="title">Giỏ hàng</p>
        <span class="textCartSide">Bạn đang có <b>{Cart_user['count']}</b> sản phẩm trong giỏ hàng.</span>
        <div class="cart-view clearfix">
            <table id="clone-item-cart" class="table-clone-cart">
                <tbody><tr class="item_2 hidden">
                                    <td class="img"><a href="" title=""><img src="" alt="cart"></a></td>
                                    <td>
                        <a class="pro-title-view" href="" title=""></a>
                        <span class="pro-price-view"></span>
                        <span class="variant"></span>
                        <span class="pro-quantity-view"></span>
                        <span class="remove_link remove-cart"></span>
                    </td>
                </tr>
            </tbody></table>
            <table id="cart-view">
                            <tbody>
                            {product_html}
                                </tbody>
                    </table>
            <span class="line"></span>
            <table class="table-total">
                <tbody><tr>
                            </tr>
                <tr>
                    <td class="text-left"><b>TỔNG TIỀN TẠM TÍNH:</b></td>
                    <td class="text-right" id="total-view-cart">
                                                {Cart_user['total_money']}₫
                                        </td>
                </tr>
                        <tr>
                    <td colspan="2"><a href="/cart/checkout" class="checkLimitCart linktocheckout button dark">Tiến hành đặt
                            hàng</a></td>
                </tr>
                <tr>
                    <td colspan="2">
                        <a href="/cart/" class="linktocart button dark">Xem chi tiết giỏ hàng <i class="fa fa-arrow-right"></i></a>
                    </td>
                </tr>
            </tbody></table>
        </div>
        </div>
        """
        response = HttpResponse(html_content, content_type="text/html")

        # Lưu giỏ hàng vào cookie
        response.set_cookie('cart', json.dumps(cart_items), max_age=3600 * 24 * 7)  # Cookie tồn tại 7 ngày

        return response
    
def remove_product_cart_cl(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')

        # Lấy giỏ hàng từ cookie
        cart = request.COOKIES.get('cart', '[]')
        try:
            cart_items = json.loads(cart)  # Chuyển từ JSON thành danh sách
        except json.JSONDecodeError:
            cart_items = []  # Nếu cookie không hợp lệ, giỏ hàng mặc định là rỗng
        print('cart_items:',cart_items)
        # Kiểm tra nếu sản phẩm đã tồn tại trong giỏ hàng
        for item in cart_items:
            if item['pk'] == pk:
                cart_items.remove(item)  # Xóa sản phẩm nếu đã tồn tại
                break
        print('cart_items_dele:',cart_items)
        # Tính toán thông tin giỏ hàng
        Cart_user = {'data': [], 'total_quantity': 0, 'total_money': 0}
        for i in cart_items:
            try:
                product = Product.objects.get(pk=i['id'])  # Lấy sản phẩm từ database
            except Product.DoesNotExist:
                continue  # Bỏ qua nếu sản phẩm không tồn tại

            obj_cart = {
                'product': product,
                'size': i['size'],
                'quantity': int(i['quantity']),
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
                
        product_html = ''
        for i in Cart_user['data']:
            product_html = product_html+f"""
            <tr class="item_2">
            <td class="img">
                    <a href="/ao-khoac-nike-ngoc-lamxanhtrang-hm0198464-s-p40777530.html">
                        <img class="lazyautosizes ls-is-cached lazyloaded" data-sizes="auto" 
                        src="{i['product'].product_photo_detail.all().first().Photo.url}" 
                        data-src="{i['product'].product_photo_detail.all().first().Photo.url}" 
                        alt="{i['product'].Name} - {i['size']}" sizes="100px">
                    </a>
                                                </td>
                                        <td>
                <a class="pro-title-view" href="">ÁO KHOÁC NIKE NGỌC LAM/XANH/TRẮNG HM0198-464 - S</a>
                <span class="pro-price-view">
                    3,500,000                            ₫
                                            <i> x {i['quantity']}</i>

                                                </span>
                <span class="pro-quantity-view">{i['quantity']}</span>
                <span class="remove_link remove-cart removePro">
                <a href="" class="cart_remove_pd" data-pk="{i['product'].id}_{i['size']}_{i['quantity']}">Xóa</a>
            </span>
            </td>
                        </tr>
            """
        # Tạo phản hồi
        html_content = f"""
        <div class="site-nav-container-last">
        <input type="hidden" id="totalCartItems_hidden" value="8">
        
        <p class="title">Giỏ hàng</p>
        <span class="textCartSide">Bạn đang có <b>{Cart_user['count']}</b> sản phẩm trong giỏ hàng.</span>
        <div class="cart-view clearfix">
            <table id="clone-item-cart" class="table-clone-cart">
                <tbody><tr class="item_2 hidden">
                                    <td class="img"><a href="" title=""><img src="" alt="cart"></a></td>
                                    <td>
                        <a class="pro-title-view" href="" title=""></a>
                        <span class="pro-price-view"></span>
                        <span class="variant"></span>
                        <span class="pro-quantity-view"></span>
                        <span class="remove_link remove-cart"></span>
                    </td>
                </tr>
            </tbody></table>
            <table id="cart-view">
                            <tbody>
                            {product_html}
                                </tbody>
                    </table>
            <span class="line"></span>
            <table class="table-total">
                <tbody><tr>
                            </tr>
                <tr>
                    <td class="text-left"><b>TỔNG TIỀN TẠM TÍNH:</b></td>
                    <td class="text-right" id="total-view-cart">
                                                {Cart_user['total_money']}₫
                                        </td>
                </tr>
                        <tr>
                    <td colspan="2"><a href="/cart/checkout" class="checkLimitCart linktocheckout button dark">Tiến hành đặt
                            hàng</a></td>
                </tr>
                <tr>
                    <td colspan="2">
                        <a href="/cart/" class="linktocart button dark">Xem chi tiết giỏ hàng <i class="fa fa-arrow-right"></i></a>
                    </td>
                </tr>
            </tbody></table>
        </div>
        </div>
        """
        response = HttpResponse(html_content, content_type="text/html")

        # Lưu giỏ hàng vào cookie
        response.set_cookie('cart', json.dumps(cart_items), max_age=3600 * 24 * 7)  # Cookie tồn tại 7 ngày

        return response

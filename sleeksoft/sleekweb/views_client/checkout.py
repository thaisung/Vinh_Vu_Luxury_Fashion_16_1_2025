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

def checkout_cl(request):
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
        return render(request, 'sleekweb/client/checkout.html', context, status=200)
    elif request.method == 'POST':
        print('thiijajksdjkg')
        cart = request.COOKIES.get('cart', '[]')
        try:
            cart_items = json.loads(cart)
        except json.JSONDecodeError:
            cart_items = []  # Nếu cookie không hợp lệ, đặt giỏ hàng mặc định là rỗng
        print('cart_items:',cart_items)
        pk = request.POST.get('pk')
        type_quantity = request.POST.get('type_quantity')
        print('pk:',pk)
        print('type_quantity:',type_quantity)
        if type_quantity == 'up':
            for i in cart_items:
                if i['pk'] == pk:
                    i['quantity'] = int(i['quantity']) + 1
        if type_quantity == 'down':
            for i in cart_items:
                if i['pk'] == pk:
                    i['quantity'] = int(i['quantity']) - 1
        print('cart_items:',cart_items)
        page = request.POST.get('page')
        print('page:',page)
        if page == 'cart':
            response = redirect('cart_cl')
        else:
            response = redirect('checkout_cl')
        response.set_cookie('cart', json.dumps(cart_items), max_age=3600 * 24 * 7)  # Cookie tồn tại trong 1 giờ
        return response
    else:
        return redirect('checkout_cl')
    
def delete_pd_checkout_cl(request):
    if request.method == 'POST':
        print('thiijajksdjkg')
        cart = request.COOKIES.get('cart', '[]')
        try:
            cart_items = json.loads(cart)
        except json.JSONDecodeError:
            cart_items = []  # Nếu cookie không hợp lệ, đặt giỏ hàng mặc định là rỗng
        print('cart_items:',cart_items)
        pk = request.POST.get('pk')
        page = request.POST.get('page')
        print('page:',page)
        if pk:
            # Tìm và xóa sản phẩm có `pk` trong giỏ hàng
            cart_items = [item for item in cart_items if item.get('pk') != pk]
        print('cart_items:',cart_items)
        if page == 'cart':
            response = redirect('cart_cl')
        else:
            response = redirect('checkout_cl')
        response.set_cookie('cart', json.dumps(cart_items), max_age=3600 * 24 * 7)  # Cookie tồn tại trong 1 giờ
        return response
    else:
        return redirect('checkout_cl')


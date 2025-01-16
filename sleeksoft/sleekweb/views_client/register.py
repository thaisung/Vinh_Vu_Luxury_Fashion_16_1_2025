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

def register_cl(request):
    if request.method == 'GET':
        context = {}
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
        return render(request, 'sleekweb/client/register.html', context, status=200)
    elif request.method == 'POST':
        Full_name = request.POST.get('Full_name')
        Phone_number = request.POST.get('Phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if Full_name and Phone_number and email and password:
            if User.objects.filter(username=email).exists():
                return JsonResponse({'success': False, 'message': 'Tên người dùng đã tồn tại'})
            elif User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email đã tồn tại'})
            else:
                User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    Phone_number=Phone_number,
                    Full_name=Full_name)
            return JsonResponse({'success': True,'message': 'Đăng ký thành công tài khoản.', 'redirect_url': reverse('login_page_client')})
        else:
            return JsonResponse({'success': False, 'message': 'Điền đầy đủ thông tin trước khi đăng ký.'})
    else:
        return redirect('register_cl')
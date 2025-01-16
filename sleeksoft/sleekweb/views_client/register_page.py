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

def decrypt_rsa(encrypted_data_b64):
    # Ví dụ sử dụng
    private_key_pem = settings.PRIVATE_KEY_PEM
    
    # Tải khóa riêng RSA từ chuỗi PEM
    private_key = RSA.import_key(private_key_pem)

    # Tạo đối tượng giải mã với padding PKCS1
    cipher = PKCS1_v1_5.new(private_key)

    try:
        # Chuyển đổi dữ liệu từ chuỗi base64 về dạng bytes
        encrypted_data_bytes = base64.b64decode(encrypted_data_b64)
        
        # Giải mã dữ liệu
        decrypted_data_bytes = cipher.decrypt(encrypted_data_bytes, None)
        
        # Chuyển đổi dữ liệu giải mã từ bytes về chuỗi
        decrypted_data = decrypted_data_bytes.decode('utf-8')
        
        return decrypted_data
    except:
        return None
    
def check_captcha(recaptcha_response):
    data = {
            'secret': '6Ld9LFsqAAAAAPxaBWkubgmx-1twJu-sKKt6VbpI',  # Thay bằng secret key của bạn
            'response': recaptcha_response
        }  
    # Gửi yêu cầu kiểm tra tới Google
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    check = response.json()
    if check.get('success'):
        return True
    else:
        return False

def register_page_client(request):
    if request.method == 'GET':
        context = {}
        print('context:',context)
        return render(request, 'sleekweb/client/register_page.html', context, status=200)
    elif request.method == 'POST':
        fl = request.POST.get('fl')
        password =  request.POST.get('pw')
        username =  request.POST.get('em')
        email = username
        print('username,password,email: ',username+'/'+password+'/'+email)
        if username is None or password is None or email is None:
            return JsonResponse({'success': False, 'message': 'Hành động đăng nhập của bạn không được chấp nhận.Hãy lên trang chính thức của WEBSITE để đăng ký.'})
        elif not username or not password  or not email:
            return JsonResponse({'success': False, 'message': 'Điền đầy đủ thông tin cần thiết trước khi đăng ký.'})
        else:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Tên người dùng đã tồn tại'})
            elif User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email đã tồn tại'})
            else:
                User.objects.create_user(username=username,email=email,password=password,Full_name=fl)
            return JsonResponse({'success': True,'message': 'Đăng ký thành công tài khoản.', 'redirect_url': reverse('login_page_client')})
    else:
        return redirect('register_page_client')

    

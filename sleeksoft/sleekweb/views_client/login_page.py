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
    


def login_page_client(request):
    if request.method == 'GET':
        context = {}
        context['PUBLIC_KEY_PEM'] = settings.PUBLIC_KEY_PEM
        print('context:',context)
        return render(request, 'sleekweb/client/login_page.html', context, status=200)
    elif request.method == 'POST':
        encrypted_username = request.POST.get('un')
        print('encrypted_username:',encrypted_username)
        encrypted_password = request.POST.get('pw')
        print('encrypted_password:',encrypted_password)
        # Giải mã username và password
        username =  decrypt_rsa(encrypted_username)
        print('username:',username)
        password =  decrypt_rsa(encrypted_password)
        print('password:',password)
        if username is None or password is None:
            return JsonResponse({'success': False, 'message': 'Hành động đăng nhập của bạn không được chấp nhận.Hãy lên trang chính thức của WEBSITE để đăng nhập.'})
        elif not username or not password:
            return JsonResponse({'success': False, 'message': 'Điền đầy đủ thông tin trước khi đăng nhập.'})
        else:
            if User.objects.filter(username=username).exists():
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        if user.is_superuser or user.is_manage:
                            return JsonResponse({'success': True, 'redirect_url': reverse('statistical_page_admin')})
                        else:
                            # Chuyển hướng đến `next` nếu có, hoặc trang mặc định
                            next_url = request.GET.get('next')
                            if next_url:
                                return redirect(next_url)
                            else:
                                return JsonResponse({'success': True, 'redirect_url': reverse('statistical_page_admin')})
                    else:
                        return JsonResponse({'success': False, 'message': 'Tài khoản của bạn đã ngừng hoạt động'})
                else:
                    return JsonResponse({'success': False, 'message': 'Mật khẩu đăng nhập không chính xác'})
            else:
                return JsonResponse({'success': False, 'message': 'Tên tài khoản đăng nhập không chính xác'})
    
def logout_page_client(request):
    logout(request)
    return redirect('login_page_client')

    

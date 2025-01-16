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



    
def reset_pw_send_otp(request):
    if request.method == 'GET':
        context = {}
        print('context:',context)
        return render(request, 'sleekweb/client/change_pw_send_otp.html', context, status=200)
    elif request.method == 'POST':
        un = request.POST.get('un')
        try:
            user = User.objects.get(username = un)
            otp = random.randint(10000000, 99999999)
            user.OTP = otp
            user.save()
            if user:
                email = un
                subject = f'Thông báo từ hệ thống CSKH'
                message = f"""
                <html>
                <body>
                    <p><strong>Mã OTP để lấy lại mật khẩu của bạn là:</strong></p>
                    <p>Mã OTP : {otp}</p>
                </body>
                </html>
                """

                email = EmailMessage(subject, message, to=[email])
                email.content_subtype = "html"  # Đặt định dạng nội dung email là HTML
                email.send()
            return JsonResponse({'success': True, 'redirect_url': reverse('reset_pw_check_otp')})
        except:
            user = None
            return JsonResponse({'success': False, 'message': 'Email không tồn tại.'})
    else:
        return JsonResponse({'success': False, 'message': 'Không tồn tại phương thức.'})
            
def reset_pw_check_otp(request):
    if request.method == 'GET':
        context = {}
        print('context:',context)
        return render(request, 'sleekweb/client/change_pw_check_otp.html', context, status=200)
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
                return JsonResponse({'success': True,'message': 'Đổi mật khẩu thành công tài khoản','redirect_url': reverse('login_page_client')})
            else:
                return JsonResponse({'success': False, 'message': 'Mã OTP không chính xác'})
        except:
            user = None
            return JsonResponse({'success': False, 'message': 'Mã OTP không chính xác'})
    else:
        return JsonResponse({'success': False, 'message': 'Không tồn tại phương thức.'})
    


    

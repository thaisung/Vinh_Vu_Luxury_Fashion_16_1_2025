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

from django.core.mail import send_mail,EmailMessage
from django.conf import settings
import openpyxl

from django.db.models import Count
from django.http import JsonResponse
from django.forms.models import model_to_dict

import tempfile

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.db.models import Case, When, BooleanField


def send_sms(email,subject,message):
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    
def send_email_notification(email, subject, message):
    # Lấy thông tin từ Django settings
    smtp_host = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_user = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD
    use_tls = settings.EMAIL_USE_TLS
    use_ssl = settings.EMAIL_USE_SSL

    # Đảm bảo tiêu đề email là duy nhất
    subject = f"{subject} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # Tạo đối tượng email
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = subject

    # Thêm Message-ID duy nhất
    msg_id = f"<{uuid.uuid4()}@lead.ns.name.vn>"
    msg['Message-ID'] = msg_id

    # Xóa các header liên quan đến chuỗi hội thoại
    if 'In-Reply-To' in msg:
        del msg['In-Reply-To']
    if 'References' in msg:
        del msg['References']

    # Thêm nội dung HTML vào email
    msg.attach(MIMEText(message, 'html'))

    # Kết nối và gửi email
    try:
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port)
            if use_tls:
                server.starttls()

        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, email, msg.as_string())
        server.quit()

        print("Email đã được gửi thành công!")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi gửi email: {e}")

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
            
    Cart_user['Revenue'] = Cart_user['total_money']
    Cart_user['total_money'] = format_number(Cart_user['total_money'])
    Cart_user['count'] =  len(Cart_user['data'])
    for i in Cart_user['data']:
        i['product'].Price = format_number(i['product'].Price)
        i['product'].Price_Discount = format_number(i['product'].Price_Discount)
    return Cart_user

    
def order_detail_ad(request,code):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context = {}
                try:
                    context['obj_order'] = Order.objects.get(Code=code)
                    context['obj_order'].Data = format_cart(context['obj_order'].Data)
                    print('Data:',context['obj_order'].Data)
                    print(context['obj_order'].Data['Revenue'])
                    if not context['obj_order'].Deposit:
                        context['obj_order'].Deposit = 0
                    print(context['obj_order'].Deposit)
                    context['obj_order'].Revenue = int(context['obj_order'].Data['Revenue'])-int(context['obj_order'].Deposit)
                    context['obj_order'].Revenue = format_number(context['obj_order'].Revenue)
                    context['obj_order'].Deposit = format_number(context['obj_order'].Deposit)
                except:
                    return redirect('order_ad')
                return render(request, 'sleekweb/admin/order_detail.html', context, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_ad')
    else:
        return redirect('login_ad')
    
def order_detail_update_ad(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context = {}
                try:
                    Code = request.GET.get('Code')
                    obj_order = Order.objects.get(Code=Code)
                    obj_order.Deposit = ''
                    obj_order.save()
                    return redirect('order_detail_ad',code=Code)
                except:
                    return redirect('order_ad')
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_ad')
    elif request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context = {}
                try:
                    Code = request.POST.get('Code')
                    Deposit = request.POST.get('Deposit')
                    obj_order = Order.objects.get(Code=Code)
                    obj_order.Deposit = Deposit
                    obj_order.save()
                    return redirect('order_detail_ad',code=Code)
                except:
                    return redirect('order_ad')
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_ad')
    else:
        return redirect('login_ad')
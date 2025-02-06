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


def order_ad(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context = {}
                s = request.GET.get('s')
                st = request.GET.get('st')
                p = request.GET.get('p')
                context = {}
                context['list_order'] = Order.objects.all()
                if s:
                    context['list_order'] = context['list_order'].filter(Q(Code__icontains=s)).order_by('-id')
                    context['s'] = s
                if st:
                    context['list_order'] = context['list_order'].filter(Status=st).order_by('-id')
                    context['st'] = st               
                # Sử dụng Paginator để chia nhỏ danh sách (10 là số lượng mục trên mỗi trang)
                paginator = Paginator(context['list_order'], settings.PAGE)

                # Lấy số trang hiện tại từ URL, nếu không mặc định là trang 1
                p = request.GET.get('p')
                page_obj = paginator.get_page(p)
                context['list_order'] = page_obj
                print('list_order:',context['list_order'])
                # Tạo danh sách các số trang
                page_list = list(range(1, paginator.num_pages + 1))
                context['page_list'] = page_list
                return render(request, 'sleekweb/admin/order.html', context, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_ad')
    elif request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff or request.user.is_manage:
                field={}
                field['Source'] = request.POST.get('Source')
                field['Name'] = request.POST.get('Name')
                field['Phone_number'] = return_phone_number(request.POST.get('Phone_number'))
                field['Area'] = request.POST.get('Area')
                field['Product'] = request.POST.get('Product')
                field['Demand'] = request.POST.get('Demand')
                field['Status'] = request.POST.get('Status')
                field['Note'] = request.POST.get('Note')
                Belong_Campaign = request.POST.get('Belong_Campaign')
                Belong_User = request.POST.get('Belong_User')
                print('Belong_User:',Belong_User)                    
                if Belong_Campaign:
                    try:
                        obj_campaign = Campaign.objects.get(pk=Belong_Campaign)
                        try:
                            Order.objects.get(Phone_number=field['Phone_number'],Belong_Campaign=Belong_Campaign)
                            return JsonResponse({'success': False, 'message': 'Số điện thoại trong chiến dịch đã tồn tại.'},json_dumps_params={'ensure_ascii': False})
                        except:
                            print('ok')
                    except:
                        obj_campaign = None
                        return JsonResponse({'success': False, 'message': 'Chiến dịch không tồn tại.'},json_dumps_params={'ensure_ascii': False})
                    if request.user.is_superuser:
                        field['Belong_Campaign'] = obj_campaign
                    if request.user.is_manage:
                        list_campaign = Campaign.objects.filter(Belong_User=request.user)
                        if obj_campaign in list_campaign:
                            field['Belong_Campaign'] = obj_campaign
                        else:
                            return JsonResponse({'success': False, 'message': 'Không thể tạo bản ghi với chiến dịch không thuộc sự quản lý của bạn.'},json_dumps_params={'ensure_ascii': False})
                    if request.user.is_staff and not request.user.is_superuser and not request.user.is_manage :
                        list_campaign = Campaign.objects.filter(Belong_User=request.user)
                        if obj_campaign in list_campaign:
                            field['Belong_Campaign'] = obj_campaign
                        else:
                            return JsonResponse({'success': False, 'message': 'Không thể tạo bản ghi với chiến dịch mà bạn không nằm trong đó.'},json_dumps_params={'ensure_ascii': False})
                if Belong_User == '--Ngẫu nhiên--' and obj_campaign:
                    user_s = obj_campaign.Belong_User.all().annotate(order_count=Count('list_order')).exclude(is_superuser=True).exclude(is_manage=True).order_by('order_count').first()
                    Belong_User = user_s.id
                if Belong_User:
                    try:
                        obj_user = User.objects.get(pk=Belong_User)
                        if  obj_user.is_superuser or obj_user.is_manage:
                            return JsonResponse({'success': False, 'message': 'Không thể phân bổ khách hàng cho quản lý.'},json_dumps_params={'ensure_ascii': False})
                    except:
                        print('jjjjj')
                        obj_user = None
                        return JsonResponse({'success': False, 'message': 'Nhân viên phân công CSKH không tồn tại.'},json_dumps_params={'ensure_ascii': False})
                    if request.user.is_superuser:
                        field['Belong_User'] = obj_user
                    if request.user.is_manage:
                        list_user = User.objects.filter(list_campaign__in=list_campaign).distinct()
                        if obj_user in list_user:
                            field['Belong_User'] = obj_user
                        else:
                            return JsonResponse({'success': False, 'message': 'Không thể tạo bản ghi với nhân viên không thuộc sự quản lý của bạn.'},json_dumps_params={'ensure_ascii': False})
                else:
                    obj_user = None
                    if request.user.is_staff and not request.user.is_superuser and not request.user.is_manage:
                        field['Belong_User'] = request.user
                obj_order = Order.objects.create(**field)
                History.objects.create(history='Tạo mới khách hàng',Belong_Lead=obj_order)
                link_order = reverse('order_page_staff_detail', kwargs={'pk': obj_order.id})
                if obj_user and obj_order:
                    email = obj_user.email
                    subject = f"[{field['Name']}] Đăng ký - TB từ chiến dịch [{field['Belong_Campaign'].Name}]"
                    message_Link_KH = f"""
                    <html>
                    <body>
                        <p><strong>Bạn đã được phân công chăm sóc khách hàng mới [{field['Name']}] :</strong></p>
                        <p>Dự án: {field['Belong_Campaign'].Name}</p>
                        <p>Tên khách hàng: {field['Name']}</p>
                        <p>Số điện thoại: Click <a href="https://lead.ns.name.vn{link_order}" target="_blank" rel="noopener noreferrer" style="text-decoration: underline; color: #0ea5e9;">https://lead.ns.name.vn{link_order}</a></p>
                        <p>Tình trạng: {field['Status']}</p>
                    </body>
                    </html>
                    """
                    message_So_DT = f"""
                    <html>
                    <body>
                        <p><strong>Bạn đã được phân công chăm sóc khách hàng mới [{field['Name']}] :</strong></p>
                        <p>Dự án: {field['Belong_Campaign'].Name}</p>
                        <p>Tên khách hàng: {field['Name']}</p>
                        <p>Số điện thoại: {field['Phone_number']}</p>
                        <p>Tình trạng: {field['Status']}</p>
                    </body>
                    </html>
                    """
                    if obj_campaign.Link_KH:
                        send_email_notification(email, subject, message_Link_KH)
                    else:
                        send_email_notification(email, subject, message_So_DT)
                    # email = EmailMessage(subject, message, to=[email])
                    # email.content_subtype = "html"  # Đặt định dạng nội dung email là HTML
                    # email.send()
                if request.user.is_superuser or request.user.is_manage:
                    return redirect('order_ad')
                if request.user.is_staff and not request.user.is_superuser and not request.user.is_manage:
                    return redirect('order_page_staff')
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_ad')
    else:
        return redirect('login_ad')
    
def update_order_ad(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff or request.user.is_manage:
                id_order_update = request.POST.get('id_order_update')
                obj_order = Order.objects.get(pk=id_order_update)
                obj_user_old = obj_order.Belong_User
                obj_order.Source = request.POST.get('Source')
                obj_order.Name = request.POST.get('Name')
                obj_order.Area = request.POST.get('Area')
                obj_order.Product = request.POST.get('Product')
                obj_order.Demand = request.POST.get('Demand')
                obj_order.Status = request.POST.get('Status')
                obj_order.Note = request.POST.get('Note')
                Belong_Campaign = request.POST.get('Belong_Campaign')
                Belong_User = request.POST.get('Belong_User')
                print(f"""
                    id_order_update: {id_order_update}
                    obj_order: {obj_order}
                    obj_user_old: {obj_user_old}
                    Name: {obj_order.Name}
                    Phone_number: {obj_order.Phone_number}
                    Area: {obj_order.Area}
                    Product: {obj_order.Product}
                    Demand: {obj_order.Demand}
                    Status: {obj_order.Status}
                    Note: {obj_order.Note}
                    Belong_Campaign: {Belong_Campaign}
                    Belong_User: {Belong_User}
                    """)
                if Belong_Campaign:
                    print('obj_order.Phone_number:',obj_order.Phone_number)
                    print('obj_order.Phone_numberád:',return_phone_number(request.POST.get('Phone_number')))
                    if obj_order.Phone_number == return_phone_number(request.POST.get('Phone_number')):
                        obj_order.Phone_number = return_phone_number(request.POST.get('Phone_number'))
                        obj_campaign = Campaign.objects.get(pk=Belong_Campaign)
                        print('1')
                    else:
                        print('2')
                        try:
                            obj_campaign = Campaign.objects.get(pk=Belong_Campaign)
                            dk_phone_number = Order.objects.filter(Phone_number=return_phone_number(request.POST.get('Phone_number')),Belong_Campaign=obj_campaign)
                            if dk_phone_number:
                                return JsonResponse({'success': False, 'message': 'Số điện thoại trong chiến dịch đã tồn tại.'},json_dumps_params={'ensure_ascii': False})
                            else:
                                obj_order.Phone_number = return_phone_number(request.POST.get('Phone_number'))
                        except:
                            return JsonResponse({'success': False, 'message': 'Chiến dịch không tồn tại.'},json_dumps_params={'ensure_ascii': False})
                    if request.user.is_superuser:
                        obj_order.Belong_Campaign = obj_campaign
                    if request.user.is_manage:
                        list_campaign = Campaign.objects.filter(Belong_User=request.user)
                        if obj_campaign in list_campaign:
                            obj_order.Belong_Campaign = obj_campaign
                        else:
                            return JsonResponse({'success': False, 'message': 'Không thể cập nhật bản ghi với chiến dịch không thuộc sự quản lý của bạn.'},json_dumps_params={'ensure_ascii': False})
                    if request.user.is_staff and not request.user.is_superuser:
                        list_campaign = Campaign.objects.filter(Belong_User=request.user)
                        if obj_campaign in list_campaign:
                            obj_order.Belong_Campaign = obj_campaign
                        else:
                            return JsonResponse({'success': False, 'message': 'Không thể cập nhật bản ghi với chiến dịch mà bạn không nằm trong đó.'},json_dumps_params={'ensure_ascii': False})
                if Belong_User == '--Ngẫu nhiên--' and obj_campaign:
                    user_s = obj_campaign.Belong_User.all().annotate(order_count=Count('list_order')).exclude(is_superuser=True).exclude(is_manage=True).order_by('order_count').first()
                    Belong_User = user_s.id
                if Belong_User:
                    try:
                        obj_user = User.objects.get(pk=Belong_User)
                        if  obj_user.is_superuser or obj_user.is_manage:
                            return JsonResponse({'success': False, 'message': 'Không thể phân bổ khách hàng cho quản lý.'},json_dumps_params={'ensure_ascii': False})
                    except:
                        return JsonResponse({'success': False, 'message': 'Nhân viên phân công CSKH không tồn tại.'},json_dumps_params={'ensure_ascii': False})
                    if request.user.is_superuser:
                        obj_order.Belong_User = obj_user
                    if request.user.is_manage:
                        list_user = User.objects.filter(list_campaign__in=list_campaign).distinct()
                        if obj_user in list_user:
                            obj_order.Belong_User = obj_user
                        else:
                            return JsonResponse({'success': False, 'message': 'Không thể cập nhật bản ghi với nhân viên không thuộc sự quản lý của bạn.'},json_dumps_params={'ensure_ascii': False})
                    if request.user.is_staff and not request.user.is_superuser:
                        obj_order.Belong_User = request.user
                obj_order.save()
                History.objects.create(history='Cập nhật dữ liệu khách hàng',Belong_Lead=obj_order)
                link_order = reverse('order_page_staff_detail', kwargs={'pk': obj_order.id})
                if request.user.is_superuser or request.user.is_manage:
                    if obj_user_old and  int(obj_user_old.id) != int(obj_user.id):
                        if obj_user:
                            print('EMAIL_HOST:',settings.EMAIL_HOST)
                            print('EMAIL_HOST_USER:',settings.EMAIL_HOST_USER)
                            email = obj_user.email
                            subject = f"[{request.POST.get('Name')}] Đăng ký - TB từ chiến dịch [{Campaign.objects.get(pk=Belong_Campaign).Name}]"
                            message_Link_KH = f"""
                            <html>
                            <body>
                                <p><strong>Bạn đã được phân công chăm sóc khách hàng mới [{request.POST.get('Name')}] :</strong></p>
                                <p>Dự án: {Campaign.objects.get(pk=Belong_Campaign).Name}</p>
                                <p>Tên khách hàng: {request.POST.get('Name')}</p>
                                <p>Số điện thoại: Click <a href="https://lead.ns.name.vn{link_order}" target="_blank" rel="noopener noreferrer" style="text-decoration: underline; color: #0ea5e9;">https://lead.ns.name.vn{link_order}</a></p>
                                <p>Tình trạng: {request.POST.get('Status')}</p>
                                <p>Ghi chú: {request.POST.get('Note')}</p>
                            </body>
                            </html>
                            """
                            message_So_DT = f"""
                            <html>
                            <body>
                                <p><strong>Bạn đã được phân công chăm sóc khách hàng mới [{request.POST.get('Name')}] :</strong></p>
                                <p>Dự án: {Campaign.objects.get(pk=Belong_Campaign).Name}</p>
                                <p>Tên khách hàng: {request.POST.get('Name')}</p>
                                <p>Số điện thoại: {request.POST.get('Phone_number')}</p>
                                <p>Tình trạng: {request.POST.get('Status')}</p>
                                <p>Ghi chú: {request.POST.get('Note')}</p>
                            </body>
                            </html>
                            """
                            if obj_campaign.Link_KH:
                                send_email_notification(email, subject, message_Link_KH)
                            else:
                                send_email_notification(email, subject, message_So_DT)
                            # email = EmailMessage(subject, message, to=[email])
                            # email.content_subtype = "html"  # Đặt định dạng nội dung email là HTML
                            # email.send()
                    return redirect('order_ad')
                if request.user.is_staff and not request.user.is_superuser:
                    return redirect('order_page_staff')
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_ad')
    else:
        return redirect('login_ad')

def delete_check_list_order_ad(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser :
                data = json.loads(request.body)
                print('data:',data)
                check_list  = json.loads(data.get('check_list'))
                text_check_list = data.get('text_check_list')
                if text_check_list == 'Tôi đồng ý xóa danh sách đơn hàng đã chọn':
                    Order.objects.filter(id__in=check_list).delete()
                    return JsonResponse({'success': True, 'redirect_url': reverse('order_ad')},json_dumps_params={'ensure_ascii': False})
                else:
                    return JsonResponse({'success': False, 'message': 'Nội dung nhập chưa chính xác'},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Tài khoản của bạn chưa được cấp quyền để thực hiện chức năng này'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_ad')
    else:
        return redirect('user_page_admin')


def update_status_order(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        id = request.POST.get('id')
        obj_order = Order.objects.get(pk=id)
        obj_order.Status = status
        obj_order.save()
        return redirect('order_ad')
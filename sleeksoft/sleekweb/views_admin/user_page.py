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

from django.db.models import Count, Q

import datetime

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

from django.forms.models import model_to_dict


def user_page_admin(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                s = request.GET.get('s')
                f = request.GET.get('f')
                context = {}
                context['list_user'] = User.objects.all().order_by('-id')
                for user in context['list_user']:
                    user.pending_orders_count = Order.objects.filter(Belong_User=user, Status='Chờ xác nhận').count()
                if s:
                    context['list_user'] = context['list_user'].filter(Q(Full_name__icontains=s)| Q(email__icontains=s)).order_by('-id')
                    context['s'] = s
                if f:
                    if f=="1":
                        context['list_user'] = context['list_user'].filter(Q(is_staff=True) | Q(is_manage=True) | Q(is_superuser=True)).order_by('-id')
                    else:
                        context['list_user'] = context['list_user'].filter(Q(is_staff=False) & Q(is_manage=False)).order_by('-id')
                    context['f'] = f                
                # Sử dụng Paginator để chia nhỏ danh sách (10 là số lượng mục trên mỗi trang)
                paginator = Paginator(context['list_user'], settings.PAGE)

                # Lấy số trang hiện tại từ URL, nếu không mặc định là trang 1
                p = request.GET.get('p')
                page_obj = paginator.get_page(p)
                context['list_user'] = page_obj
                # Tạo danh sách các số trang
                page_list = list(range(1, paginator.num_pages + 1))
                context['page_list'] = page_list
                return render(request, 'sleekweb/admin/user_page.html', context, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    # elif request.method == 'POST':
    #     if request.user.is_authenticated:
    #         if request.user.is_superuser:
    #             is_user_update = request.POST.get('is_user_update')
    #             id_user_update = request.POST.get('id_user_update')
    #             if is_user_update and id_user_update:
    #                 try:
    #                     obj_user = User.objects.get(pk=int(id_user_update))
    #                     if is_user_update == 'is_manage':
    #                         obj_user.is_manage = True
    #                         obj_user.is_staff = False
    #                     if is_user_update == 'is_staff':
    #                         obj_user.is_staff = True
    #                         obj_user.is_manage = False
    #                     obj_user.save()
    #                     return redirect('user_page_admin')
    #                 except:
    #                     return JsonResponse({'success': False, 'message': 'Tài khoản không tồn tại'},json_dumps_params={'ensure_ascii': False})
    #             else:  
    #                 Full_name =  request.POST.get('fl')
    #                 is_user =  request.POST.get('is_user')
    #                 password =  request.POST.get('pw')
    #                 username =  request.POST.get('em')
    #                 email = username
    #                 if username is None or password is None or email is None:
    #                     return JsonResponse({'success': False, 'message': 'Hành động đăng nhập của bạn không được chấp nhận.Hãy lên trang chính thức của WEBSITE để đăng ký.'},json_dumps_params={'ensure_ascii': False})
    #                 elif not username or not password  or not email:
    #                     return JsonResponse({'success': False, 'message': 'Điền đầy đủ thông tin cần thiết trước khi đăng ký.'},json_dumps_params={'ensure_ascii': False})
    #                 else:
    #                     if User.objects.filter(username=username).exists():
    #                         return JsonResponse({'success': False, 'message': 'Tên người dùng đã tồn tại'},json_dumps_params={'ensure_ascii': False})
    #                     elif User.objects.filter(email=email).exists():
    #                         return JsonResponse({'success': False, 'message': 'Email đã tồn tại'},json_dumps_params={'ensure_ascii': False})
    #                     else:
    #                         if is_user == 'is_manage':
    #                             User.objects.create_user(username=username,email=email,password=password,Full_name=Full_name,is_manage=True)
    #                         if is_user == 'is_staff':
    #                             User.objects.create_user(username=username,email=email,password=password,Full_name=Full_name,is_staff=True)
    #                     return JsonResponse({'success': True,'message': 'Đăng ký thành công tài khoản.', 'redirect_url': reverse('user_page_admin')},json_dumps_params={'ensure_ascii': False})
    #         if request.user.is_manage:
    #             Full_name =  request.POST.get('fl')
    #             password =  request.POST.get('pw')
    #             username =  request.POST.get('em')
    #             email = username
    #             if username is None or password is None or email is None:
    #                 return JsonResponse({'success': False, 'message': 'Hành động đăng nhập của bạn không được chấp nhận.Hãy lên trang chính thức của WEBSITE để đăng ký.'},json_dumps_params={'ensure_ascii': False})
    #             elif not username or not password  or not email:
    #                 return JsonResponse({'success': False, 'message': 'Điền đầy đủ thông tin cần thiết trước khi đăng ký.'},json_dumps_params={'ensure_ascii': False})
    #             else:
    #                 if User.objects.filter(username=username).exists():
    #                     return JsonResponse({'success': False, 'message': 'Tên người dùng đã tồn tại'},json_dumps_params={'ensure_ascii': False})
    #                 elif User.objects.filter(email=email).exists():
    #                     return JsonResponse({'success': False, 'message': 'Email đã tồn tại'},json_dumps_params={'ensure_ascii': False})
    #                 else:
    #                     Belong_Campaign = request.POST.get('Belong_Campaign')
    #                     obj_user = User.objects.create_user(username=username,email=email,password=password,Full_name=Full_name,is_staff=True)
    #                     obj_campaign = Campaign.objects.get(pk=Belong_Campaign)
    #                     obj_campaign.Belong_User.add(obj_user)
    #                 return JsonResponse({'success': True,'message': 'Đăng ký thành công tài khoản.', 'redirect_url': reverse('user_page_admin')},json_dumps_params={'ensure_ascii': False})
    #         else:
    #             return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
    #     else:
    #         return redirect('login_page_client')
    else:
        return redirect('user_page_admin')
    
def delete_check_list_user_admin(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                data = json.loads(request.body)
                print('data:',data)
                check_list  = json.loads(data.get('check_list'))
                text_check_list = data.get('text_check_list')
                if request.user.is_authenticated:
                    if request.user.is_superuser or request.user.is_staff:
                        if text_check_list == 'Tôi đồng ý xóa danh sách tài khoản đã chọn':
                            User.objects.filter(id__in=check_list).exclude(is_superuser=True).delete()
                            return JsonResponse({'success': True, 'redirect_url': reverse('user_page_admin')},json_dumps_params={'ensure_ascii': False})
                        else:
                            return JsonResponse({'success': False, 'message': 'Nội dung nhập chưa chính xác'},json_dumps_params={'ensure_ascii': False})
                    else:
                        return JsonResponse({'success': False, 'message': 'Tài khoản của bạn chưa được cấp quyền để thực hiện chức năng này'},json_dumps_params={'ensure_ascii': False})
                else:
                    return JsonResponse({'success': False, 'message': 'Đăng nhập tài khoản để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
                return redirect('login_page_client')
    else:
        return redirect('user_page_admin')
   
    
def change_password_user_page_admin(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_manage:
                id_user_change_password = request.POST.get('id_user_change_password')
                new_password_user = request.POST.get('new_password_user')
                obj = User.objects.get(pk=id_user_change_password)
                obj.set_password(new_password_user)
                obj.save()
                update_session_auth_hash(request, obj)
                return JsonResponse({'success': True, 'message': 'Đổi mật khẩu thành công'},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('login_page_client')
    
def change_password_user_auth_page_admin(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            pwn = request.POST.get('pwn')
            obj = request.user
            obj.set_password(pwn)
            obj.save()
            update_session_auth_hash(request, obj)
            return JsonResponse({'success': True, 'message': 'Đổi mật khẩu thành công'})
        else:
            return redirect('login_page_client')
    else:
        return redirect('login_page_client')
    
def approve_user_page_admin(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                id_user_approve = request.POST.get('id_user_approve')
                is_user = request.POST.get('is_user')
                obj = User.objects.get(pk=id_user_approve)
                if is_user == 'is_manage':
                    obj.is_manage = True
                elif is_user == 'is_staff':
                    obj.is_staff = True
                obj.save()
                return JsonResponse({'success': True, 'message': 'Phê duyệt thành công','redirect_url': reverse('user_page_admin')},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('login_page_client')
    
    
def reset_user_lead_admin(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                id_reset_user_lead = request.POST.get('id_reset_user_lead')
                text_reser_user_lead = request.POST.get('text_reser_user_lead')
                obj_user = User.objects.get(pk=id_reset_user_lead)
                if text_reser_user_lead == 'Tôi đồng ý':
                    obj_user.list_lead.update(Belong_User=None)
                    obj_user.list_campaign.clear()
                    return JsonResponse({'success': True, 'message': 'Làm mới tài khoản thành công','redirect_url': reverse('user_page_admin')},json_dumps_params={'ensure_ascii': False})
                else:
                    return JsonResponse({'success': False, 'message': 'Nội dung nhập chưa chính xác','redirect_url': reverse('user_page_admin')},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('login_page_client')
    



    
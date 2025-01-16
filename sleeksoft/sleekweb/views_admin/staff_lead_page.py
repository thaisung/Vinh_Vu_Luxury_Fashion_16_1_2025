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

from django.db.models import Count
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import datetime, timezone, timedelta
from django.utils.http import urlencode

def lead_page_staff_detail(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_staff:
                context = {}
                list_Select_setting = Select_setting.objects.all()
                if list_Select_setting:
                    obj = list_Select_setting[0]
                    context['Select_setting'] = {
                        "Area": [item.strip() for item in obj.Area.split('\n') if item.strip()],
                        "Product": [item.strip() for item in obj.Product.split('\n') if item.strip()],
                        "Demand": [item.strip() for item in obj.Demand.split('\n') if item.strip()],
                        "Source": [item.strip() for item in obj.Source.split('\n') if item.strip()],
                    }
                    print('contextSelect_setting:', context['Select_setting'])
                else:
                    context['Select_setting'] = ''
                context['list_campaign'] = Campaign.objects.filter(Belong_User=request.user)
                list_lead = Lead.objects.filter(Belong_User=request.user)
                obj_lead = Lead.objects.get(pk=pk)
                if obj_lead in list_lead:
                    context['obj_lead'] = obj_lead
                    return render(request, 'sleekweb/admin/staff_lead_page_detail.html', context, status=200)
                else:
                    return JsonResponse({'success': False, 'message': 'Bạn không thể truy cập khách hàng không thuộc sự chăm sóc của bạn.'}, json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'}, json_dumps_params={'ensure_ascii': False})
        else:
            # Redirect đến trang đăng nhập với URL quay lại
            query_string = urlencode({'next': request.path})
            login_url = f"{reverse('login_page_client')}?{query_string}"
            return redirect(login_url)


def send_sms(email,subject,message):
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])

def lead_page_staff(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_staff:
                context = {}
                s = request.GET.get('s')
                f = request.GET.get('f')
                st = request.GET.get('st')
                f1 = request.GET.get('f1')
                f2 = request.GET.get('f2')
                list_Select_setting = Select_setting.objects.all()
                if list_Select_setting:
                    obj = list_Select_setting[0]
                    context['Select_setting'] = {
                        "Area": [item.strip() for item in obj.Area.split('\n') if item.strip()],
                        "Product": [item.strip() for item in obj.Product.split('\n') if item.strip()],
                        "Demand": [item.strip() for item in obj.Demand.split('\n') if item.strip()],
                        "Source": [item.strip() for item in obj.Source.split('\n') if item.strip()],
                    }
                    print('contextSelect_setting:',context['Select_setting'])
                else:
                    context['Select_setting'] = ''
                context['list_campaign'] = Campaign.objects.filter(Belong_User=request.user)
                context['list_lead'] = Lead.objects.filter(Belong_User=request.user).order_by('-id')
                if s:
                    context['list_lead'] = context['list_lead'].filter(Q(Name__icontains=s)).order_by('-id')
                    context['s'] = s
                if f:
                    Belong_Campaign = Campaign.objects.get(pk=f)
                    context['list_lead'] = context['list_lead'].filter(Belong_Campaign=Belong_Campaign).order_by('-id')
                    context['f'] = int(f)
                if st:
                    context['list_lead'] = context['list_lead'].filter(Status_lead=st).order_by('-id')
                    context['st'] = st
                if f1:
                    if f1 == '0':
                        context['list_lead'] = context['list_lead'].annotate(num_report=Count('list_report')).filter(num_report=0).order_by('-id')
                        context['f1'] = int(f1)
                    if f1 == '1':
                        context['list_lead'] = context['list_lead'].annotate(num_report=Count('list_report')).filter(num_report__gt=0).order_by('-id')
                        context['f1'] = int(f1)
                if f2:
                    if f2 == '0':
                        context['list_lead'] = context['list_lead'].annotate(num_history=Count('list_history')).filter(num_history=0).order_by('-id')
                        context['f2'] = int(f2)
                    if f2 == '1':
                        context['list_lead'] = context['list_lead'].annotate(num_history=Count('list_history')).filter(num_history__gt=0).order_by('-id')
                        context['f2'] = int(f2)
                        
                # Sử dụng Paginator để chia nhỏ danh sách (10 là số lượng mục trên mỗi trang)
                paginator = Paginator(context['list_lead'], settings.PAGE)

                # Lấy số trang hiện tại từ URL, nếu không mặc định là trang 1
                p = request.GET.get('p')
                page_obj = paginator.get_page(p)
                context['list_lead'] = page_obj
                # Tạo danh sách các số trang
                page_list = list(range(1, paginator.num_pages + 1))
                context['page_list'] = page_list
                return render(request, 'sleekweb/admin/staff_lead_page.html', context, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('login_page_client')
   
def lead_update_report_history_page_staff(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_staff:
                id_lead_update_report = request.POST.get('id_lead_update_report')
                id_lead_update_history = request.POST.get('id_lead_update_history')
                report = request.POST.get('report_update')
                history = request.POST.get('history_update')
                print(f"id_lead_update_report: {id_lead_update_report}")
                print(f"id_lead_update_history: {id_lead_update_history}")
                print(f"Report: {report}")
                print(f"History: {history}")
                if id_lead_update_report:
                    obj_lead = Lead.objects.get(pk=id_lead_update_report,Belong_User=request.user)
                    Report.objects.create(report=report,Belong_Lead=obj_lead)
                if id_lead_update_history:
                    obj_lead = Lead.objects.get(pk=id_lead_update_history,Belong_User=request.user)
                    History.objects.create(history=history,Belong_Lead=obj_lead)
                return redirect('lead_page_staff')
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('login_page_client')
    
def lead_page_staff_detail(request,pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_staff:
                context = {}
                list_Select_setting = Select_setting.objects.all()
                if list_Select_setting:
                    obj = list_Select_setting[0]
                    context['Select_setting'] = {
                        "Area": [item.strip() for item in obj.Area.split('\n') if item.strip()],
                        "Product": [item.strip() for item in obj.Product.split('\n') if item.strip()],
                        "Demand": [item.strip() for item in obj.Demand.split('\n') if item.strip()],
                        "Source": [item.strip() for item in obj.Source.split('\n') if item.strip()],
                    }
                    print('contextSelect_setting:',context['Select_setting'])
                else:
                    context['Select_setting'] = ''
                context['list_campaign'] = Campaign.objects.filter(Belong_User=request.user)
                list_lead = Lead.objects.filter(Belong_User=request.user)
                obj_lead = Lead.objects.get(pk=pk)
                if obj_lead in list_lead:
                    context['obj_lead'] = Lead.objects.get(pk=pk)
                    return render(request, 'sleekweb/admin/staff_lead_page_detail.html', context, status=200)
                else:
                    return JsonResponse({'success': False, 'message': 'Bạn không thể truy cập khách hàng không thuộc sự chăm sóc của bạn.'},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            # Redirect đến trang đăng nhập với URL quay lại
            query_string = urlencode({'next': request.path})
            login_url = f"{reverse('login_page_client')}?{query_string}"
            return redirect(login_url)
    if request.method == 'POST':
        list_lead = Lead.objects.filter(Belong_User=request.user)
        obj_lead = Lead.objects.get(pk=pk)
        if obj_lead in list_lead:
            obj_lead.Name = request.POST.get('Name')
            obj_lead.Phone_number = request.POST.get('Phone_number')
            obj_lead.Area = request.POST.get('Area')
            obj_lead.Product = request.POST.get('Product')
            obj_lead.Demand = request.POST.get('Demand')
            obj_lead.Status_lead = request.POST.get('Status_lead')
            print('Status_lead:',request.POST.get('Status_lead'))
            if obj_lead.Status_lead == 'Chưa tư vấn':
                obj_lead.Status = 'Khách hàng mới'
            else:
                obj_lead.Status = 'Khách hàng cũ'
            
            # Belong_Campaign = request.POST.get('Belong_Campaign')
            
            # try:
            #     Belong_Campaign = Campaign.objects.get(pk=Belong_Campaign)
            # except:
            #     return JsonResponse({'success': False, 'message': 'Chiến dịch cập nhật không tồn tại.'},json_dumps_params={'ensure_ascii': False})
            
            # list_campaign = Campaign.objects.filter(Belong_User=request.user)
            # if Belong_Campaign in list_campaign:
            #     obj_lead.Belong_Campaign = Belong_Campaign
            # else:
            #     return JsonResponse({'success': False, 'message': 'Không thể cập nhật chiến dịch mà bạn không nằm trong đó.'},json_dumps_params={'ensure_ascii': False})
            obj_lead.save()
            
            report = request.POST.get('report')
            
            if report:
                Report.objects.create(report=report,Belong_Lead=obj_lead)
            
            return redirect('lead_page_staff_detail',pk=pk)
        else:
            return JsonResponse({'success': False, 'message': 'Bạn không thể cập nhật khách hàng không thuộc sự chăm sóc của bạn.'},json_dumps_params={'ensure_ascii': False})
    else:
        return redirect('login_page_client')
    
def lead_update_Status_lead_page_staff(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_staff:
                id_lead_update_st = request.POST.get('id_lead_update_st')
                st = request.POST.get('st')
                print(f'{id_lead_update_st}/{st}')
                obj_lead = Lead.objects.get(pk=id_lead_update_st,Belong_User=request.user)
                obj_lead.Status_lead = st
                obj_lead.Status = 'Khách hàng cũ'
                obj_lead.save()
                return redirect('lead_page_staff')
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('login_page_client')


def get_list_report_history(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_manage or request.user.is_staff:
                id_lead_report_history = request.GET.get('id_lead_report_history')
                print('id_lead_report_history:',id_lead_report_history)
                type_get = request.GET.get('type_get')
                obj = Lead.objects.get(pk=id_lead_report_history)
                if obj:
                    if type_get == 'Report':
                        # Múi giờ Hồ Chí Minh (GMT+7)
                        hcm_tz = timezone(timedelta(hours=7))
                        list_data = list(obj.list_report.all().values('report', 'Creation_time'))
                        # Chuyển đổi Creation_time trong list_data
                        for item in list_data:
                            if 'Creation_time' in item and item['Creation_time']:
                                # Chuyển đổi sang thời gian UTC trước (nếu Creation_time là datetime không có timezone)
                                creation_time_utc = item['Creation_time'].replace(tzinfo=timezone.utc)
                                # Sau đó chuyển sang múi giờ Hồ Chí Minh
                                creation_time_hcm = creation_time_utc.astimezone(hcm_tz)
                                # Định dạng lại thời gian
                                item['Creation_time'] = creation_time_hcm.strftime("%d-%m-%Y %H:%M")
                        print('list_data:',list_data)
                    if type_get == 'History':
                        # Múi giờ Hồ Chí Minh (GMT+7)
                        hcm_tz = timezone(timedelta(hours=7))
                        list_data = list(obj.list_history.all().values('history','Creation_time'))
                        # Chuyển đổi Creation_time trong list_data
                        for item in list_data:
                            if 'Creation_time' in item and item['Creation_time']:
                                # Chuyển đổi sang thời gian UTC trước (nếu Creation_time là datetime không có timezone)
                                creation_time_utc = item['Creation_time'].replace(tzinfo=timezone.utc)
                                # Sau đó chuyển sang múi giờ Hồ Chí Minh
                                creation_time_hcm = creation_time_utc.astimezone(hcm_tz)
                                # Định dạng lại thời gian
                                item['Creation_time'] = creation_time_hcm.strftime("%d-%m-%Y %H:%M")
                        # Chuyển đổi đối tượng thành dict
                        print('list_data:',list_data)
                    # Trả về dữ liệu dưới dạng JSON
                    return JsonResponse({'success': True, 'data': list_data},json_dumps_params={'ensure_ascii': False})
                else:
                    return JsonResponse({'success': False, 'data': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
            else:
                    return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return JsonResponse({'success': False, 'message': 'Không tồn tại phương thức này'},json_dumps_params={'ensure_ascii': False})





    

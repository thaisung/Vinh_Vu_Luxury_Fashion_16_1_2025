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
from django.db.models.functions import ExtractWeek,ExtractQuarter
import calendar

def statistical_page_admin(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context = {}
                
                context['number_campaign'] = Campaign.objects.all().count()
                context['number_lead'] = Lead.objects.all().count()
                context['number_user'] = User.objects.all().count()
                context['number_user_approve'] = User.objects.all().filter(Q(is_staff=True)|Q(is_manage=True)|Q(is_superuser=True)).count()
                context['number_user_not_approve'] = User.objects.all().filter(Q(is_staff=False)&Q(is_manage=False)).count()
                
                context['months'] = range(1, 13)
                context['years'] = range(2024, 2031)
                context['weeks'] = range(1, 5)
                context['years'] = range(2024, 2031)
                context['quarters'] = range(1, 5)
                f = request.GET.get('f')
                context['List_Campaign'] = Campaign.objects.all().annotate(
                    lead_count=Count('list_campaign')
                ).order_by('-id').order_by('-id')
                
                d = request.GET.get('d')
                m = request.GET.get('m')
                y = request.GET.get('y')
                w = request.GET.get('w')
                q = request.GET.get('q')
                
                if y and m:
                    days_in_month = calendar.monthrange(int(y), int(m))[1]
                    context['days'] = range(1, days_in_month + 1)
                # List_Lead = Lead.objects.filter(Belong_Campaign__in=context['List_Campaign'])
                if not f:
                    List_Lead = Lead.objects.all()
                    print('List_Lead:',List_Lead)
                    context['List_Lead_CTV'] = List_Lead.filter(Status_lead='Chưa tư vấn').count()
                    context['List_Lead_DTV'] = List_Lead.filter(Status_lead='Đã tư vấn').count()
                    context['List_Lead_GTT'] = List_Lead.filter(Status_lead='Gửi thông tin').count()
                    context['List_Lead_DXDA'] = List_Lead.filter(Status_lead='Đã xem dự án').count()
                    context['List_Lead_KHKTN'] = List_Lead.filter(Status_lead='KH không tiềm năng').count()
                    context['List_Lead_KHDB'] = List_Lead.filter(Status_lead='KH Đã booking').count()
                    context['List_Lead_KHDXNM'] = List_Lead.filter(Status_lead='KH đã xem nhà mẫu').count()
                    context['List_Lead_KHTN'] = List_Lead.filter(Status_lead='KH tiềm năng').count()
                    context['List_Lead_KHDM'] = List_Lead.filter(Status_lead='KH Đã mua').count()
                else:
                    try:
                        context['f'] = int(f)
                        obj_Campaign = Campaign.objects.get(pk=f)
                        context['obj_Campaign'] = obj_Campaign
                        List_Lead = Lead.objects.filter(Belong_Campaign=obj_Campaign)
                        
                        if y:
                            List_Lead = List_Lead.filter(Creation_time__year=y)
                            context['y'] = int(y)
                        if m:
                            List_Lead = List_Lead.filter(Creation_time__month=m)
                            context['m'] = int(m)
                        if d:
                            List_Lead = List_Lead.filter(Creation_time__day=d)
                            context['d'] = int(d)
                        if y and m and w:
                            List_Lead = List_Lead.filter(
                                Creation_time__year=y,  # Năm 2023
                                Creation_time__month=m     # Tháng 1
                            ).annotate(
                                week=ExtractWeek('Creation_time')
                            ).filter(week=w)  # Tuần 1
                            context['w'] = int(w)
                            context['m'] = int(m)
                            context['y'] = int(y)
                        if y and q:
                            List_Lead = List_Lead.annotate(quarter=ExtractQuarter('Creation_time')).filter(
                                Creation_time__year=y,
                                quarter=q  # Quý 2
                            )
                            context['y'] = int(y)
                            context['q'] = int(q)
                        
                        context['List_Lead_CTV'] = List_Lead.filter(Status_lead='Chưa tư vấn').count()
                        context['List_Lead_DTV'] = List_Lead.filter(Status_lead='Đã tư vấn').count()
                        context['List_Lead_GTT'] = List_Lead.filter(Status_lead='Gửi thông tin').count()
                        context['List_Lead_DXDA'] = List_Lead.filter(Status_lead='Đã xem dự án').count()
                        context['List_Lead_KHKTN'] = List_Lead.filter(Status_lead='KH không tiềm năng').count()
                        context['List_Lead_KHDB'] = List_Lead.filter(Status_lead='KH Đã booking').count()
                        context['List_Lead_KHDXNM'] = List_Lead.filter(Status_lead='KH đã xem nhà mẫu').count()
                        context['List_Lead_KHTN'] = List_Lead.filter(Status_lead='KH tiềm năng').count()
                        context['List_Lead_KHDM'] = List_Lead.filter(Status_lead='KH Đã mua').count()
                    except:
                        context['f'] = ''
                print('context:',context)
                return render(request, 'sleekweb/admin/statistical_page.html', context, status=200)
                # Sử dụng Paginator để chia nhỏ danh sách (10 là số lượng mục trên mỗi trang)
                # paginator = Paginator(context['list_user'], settings.PAGE)

                # # Lấy số trang hiện tại từ URL, nếu không mặc định là trang 1
                # p = request.GET.get('p')
                # page_obj = paginator.get_page(p)
                # context['list_user'] = page_obj
                # # Tạo danh sách các số trang
                # page_list = list(range(1, paginator.num_pages + 1))
                # context['page_list'] = page_list
                
            elif request.user.is_manage:
                context = {}
                
                list_campaign = Campaign.objects.filter(Belong_User=request.user)
                context['number_campaign'] = list_campaign.count()
                context['number_lead'] = Lead.objects.filter(Belong_Campaign__in=list_campaign).count()
                list_user = User.objects.filter(list_campaign__in=list_campaign).distinct().exclude(is_superuser=True)
                context['number_user'] = list_user.count()
                context['number_user_approve'] = list_user.filter(Q(is_staff=True) | Q(is_manage=True)).count()
                context['number_user_not_approve'] = list_user.filter(Q(is_staff=True) & Q(is_manage=True)).count()
                
                context['months'] = range(1, 13)
                context['years'] = range(2024, 2031)
                context['weeks'] = range(1, 5)
                context['years'] = range(2024, 2031)
                context['quarters'] = range(1, 5)
                f = request.GET.get('f')
                context['List_Campaign'] = Campaign.objects.filter(Belong_User=request.user).annotate(
                    lead_count=Count('list_campaign')
                ).order_by('-id').order_by('-id')
                
                d = request.GET.get('d')
                m = request.GET.get('m')
                y = request.GET.get('y')
                w = request.GET.get('w')
                q = request.GET.get('q')
                
                if y and m:
                    days_in_month = calendar.monthrange(int(y), int(m))[1]
                    context['days'] = range(1, days_in_month + 1)
                # List_Lead = Lead.objects.filter(Belong_Campaign__in=context['List_Campaign'])
                if not f:
                    List_Lead = Lead.objects.filter(Belong_Campaign__in=context['List_Campaign'])
                    print('List_Lead:',List_Lead)
                    context['List_Lead_CTV'] = List_Lead.filter(Status_lead='Chưa tư vấn').count()
                    context['List_Lead_DTV'] = List_Lead.filter(Status_lead='Đã tư vấn').count()
                    context['List_Lead_GTT'] = List_Lead.filter(Status_lead='Gửi thông tin').count()
                    context['List_Lead_DXDA'] = List_Lead.filter(Status_lead='Đã xem dự án').count()
                    context['List_Lead_KHKTN'] = List_Lead.filter(Status_lead='KH không tiềm năng').count()
                    context['List_Lead_KHDB'] = List_Lead.filter(Status_lead='KH Đã booking').count()
                    context['List_Lead_KHDXNM'] = List_Lead.filter(Status_lead='KH đã xem nhà mẫu').count()
                    context['List_Lead_KHTN'] = List_Lead.filter(Status_lead='KH tiềm năng').count()
                    context['List_Lead_KHDM'] = List_Lead.filter(Status_lead='KH Đã mua').count()
                else:
                    try:
                        context['f'] = int(f)
                        obj_Campaign = Campaign.objects.get(pk=f)
                        context['obj_Campaign'] = obj_Campaign
                        List_Lead = Lead.objects.filter(Belong_Campaign=obj_Campaign)
                        
                        if y:
                            List_Lead = List_Lead.filter(Creation_time__year=y)
                            context['y'] = int(y)
                        if m:
                            List_Lead = List_Lead.filter(Creation_time__month=m)
                            context['m'] = int(m)
                        if d:
                            List_Lead = List_Lead.filter(Creation_time__day=d)
                            context['d'] = int(d)
                        if y and m and w:
                            List_Lead = List_Lead.filter(
                                Creation_time__year=y,  # Năm 2023
                                Creation_time__month=m     # Tháng 1
                            ).annotate(
                                week=ExtractWeek('Creation_time')
                            ).filter(week=w)  # Tuần 1
                            context['w'] = int(w)
                            context['m'] = int(m)
                            context['y'] = int(y)
                        if y and q:
                            List_Lead = List_Lead.annotate(quarter=ExtractQuarter('Creation_time')).filter(
                                Creation_time__year=y,
                                quarter=q  # Quý 2
                            )
                            context['y'] = int(y)
                            context['q'] = int(q)
                        
                        context['List_Lead_CTV'] = List_Lead.filter(Status_lead='Chưa tư vấn').count()
                        context['List_Lead_DTV'] = List_Lead.filter(Status_lead='Đã tư vấn').count()
                        context['List_Lead_GTT'] = List_Lead.filter(Status_lead='Gửi thông tin').count()
                        context['List_Lead_DXDA'] = List_Lead.filter(Status_lead='Đã xem dự án').count()
                        context['List_Lead_KHKTN'] = List_Lead.filter(Status_lead='KH không tiềm năng').count()
                        context['List_Lead_KHDB'] = List_Lead.filter(Status_lead='KH Đã booking').count()
                        context['List_Lead_KHDXNM'] = List_Lead.filter(Status_lead='KH đã xem nhà mẫu').count()
                        context['List_Lead_KHTN'] = List_Lead.filter(Status_lead='KH tiềm năng').count()
                        context['List_Lead_KHDM'] = List_Lead.filter(Status_lead='KH Đã mua').count()
                    except:
                        context['f'] = ''
                print('context:',context)
                return render(request, 'sleekweb/admin/statistical_page.html', context, status=200)
            elif request.user.is_staff:
                context = {}
                context['months'] = range(1, 13)
                context['years'] = range(2024, 2031)
                context['weeks'] = range(1, 5)
                context['years'] = range(2024, 2031)
                context['quarters'] = range(1, 5)
                f = request.GET.get('f')
                context['List_Campaign'] = Campaign.objects.filter(Belong_User=request.user).annotate(
                    lead_count=Count('list_campaign', filter=Q(list_campaign__Belong_User=request.user))
                ).order_by('-id')
                
                d = request.GET.get('d')
                m = request.GET.get('m')
                y = request.GET.get('y')
                w = request.GET.get('w')
                q = request.GET.get('q')
                
                if y and m:
                    days_in_month = calendar.monthrange(int(y), int(m))[1]
                    context['days'] = range(1, days_in_month + 1)
                # List_Lead = Lead.objects.filter(Belong_Campaign__in=context['List_Campaign'])
                if not f:
                    List_Lead = Lead.objects.filter(Belong_Campaign__in=context['List_Campaign'],Belong_User=request.user)
                    print('List_Lead:',List_Lead)
                    context['List_Lead_CTV'] = List_Lead.filter(Status_lead='Chưa tư vấn').count()
                    context['List_Lead_DTV'] = List_Lead.filter(Status_lead='Đã tư vấn').count()
                    context['List_Lead_GTT'] = List_Lead.filter(Status_lead='Gửi thông tin').count()
                    context['List_Lead_DXDA'] = List_Lead.filter(Status_lead='Đã xem dự án').count()
                    context['List_Lead_KHKTN'] = List_Lead.filter(Status_lead='KH không tiềm năng').count()
                    context['List_Lead_KHDB'] = List_Lead.filter(Status_lead='KH Đã booking').count()
                    context['List_Lead_KHDXNM'] = List_Lead.filter(Status_lead='KH đã xem nhà mẫu').count()
                    context['List_Lead_KHTN'] = List_Lead.filter(Status_lead='KH tiềm năng').count()
                    context['List_Lead_KHDM'] = List_Lead.filter(Status_lead='KH Đã mua').count()
                else:
                    try:
                        context['f'] = int(f)
                        obj_Campaign = Campaign.objects.get(pk=f)
                        context['obj_Campaign'] = obj_Campaign
                        List_Lead = Lead.objects.filter(Belong_Campaign=obj_Campaign,Belong_User=request.user)
                        
                        if y:
                            List_Lead = List_Lead.filter(Creation_time__year=y)
                            context['y'] = int(y)
                        if m:
                            List_Lead = List_Lead.filter(Creation_time__month=m)
                            context['m'] = int(m)
                        if d:
                            List_Lead = List_Lead.filter(Creation_time__day=d)
                            context['d'] = int(d)
                        if y and m and w:
                            List_Lead = List_Lead.filter(
                                Creation_time__year=y,  # Năm 2023
                                Creation_time__month=m     # Tháng 1
                            ).annotate(
                                week=ExtractWeek('Creation_time')
                            ).filter(week=w)  # Tuần 1
                            context['w'] = int(w)
                            context['m'] = int(m)
                            context['y'] = int(y)
                        if y and q:
                            List_Lead = List_Lead.annotate(quarter=ExtractQuarter('Creation_time')).filter(
                                Creation_time__year=y,
                                quarter=q  # Quý 2
                            )
                            context['y'] = int(y)
                            context['q'] = int(q)
                        
                        context['List_Lead_CTV'] = List_Lead.filter(Status_lead='Chưa tư vấn').count()
                        context['List_Lead_DTV'] = List_Lead.filter(Status_lead='Đã tư vấn').count()
                        context['List_Lead_GTT'] = List_Lead.filter(Status_lead='Gửi thông tin').count()
                        context['List_Lead_DXDA'] = List_Lead.filter(Status_lead='Đã xem dự án').count()
                        context['List_Lead_KHKTN'] = List_Lead.filter(Status_lead='KH không tiềm năng').count()
                        context['List_Lead_KHDB'] = List_Lead.filter(Status_lead='KH Đã booking').count()
                        context['List_Lead_KHDXNM'] = List_Lead.filter(Status_lead='KH đã xem nhà mẫu').count()
                        context['List_Lead_KHTN'] = List_Lead.filter(Status_lead='KH tiềm năng').count()
                        context['List_Lead_KHDM'] = List_Lead.filter(Status_lead='KH Đã mua').count()
                    except:
                        context['f'] = ''
                print('context:',context)
                return render(request, 'sleekweb/admin/statistical_page.html', context, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('statistical_page_admin')
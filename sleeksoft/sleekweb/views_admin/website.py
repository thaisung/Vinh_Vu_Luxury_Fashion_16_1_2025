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


def setting_website(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                field = {}
                field['Name'] = request.POST.get('Name')
                field['Email'] = request.POST.get('Email')
                field['Phone_number'] = request.POST.get('Phone_number')
                field['Src_Fanpage'] = request.POST.get('Src_Fanpage')
                field['Logo'] = request.FILES.get('Logo')
                field['Banner'] = request.FILES.get('Banner')
                
                list_obj_setting_email = Website.objects.all()
                
                if list_obj_setting_email:
                    obj = list_obj_setting_email[0]
                    obj.Name = field['Name']
                    obj.Email = field['Email']
                    obj.Phone_number = field['Phone_number']
                    obj.Src_Fanpage = field['Src_Fanpage']
                    obj.Logo = field['Logo']
                    obj.Banner = field['Banner']
                    obj.save()
                else:
                    Website.objects.create(**field)
                return redirect('setting_all')
            else:
                    return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return JsonResponse({'success': False, 'message': 'Không tồn tại phương thức này'},json_dumps_params={'ensure_ascii': False})

def setting_all(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context={}
                list_obj_setting_email = Email_setting.objects.all()
                list_obj_website = Website.objects.all()
                if list_obj_setting_email:
                    context['obj_setting_email'] = list_obj_setting_email[0]
                if list_obj_website:
                    context['obj_website'] = list_obj_website[0]
                return render(request, 'sleekweb/admin/setting_all_page.html', context, status=200)
            else:
                    return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                field = {}
                field['EMAIL_HOST'] = request.POST.get('EMAIL_HOST')
                field['EMAIL_PORT'] = request.POST.get('EMAIL_PORT')
                field['EMAIL_HOST_USER'] = request.POST.get('EMAIL_HOST_USER')
                field['EMAIL_HOST_PASSWORD'] = request.POST.get('EMAIL_HOST_PASSWORD')
                SMTPSecure = request.POST.get('SMTPSecure')
                if SMTPSecure == 'TLS':
                    field['EMAIL_USE_TLS'] = True
                    field['EMAIL_USE_SSL'] = False
                if SMTPSecure == 'SSL':
                    field['EMAIL_USE_TLS'] = False
                    field['EMAIL_USE_SSL'] = True
                
                list_obj_setting_email = Email_setting.objects.all()
                
                if list_obj_setting_email:
                    obj = list_obj_setting_email[0]
                    obj.EMAIL_HOST = field['EMAIL_HOST']
                    obj.EMAIL_USE_TLS = field['EMAIL_USE_TLS']
                    obj.EMAIL_USE_SSL = field['EMAIL_USE_SSL']
                    obj.EMAIL_PORT = field['EMAIL_PORT']
                    obj.EMAIL_HOST_USER = field['EMAIL_HOST_USER']
                    obj.EMAIL_HOST_PASSWORD = field['EMAIL_HOST_PASSWORD']
                    obj.save()
                else:
                    Email_setting.objects.create(**field)
                return redirect('setting_all')
            else:
                    return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return JsonResponse({'success': False, 'message': 'Không tồn tại phương thức này'},json_dumps_params={'ensure_ascii': False})
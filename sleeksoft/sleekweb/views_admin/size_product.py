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


def size_product_ad(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                id_product = request.POST.get('id_product')
                obj_product = Product.objects.get(pk=id_product)
                Size_product.objects.create(Belong_Product_Size=obj_product,Quantity=0)
                return redirect('product_ad',Slug=obj_product.Belong_Category_product_child.Slug)
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('login_page_client')
    
def update_size_product_ad(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                Size = request.POST.get('Size')
                Quantity = request.POST.get('Quantity')
                id_size_product = request.POST.get('id_size_product')
                id_product = request.POST.get('id_product')
                obj_product = Product.objects.get(pk=id_product)
                obj_size_product = Size_product.objects.get(pk=id_size_product)
                obj_size_product.Size = Size
                obj_size_product.Quantity = Quantity
                obj_size_product.save()
                return redirect('product_ad',Slug=obj_product.Belong_Category_product_child.Slug)
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('login_page_client')
    
def delete_size_product_ad(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                id_product = request.POST.get('id_product')
                obj_product = Product.objects.get(pk=id_product)
                id_size_product = request.POST.get('id_size_product')
                Size_product.objects.get(pk=id_size_product).delete()
                return redirect('product_ad',Slug=obj_product.Belong_Category_product_child.Slug)
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('login_page_client')
    

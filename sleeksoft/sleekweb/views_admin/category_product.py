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


def category_product_ad(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context = {}
                s = request.GET.get('s')
                context = {}
                context['List_Category_product'] = Category_product.objects.all().order_by('Arrange')
                if s:
                    context['List_Category_product'] = context['List_Category_product'].filter(Q(Name__icontains=s)).order_by('-id')
                    context['s'] = s
                return render(request, 'sleekweb/admin/category_product.html', context, status=200)
                # Sử dụng Paginator để chia nhỏ danh sách (10 là số lượng mục trên mỗi trang)
                # paginator = Paginator(context['list_user'], settings.PAGE)

                # # Lấy số trang hiện tại từ URL, nếu không mặc định là trang 1
                # p = request.GET.get('p')
                # page_obj = paginator.get_page(p)
                # context['list_user'] = page_obj
                # # Tạo danh sách các số trang
                # page_list = list(range(1, paginator.num_pages + 1))
                # context['page_list'] = page_list
                
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    elif request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                Name = request.POST.get('Name')
                if Name:
                    if  Category_product.objects.filter(Name=Name):
                        return JsonResponse({'success': False, 'message': f'Tên Danh mục {Name} đã tồn tại, vui lòng chọn tên khác để tạo Danh mục'},json_dumps_params={'ensure_ascii': False})
                    else:
                        Category_product.objects.create(
                            Name=Name,
                            Slug = slugify(Name)
                            )
                else:
                    return JsonResponse({'success': False, 'message': f'Tên Danh mục không thể là trống khi tạo'},json_dumps_params={'ensure_ascii': False})
                return redirect('category_product_ad')
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('category_product_ad')
  
def search_category_product_ad(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff or request.user.is_manage :
                s = request.POST.get('s')
                List_Category_product = request.user.list_Category_product.all().order_by('-id')
                if s:
                    List_Category_product = list_Category_product.filter(Q(Name__icontains=s)).order_by('-id')
                List_Category_product = list_Category_product.values('id','Name')
                List_Category_product = list(List_Category_product)
                return JsonResponse({'s':s,'List_Category_product':List_Category_product,'success':True}, status=200,json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('lead_page_admin')

def delete_category_product_ad(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                id_delete = request.POST.get('id_delete')
                text_delete_campaign = request.POST.get('text_delete_campaign')
                obj = Category_product.objects.get(pk=int(id_delete))
                if text_delete_campaign == obj.Name:
                    print('id_delete:',id_delete)
                    obj.delete()
                    return JsonResponse({'success': True, 'message': 'Xóa thành công Danh mục sản phẩm','redirect_url': reverse('category_product_ad')},json_dumps_params={'ensure_ascii': False})
                else:
                    return JsonResponse({'success': False, 'message': 'Nội dung nhập chưa chính xác'},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('category_product_ad')
  
def update_category_product_ad(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_manage:
                if not request.POST.get('id_update'):
                    return JsonResponse({'success': False, 'message': 'Danh mục sản phẩm chưa tồn tại'},json_dumps_params={'ensure_ascii': False})
                else:
                    id_update = request.POST.get('id_update')
                if not request.POST.get('name_update'):
                    return JsonResponse({'success': False, 'message': 'Tên Danh mục cập nhật không được để trống'},json_dumps_params={'ensure_ascii': False})
                else:
                    name_update = request.POST.get('name_update')
                print('id_update:',id_update)
                try:
                    obj = Category_product.objects.get(pk=int(id_update))
                    if Category_product.objects.exclude(pk=id_update).filter(Name=name_update):
                        return JsonResponse({'success': False, 'message': f'Tên Danh mục {name_update} đã tồn tại, vui lòng chọn tên khác để cập nhật'},json_dumps_params={'ensure_ascii': False})
                    else:
                        obj.Name = name_update
                        obj.Arrange = request.POST.get('name_arrange')
                        obj.Slug = slugify(name_update)
                        obj.save()
                        return redirect('category_product_ad')
                except:
                    return JsonResponse({'success': False, 'message': 'Danh mục sản phẩm không tồn tại'},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('category_product_ad')
    
def update_Link_KH_and_So_DT_page_admin(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_manage:
                id_update = request.POST.get('id_update')
                Link_KH = request.POST.get('Link_KH')
                So_DT = request.POST.get('So_DT')
                try:
                    obj = Category_product.objects.get(pk=int(id_update))
                    if Link_KH == 'on':
                        obj.Link_KH = True
                        obj.So_DT = False
                    if So_DT == 'on':
                        obj.Link_KH = False
                        obj.So_DT = True
                    obj.save()
                    return redirect('category_product_ad')
                except:
                    return JsonResponse({'success': False, 'message': 'Chiến dịch không tồn tại'},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('category_product_ad')




    

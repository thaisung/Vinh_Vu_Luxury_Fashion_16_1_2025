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


def category_product_child_ad(request,Slug):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context = {}
                s = request.GET.get('s')
                context = {}
                context['obj_Category_product'] = Category_product.objects.get(Slug=Slug)
                context['List_Category_product'] = Category_product.objects.all()
                context['List_Trademark'] = Trademark.objects.all()
                context['List_Category_product_child'] = context['obj_Category_product'].category_product_detail.all().order_by('-id')
                if s:
                    context['List_Category_product_child'] = context['List_Category_product_child'].filter(Q(Name__icontains=s)).order_by('-id')
                    context['s'] = s
                # Sử dụng Paginator để chia nhỏ danh sách (10 là số lượng mục trên mỗi trang)
                paginator = Paginator(context['List_Category_product_child'], settings.PAGE)

                # Lấy số trang hiện tại từ URL, nếu không mặc định là trang 1
                p = request.GET.get('p')
                page_obj = paginator.get_page(p)
                context['List_Category_product_child'] = page_obj
                # Tạo danh sách các số trang
                page_list = list(range(1, paginator.num_pages + 1))
                context['page_list'] = page_list
                return render(request, 'sleekweb/admin/category_product_child.html', context, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    elif request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                Name = request.POST.get('Name')
                if Name:
                    if  Category_product_child.objects.filter(Name=Name):
                        return JsonResponse({'success': False, 'message': f'Tên Thư mục {Name} đã tồn tại trong hệ thống bao gồm trong Danh mục khác, vui lòng chọn tên khác để tạo Thư mục'},json_dumps_params={'ensure_ascii': False})
                    else:
                        Category_product_child.objects.create(
                            Name=Name,
                            Slug = slugify(Name),
                            Belong_Category_product = Category_product.objects.get(Slug=Slug)
                            )
                else:
                    return JsonResponse({'success': False, 'message': f'Tên Thư mục không thể là trống khi tạo'},json_dumps_params={'ensure_ascii': False})
                return redirect('category_product_child_ad',Slug=Slug)
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('category_product_child_ad',Slug=Slug)
    
def delete_category_product_child_ad(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                id_delete = request.POST.get('id_delete')
                text_delete_campaign = request.POST.get('text_delete_campaign')
                obj = Category_product_child.objects.get(pk=int(id_delete))
                if text_delete_campaign == obj.Name:
                    print('id_delete:',id_delete)
                    obj.delete()
                    return JsonResponse({'success': True, 'message': 'Xóa thành công Thư mục sản phẩm','redirect_url': reverse('category_product_child_ad', kwargs={'Slug': obj.Belong_Category_product.Slug})},json_dumps_params={'ensure_ascii': False})
                else:
                    return JsonResponse({'success': False, 'message': 'Nội dung nhập chưa chính xác'},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('category_product_ad')
  
def update_category_product_child_ad(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_manage:
                if not request.POST.get('id_update'):
                    return JsonResponse({'success': False, 'message': 'Thư mục sản phẩm chưa tồn tại'},json_dumps_params={'ensure_ascii': False})
                else:
                    id_update = request.POST.get('id_update')
                if not request.POST.get('name_update'):
                    return JsonResponse({'success': False, 'message': 'Tên Thư mục cập nhật không được để trống'},json_dumps_params={'ensure_ascii': False})
                else:
                    name_update = request.POST.get('name_update')
                print('id_update:',id_update)
                try:
                    obj = Category_product_child.objects.get(pk=int(id_update))
                    if Category_product.objects.exclude(pk=id_update).filter(Name=name_update):
                        return JsonResponse({'success': False, 'message': f'Tên Thư mục {name_update} đã tồn tại, vui lòng chọn tên khác để cập nhật'},json_dumps_params={'ensure_ascii': False})
                    else:
                        obj.Name = name_update
                        obj.Slug = slugify(name_update)
                        obj.save()
                        return redirect('category_product_child_ad',Slug=obj.Belong_Category_product.Slug)
                except:
                    return JsonResponse({'success': False, 'message': 'Thư mục sản phẩm không tồn tại'},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Bạn chưa được cấp quyền để thực hiện chức năng'},json_dumps_params={'ensure_ascii': False})
        else:
            return redirect('login_page_client')
    else:
        return redirect('category_product_ad')
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

def category_product_child_cl(request,Slug):
    if request.method == 'GET':
        context = {}
        f_size = request.GET.get('f_size')
        f_trademark = request.GET.get('f_trademark')
        f_arrange = request.GET.get('f_arrange')
        # Lấy tất cả danh mục lớn
        context['List_Trademark'] = Trademark.objects.all()
        context['List_Size_product'] = Size_product.objects.all()
        context['List_Size_product'] = {s.Size: s for s in context['List_Size_product']}.values()
        context['List_Category_product'] = Category_product.objects.all()
        for category in context['List_Category_product']:
            # Lấy 3 sản phẩm đầu tiên cho danh mục lớn
            category.list_product = Product.objects.filter(
                Belong_Category_product_child__Belong_Category_product=category
            ).order_by('Creation_time')[:3]
            
            # Lấy tất cả sản phẩm cho danh mục lớn
            category.list_product_home = Product.objects.filter(
                Belong_Category_product_child__Belong_Category_product=category
            ).order_by('Creation_time')
            
            # Gán photo_1 và photo_2 cho từng sản phẩm
            for product in category.list_product_home:
                photos = product.product_photo_detail.all()
                product.photo_1 = photos.first()  # Ảnh đầu tiên
                product.photo_2 = photos[1] if photos.count() > 1 else None  # Ảnh thứ 2 (nếu có)
                
                # Kiểm tra hết hàng
                total_quantity = product.product_size_detail.aggregate(
                    total=models.Sum('Quantity')
                )['total'] or 0
                product.is_out_of_stock = total_quantity == 0
        obj_category_child = Category_product_child.objects.get(Slug=Slug)
        context['obj_category_child'] = obj_category_child
        context['List_Product_filter'] = Product.objects.filter(Belong_Category_product_child__Slug=Slug)
        
        if f_size:
            context['f_size'] = f_size
            context['List_Product_filter'] = context['List_Product_filter'].filter(product_size_detail__Size=f_size)
        if f_trademark:
            context['f_trademark'] = f_trademark
            context['List_Product_filter'] = context['List_Product_filter'].filter(Belong_Trademark__Name=f_trademark)
        if f_arrange:
            context['f_arrange'] = f_arrange
            if f_arrange == '':
                # Sản phẩm mới nhất
                context['List_Product_filter'] = context['List_Product_filter'].order_by('Creation_time')

            if f_arrange == 'priceDesc':
                # Sản phẩm giá giảm dần
                context['List_Product_filter'] = context['List_Product_filter'].order_by('Price_Discount')

            if f_arrange == 'priceAsc':
                # Sản phẩm giá tăng dần
                context['List_Product_filter'] = context['List_Product_filter'].order_by('-Price_Discount')

            if f_arrange == 'discount':
                # Sản phẩm giảm giá (Discount > 0)
                context['List_Product_filter'] = context['List_Product_filter'].filter(Discount__gt=0).order_by('Discount')
                
        # Gán photo_1 và photo_2 cho từng sản phẩm
        for product in context['List_Product_filter']:
            photos = product.product_photo_detail.all()
            product.photo_1 = photos.first()  # Ảnh đầu tiên
            product.photo_2 = photos[1] if photos.count() > 1 else None  # Ảnh thứ 2 (nếu có)
            
            # Kiểm tra hết hàng
            total_quantity = product.product_size_detail.aggregate(
                total=models.Sum('Quantity')
            )['total'] or 0
            product.is_out_of_stock = total_quantity == 0  # True nếu hết hàng
        return render(request, 'sleekweb/client/category_product_child.html', context, status=200)
    else:
        return redirect('category_product_child_cl')
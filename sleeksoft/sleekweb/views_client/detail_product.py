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
from types import SimpleNamespace

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

def detail_product_cl(request,Slug):
    if request.method == 'GET':
        context = {}

        list_obj_website = Website.objects.all()
        if list_obj_website:
            context['obj_website'] = list_obj_website[0]
        list_obj_email = Email_setting.objects.all()
        if list_obj_email:
            context['obj_email'] = list_obj_email[0]
        
        cart = request.COOKIES.get('cart', '[]')
        try:
            cart_items = json.loads(cart)
        except json.JSONDecodeError:
            cart_items = []  # Nếu cookie không hợp lệ, đặt giỏ hàng mặc định là rỗng
        
        # Tính toán thông tin giỏ hàng
        Cart_user = {'data': [], 'total_quantity': 0, 'total_money': 0,'count':0}
        for i in cart_items:
            try:
                product = Product.objects.get(pk=i['id'])  # Lấy sản phẩm từ database
            except Product.DoesNotExist:
                continue  # Bỏ qua nếu sản phẩm không tồn tại

            obj_cart = {
                'product': product,
                'size': i['size'],
                'quantity': int(i['quantity']),
                'pk':i['pk']
            }
            Cart_user['data'].append(obj_cart)

        # Tính tổng số lượng và tổng tiền
        for i in Cart_user['data']:
            Cart_user['total_quantity'] += i['quantity']
            if i['product'].Discount > 0:
                Cart_user['total_money'] += i['quantity'] * int(i['product'].Price_Discount)
            else:
                Cart_user['total_money'] += i['quantity'] * int(i['product'].Price)
        context['Cart_user'] = Cart_user
        Cart_user['total_money'] = format_number(Cart_user['total_money'])
        Cart_user['count'] =  len(Cart_user['data'])
        for i in Cart_user['data']:
            i['product'].Price = format_number(i['product'].Price)
            i['product'].Price_Discount = format_number(i['product'].Price_Discount)
        
        context['obj_Product'] = Product.objects.get(Slug=Slug)
        # Lấy tất cả danh mục lớn
        context['List_Category_product'] = list(Category_product.objects.all())
        
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
                product.is_out_of_stock = total_quantity == 0  # True nếu hết hàng
                
                # product.Price = format_number(product.Price)
                # product.Price_Discount = format_number(product.Price_Discount)
                
        context['List_Product_Love'] = Product.objects.all()
        print('List_Product_Love:',context['List_Product_Love'])
        for product in context['List_Product_Love']:
                photos = product.product_photo_detail.all()
                product.photo_1 = photos.first()  # Ảnh đầu tiên
                product.photo_2 = photos[1] if photos.count() > 1 else None  # Ảnh thứ 2 (nếu có)
                
                # Kiểm tra hết hàng
                total_quantity = product.product_size_detail.aggregate(
                    total=models.Sum('Quantity')
                )['total'] or 0
                product.is_out_of_stock = total_quantity == 0  # True nếu hết hàng
                product.Price = format_number(product.Price)
                product.Price_Discount = format_number(product.Price_Discount)
                
        context['List_Product_Well'] = Product.objects.all()
        print('List_Product_Well:',context['List_Product_Well'])
        for product in context['List_Product_Well']:
                photos = product.product_photo_detail.all()
                product.photo_1 = photos.first()  # Ảnh đầu tiên
                product.photo_2 = photos[1] if photos.count() > 1 else None  # Ảnh thứ 2 (nếu có)
                
                # Kiểm tra hết hàng
                total_quantity = product.product_size_detail.aggregate(
                    total=models.Sum('Quantity')
                )['total'] or 0
                product.is_out_of_stock = total_quantity == 0  # True nếu hết hàng
                product.Price = format_number(product.Price)
                product.Price_Discount = format_number(product.Price_Discount)
                
        sale_category = SimpleNamespace(
                id="9999999999999999",  # Đặt một giá trị giả định cho id
                Name="SUPER SALE",
                Slug="super-sale",
                list_product_home=Product.objects.filter(Discount__gt=0).order_by('Creation_time'),
                # list_product = Product.objects.filter(Discount__gt=0).order_by('Creation_time')[:3]
            )
        context['List_Category_product'].append(sale_category)
                
        
        return render(request, 'sleekweb/client/detail_product.html', context, status=200)
    else:
        return redirect('detail_product_cl',Slug=Slug)



    
def get_detail_product_cl(request,pk):
    if request.method == 'GET':
        obj_product=Product.objects.get(pk=pk)
        thumbnail = ''
        product_thumb = ''
        itemdelete = ''
        clickItem = ''
        if obj_product.Description:
            Description = obj_product.Description
        else:
            Description = ''
        if obj_product.Parameter:
            Parameter = obj_product.Parameter
        else:
            Parameter = ''
        
        if obj_product.Discount > 0:
            Price = f"""<p class="pro-price highlight tp_product_price format-number">
                    {format_number(obj_product.Price_Discount)}₫
                    <span class="pro-price-del"><del class="compare-price format-number">{format_number(obj_product.Price)}₫</del></span>
                </p>"""
        else:
            Price = f"""<p class="pro-price highlight tp_product_price format-number">
                    {format_number(obj_product.Price)}₫

                </p>"""
        Size = ''
        for i in obj_product.product_size_detail.all():
            if i.Quantity > 0:
                Size = Size + f"""
                                <div data-value="" class=" n-sd swatch-element">
                                    <label  class="" data-size="{i.Size}">
                                        <span>{i.Size}</span>
                                        <img class="crossed-out" src="https://web.nvnstatic.net/tp/T0298/img/soldout.png?v=7">
                                    </label>
                                </div>
                            """
            else:
                Size = Size + f"""
                                <div data-value="" class=" n-sd swatch-element">
                                    <label class="deactive"  title="Sản phẩm tạm thời hết hàng">
                                        <span>{i.Size}</span>
                                        <img class="crossed-out" src="https://web.nvnstatic.net/tp/T0298/img/soldout.png?v=7">
                                    </label>
                                </div>
                            """
        # Tạo danh sách các thẻ <option> cho thương hiệu
        for idx,i in enumerate(obj_product.product_photo_detail.all()):
            thumbnail = thumbnail + f"""
                    <div class="  thumbnail thumdelete clickItem" data-index="{idx}" data-option="do"
                        data-zoom="{i.Photo.url}">
                        <img class="img-fluid img-thumbnail"
                            src="{i.Photo.url}">
                    </div>
            """
            product_thumb = product_thumb + f"""
                <div class="product-thumb text-center">
                    <img class="product-image-feature" src="{i.Photo.url}"
                        alt="{obj_product.Name}">
                </div>
            """
            itemdelete = itemdelete + f"""
                <div name-new="_sd05041" class="item itemdelete"
                data-original="{i.Photo.url}" data-option="do"
                data-variant="SD05041">
                <a href="{i.Photo.url}" title="Click để xem" data-option="do"
                    data-image="{i.Photo.url}"
                    data-zoom-image="{i.Photo.url}" rel="lightbox-do">
                    <img class="img-fluid img-responsive"
                        src="{i.Photo.url}">
                    <p class="click-p" href="{i.Photo.url}"
                        data-zoom-image="{i.Photo.url}" rel="lightbox-do">
                        <i class="fa fa-search" aria-hidden="true"></i>
                        Click xem hình lớn hơn
                    </p>
                </a>
            </div>
            """
            clickItem  = clickItem + f"""
                <div class="  thumbnail thumdelete clickItem" data-option="do"
                data-zoom="{i.Photo.url}">
                <img class="img-fluid img-thumbnail" src="{i.Photo.url}">
            </div>
            """
            
        html_content=f"""
                    <script defer type="text/javascript" src="/static/js/pQuickview.js"></script>

        <button type="button" class="close" data-dismiss="modal">
            <img src="https://web.nvnstatic.net/tp/T0298/img/tmp/iconclose.png?v=7" alt="Đóng">
        </button>

        <div class="col-md-8 col-sm-7 col-xs-12">
            <div class="clearfix hidden-xs col-sm-1 thumbnails small-img">
                <div class="row">

                    {thumbnail}
                </div>
            </div>

            <div class="clearfix col-sm-11">
                <div id="slide-image"></div>
                <div class="hinh360" style="display:none">
                    <div id="mySpriteSpin"></div>
                </div>
                <div class="videoProduct" style="display:none">
                    <iframe src="" width="100%" height="470" frameborder="0" allow="autoplay; fullscreen"
                        allowfullscreen=""></iframe>
                </div>
            </div>
        </div>
        <div class="col-md-4 col-sm-5 col-xs-12" id="detail-product">
            <div class="product-title">
                <h1>{obj_product.Name}</h1>
                <span class="pro-soldold">Tình trạng: <span class="statusProduct">Còn hàng</span></span>
            </div>
            <div class="product-price sale-undo" id="price-preview">
                {Price}
            </div>


            <form id="add-item-form" action="" method="post" class="variants clearfix">
                <div class="select-swatch clearfix ">
                    <div id="variant-swatch-1" class=" swatch clearfix">
                        <div class="header">kích thước</div>
                        <div class="select-swap attr-size req" data-column="i1">
                            {Size}
                        </div>
                    </div>

                </div>

                <div class="selector-actions">
                    <div class="quantity-area clearfix hide">
                        <input type="button" value="-" onclick="minusQuantity()" class="qty-btn">
                        <input type="text" id="quantity" name="quantity" value="1" min="1" class="quantity-selector">
                        <input type="button" value="+" onclick="plusQuantity()" class="qty-btn">
                    </div>

                    <div class="wrap-addcart clearfix">
                        <button type="button" id="add-to-cart-detail" class="btnAddToCart" data-psid="40776086" data-selId="40776086"
                             data-ck="0" data-id="{obj_product.id}">SỞ HỮU NGAY</button>
                    </div>
                </div>
            </form>

            <div class="product-description">
                <div class="title-bl">
                    <h2>
                        Thông số sản phẩm <span class="icon-open"></span>
                    </h2>
                </div>
                <div class="description-content">
                    <div class="main_details">
                        {Parameter} </div>
                </div>
            </div>
            <div class="product-description">
                <div class="title-bl">
                    <h2>
                        Mô tả sản phẩm <span class="icon-open"></span>
                    </h2>
                </div>
                <div class="description-content">
                    <div class="description-productdetail">
                        {Description} </div>
                </div>
            </div>
            <center class="centerDetial">
                <a href="/ao-phong-dsquared2-trang-chu-nhieu-mau-s71gd1384-d20020-100-p40776086.html">Xem chi tiết sản phẩm
                    &gt;&gt;</a>
            </center>
        </div>

        <div id="divzoom">
            <div class="divzoom_main">
                {product_thumb}
            </div>
            <div id="positionButtonDiv" class="hidden">
                <p>
                    <span>
                        <button type="button" class="buttonZoomIn"><i></i></button>
                        <button type="button" class="buttonZoomOut"><i></i></button>
                    </span>
                </p>
            </div>
            <button id="closedivZoom"><i></i></button>
        </div>


        <div class="hidden images">
            {itemdelete}
        </div>

        <!-- source thumb slide -->
        <div class="hidden thumbnails-hidden">

            {clickItem}
        </div>

        <div class="checkValue hide">
            <div class="item360deg" data-color="do"></div>

            <div class="item360deg" data-color="xanh-la"></div>

            <div class="item360deg" data-color="den"></div>
        </div>
                 """
        return HttpResponse(html_content, content_type="text/html")
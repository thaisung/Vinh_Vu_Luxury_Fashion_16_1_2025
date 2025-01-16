"""
URL configuration for luanvan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.contrib import admin
# from Data_Interaction.admin import admin_site
from django.urls import path

from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from django.urls import re_path,path


from django.views.generic.base import TemplateView
from django.conf.urls.static import serve

from django.views.generic import RedirectView
from .views_client import *

from .views_admin.user_page import *
from .views_admin.order import *
from .views_admin.home_page import *

from .views_admin.statistical_page import *

from .views_client.login_page import *
from .views_client.register_page import *
from .views_client.reset_pw_send_otp import *

from .views_client.home import *
from .views_client.detail_product import *
from .views_client.cart import *
from .views_client.login import *
from .views_client.register import *
from .views_client.category_product import *
from .views_client.category_product_child import *
from .views_client.getpassword import *
from .views_client.checkout import *
from .views_client.search import *
from .views_client.order import *

from .views_admin.category_product import *
from .views_admin.category_product_child import *
from .views_admin.product import *
from .views_admin.trademark import *
from .views_admin.size_product import *
from .views_admin.order import *


from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin-django/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Thêm URL của allauth
    
    path('', home_cl,name='home_cl'),
    path('category/<str:Slug>/', category_product_cl,name='category_product_cl'),
    path('category-child/<str:Slug>/', category_product_child_cl,name='category_product_child_cl'),
    path('detail-product/<str:Slug>/', detail_product_cl,name='detail_product_cl'),
    path('get-detail-product/<int:pk>/', get_detail_product_cl,name='get_detail_product_cl'),
    path('get-category-product-child/<int:pk>/', get_category_product_child_cl,name='get_category_product_child_cl'),
    path('cart/', cart_cl,name='cart_cl'),
    path('add-product-cart/', add_product_cart_cl,name='add_product_cart_cl'),
    path('remove-product-cart/', remove_product_cart_cl,name='remove_product_cart_cl'),
    path('login/', login_cl,name='login_cl'),
    path('register/', register_cl,name='register_cl'),
    path('getpassword/', getpassword_cl,name='getpassword_cl'),
    path('checkout/', checkout_cl,name='checkout_cl'),
    path('order/', order_cl,name='order_cl'),
    
    path('delete-pd-checkout/', delete_pd_checkout_cl,name='delete_pd_checkout_cl'),
    path('search/', search_cl,name='search_cl'),
    
    # Các đường dẫn khác...
    path('reset-pw-send-otp/', reset_pw_send_otp,name='reset_pw_send_otp'),
    path('reset-pw-check-otp/', reset_pw_check_otp,name='reset_pw_check_otp'),
    
    # path('admin/home/', home_page_admin,name='home_page_admin'),
    
    path('ad/category-product/', category_product_ad,name='category_product_ad'),
    path('ad/category-product/<str:Slug>/', category_product_child_ad,name='category_product_child_ad'),
    path('ad/product/<str:Slug>/', product_ad,name='product_ad'),
    path('ad/update-product/<str:Slug>/<str:Slugg>/', update_product_ad,name='update_product_ad'),
    path('ad/delete-check-list-product/<str:Slug>/', delete_check_list_product_ad,name='delete_check_list_product_ad'),
    # path('admin/search-campaign/', search_category_product_ad,name='search_category_product_ad'),
    path('admin/delete-category-product/', delete_category_product_ad,name='delete_category_product_ad'),
    path('ad/update-category-product/', update_category_product_ad,name='update_category_product_ad'),
    
    path('ad/trademark/', trademark_ad,name='trademark_ad'),
    path('ad/update-trademark/', update_trademark_ad,name='update_trademark_ad'),
    path('ad/delete-trademark/', delete_trademark_ad,name='delete_trademark_ad'),
    
    path('ad/size-product/', size_product_ad,name='size_product_ad'),
    path('ad/delete-size-product/', delete_size_product_ad,name='delete_size_product_ad'),
    path('ad/update-size-product/', update_size_product_ad,name='update_size_product_ad'),
    
    path('admin/delete-category-product-child/', delete_category_product_child_ad,name='delete_category_product_child_ad'),
    path('ad/update-category-product-child/', update_category_product_child_ad,name='update_category_product_child_ad'),
    
    path('ad/order/', order_ad,name='order_ad'),
    path('ad/update-order/', update_order_ad,name='update_order_ad'),
    path('admin/order-delete-check-list/', delete_check_list_order_ad,name='delete_check_list_order_ad'),
    path('ad/delete-order/', delete_order_cl,name='delete_order_cl'),
    
    
    
    
    path('admin/get-setting/', get_setting,name='get_setting'),
    
    path('admin/search-user/', search_user_page_admin,name='search_user_page_admin'),
    # path('admin/search-user-campaign/', search_user_category_product_ad,name='search_user_category_product_ad'),
    path('admin/data-user-campaign/', data_user_campaign,name='data_user_campaign'),
    path('admin/update-data-user-campaign/', update_data_user_campaign,name='update_data_user_campaign'),
    path('admin/user/', user_page_admin,name='user_page_admin'),
    path('admin/user-delete-check-list/', delete_check_list_user_admin,name='delete_check_list_user_admin'),
    
    path('admin/update-un-and-fl/', update_un_and_fl,name='update_un_and_fl'),
    path('admin/update-campaign-user-list/', update_campaign_user_list,name='update_campaign_user_list'),
    
    path('statistical/', statistical_page_admin,name='statistical_page_admin'),

    
    
    
    path('change-password-user-page-admin/', change_password_user_page_admin,name='change_password_user_page_admin'),
    path('change-password-user-auth-page-admin/', change_password_user_auth_page_admin,name='change_password_user_auth_page_admin'),
    path('approve-user-page-admin/', approve_user_page_admin,name='approve_user_page_admin'),
    
    
    
    path('ad-login/', login_page_client,name='login_page_client'),
    path('ad-logout/', logout_page_client,name='logout_page_client'),
    path('ad-register/', register_page_client,name='register_page_client'),
    
    path('admin/setting-all/', setting_all,name='setting_all'),
    
    
]
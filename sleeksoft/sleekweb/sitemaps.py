# blog/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import *

from datetime import datetime
from .views_client import *
from .views_client.home import *
from .views_client.detail_product import *
from .views_client.cart import *
from .views_client.login import *
from .views_client.user import *
from .views_client.register import *
from .views_client.category_product import *
from .views_client.category_product_child import *
from .views_client.getpassword import *
from .views_client.checkout import *
from .views_client.search import *
from .views_client.order import *

protocol = 'http'

class HomeSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = protocol
 
    def items(self):
        return ['home_cl'] 
    
    def lastmod(self, obj):

        return None
 
    def location(self, item):
        return reverse(item)
    
class category_product_cl_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = protocol

    def items(self):
        # Lấy tất cả các Category_product từ cơ sở dữ liệu
        return Category_product.objects.all()

    def lastmod(self, obj):
        return obj.Update_time

    def location(self, item):
        # Dùng slug của mỗi category_product để tạo đường dẫn
        return reverse('category_product_cl', kwargs={'Slug': item.Slug})

# class detail_sound_Sitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.9
#     protocol = 'https'

#     def items(self):
#         return Sound_List.objects.all()

#     def lastmod(self, obj):
#         return obj.created_at_sound
    
#     def location(self, obj):
#         return reverse('detail_sound', args=[obj.sound_url])
    
# class detail_video_Sitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.9
#     protocol = 'https'

#     def items(self):
#         return Video_List.objects.all()

#     def lastmod(self, obj):
#         return obj.created_at_video
    
#     def location(self, obj):
#         return reverse('detail_video', args=[obj.video_url])
    
# class image_video_Sitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.9
#     protocol = 'https'

#     def items(self):
#         return Video_List.objects.all()

#     def lastmod(self, obj):
#         return obj.created_at_video
    
#     def location(self, obj):
#         image_path = obj.video_Image.url
#         return image_path
    
# class StaticSitemap1(Sitemap):
#     changefreq = "monthly"
#     priority = 0.5
#     protocol = 'https'
 
#     def items(self):
#         return ['about','copyright','contact'] 
    
#     def lastmod(self, obj):

#         return None
 
#     def location(self, item):
#         return reverse(item)
    


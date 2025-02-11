# middleware/redirect_middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404
from django.http import JsonResponse
from django.conf import settings
# middleware.py
from sleekweb.models import Email_setting

class RedirectOn404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Nếu gặp lỗi 404, chuyển hướng đến trang đăng nhập
        if response.status_code == 404:
            if 'ad' in request.path:
                print('jkhagshkgdghjk')
                return redirect(reverse('login_page_client'))  # Thay 'login' bằng tên URL của trang đăng nhập
            else:
                return redirect(reverse('home_cl'))
        return response

class EmailSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            email_config = Email_setting.objects.first()
            if email_config:
                settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
                settings.EMAIL_HOST = email_config.EMAIL_HOST
                settings.EMAIL_PORT = email_config.EMAIL_PORT
                settings.EMAIL_USE_TLS = email_config.EMAIL_USE_TLS
                settings.EMAIL_USE_SSL = email_config.EMAIL_USE_SSL
                settings.EMAIL_HOST_USER = email_config.EMAIL_HOST_USER
                settings.EMAIL_HOST_PASSWORD = email_config.EMAIL_HOST_PASSWORD
        except Exception as e:
            print("Không thể tải cài đặt email từ cơ sở dữ liệu:", e)

        response = self.get_response(request)
        return response
    
class RedirectOn405Middleware():
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_paths = [
            reverse('home_page_admin'),
            reverse('campaign_page_admin'),  
            reverse('search_campaign_page_admin'),
            reverse('delete_campaign_page_admin'),  
            reverse('campaign_page_admin'),  
            reverse('update_campaign_page_admin'),
            reverse('lead_page_admin'),
            reverse('lead_update_page_admin'),
            reverse('Select_setting_lead_admin'),
            reverse('get_setting'),
            reverse('get_acc_dete'),
            reverse('login_page_client'),
            reverse('logout_page_client'),
            reverse('register_page_client'),
            reverse('import_data_lead'),
            reverse('get_list_report_history'),
            
        ]

    def __call__(self, request):
        # Nếu đường dẫn hiện tại thuộc danh sách được phép, bỏ qua middleware
        if request.path in self.allowed_paths or  request.path.startswith(settings.MEDIA_URL):
            return self.get_response(request)

        response = self.get_response(request)
        
        # Nếu gặp lỗi 404, xử lý theo logic yêu cầu
        if response.status_code == 404:
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    return redirect(reverse('statistical_page_admin'))
                else:
                    return redirect(reverse('lead_page_staff'))
            else:
                return redirect(reverse('login_page_client'))  # Chuyển hướng đến trang đăng nhập

        # Nếu đường dẫn không thuộc danh sách cho phép, trả về JSON "Đang bảo trì"
        if request.path not in self.allowed_paths:
            return JsonResponse({"message": "Hệ thống đang tạm ngưng chức năng để chờ thanh toán"}, status=503,json_dumps_params={'ensure_ascii': False})

        return response

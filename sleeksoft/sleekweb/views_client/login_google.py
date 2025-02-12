from ..models import *
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login

GOOGLE_CLIENT_ID = "29474878071-j0kinpris517ascir55ck8e9u7nsaqch.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = "http://localhost:8000/accounts/google/callback/"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"

def google_login(request):
    auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&scope=email profile"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return redirect(auth_url)


GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def google_callback(request):
    code = request.GET.get("code")
    
    # Gửi yêu cầu để đổi lấy access token
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    token_json = response.json()
    access_token = token_json.get("access_token")

    # Lấy thông tin người dùng từ Google
    user_info_response = requests.get(GOOGLE_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"})
    user_info = user_info_response.json()

    email = user_info.get("email")
    name = user_info.get("name")
    print('email:',email)
    print('name:',name)

    # Kiểm tra xem người dùng đã tồn tại chưa
    user, created = User.objects.get_or_create(username=email, defaults={"username":email,"email": email, "Full_name": name})
    # Đăng nhập người dùng
    login(request, user)

    return redirect("/")  # Chuyển hướng đến trang chủ sau khi đăng nhập
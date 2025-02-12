from ..models import *
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login
from django.http import JsonResponse

FACEBOOK_CLIENT_ID = "2233110823786626"
FACEBOOK_CLIENT_SECRET = "6010834a778b1f1eb575072d15c20fee"
FACEBOOK_REDIRECT_URI = "http://localhost:8000/accounts/facebook/callback/"

FACEBOOK_TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
FACEBOOK_USER_INFO_URL = "https://graph.facebook.com/me?fields=id,name,email"

def facebook_login(request):
    auth_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth?"
        f"client_id={FACEBOOK_CLIENT_ID}"
        f"&redirect_uri={FACEBOOK_REDIRECT_URI}"
        f"&scope=email,public_profile"
    )
    return redirect(auth_url)

def facebook_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Không tìm thấy code từ Facebook"}, status=400)

    # Lấy access token từ Facebook
    token_data = {
        "client_id": FACEBOOK_CLIENT_ID,
        "client_secret": FACEBOOK_CLIENT_SECRET,
        "redirect_uri": FACEBOOK_REDIRECT_URI,
        "code": code,
    }
    response = requests.get(FACEBOOK_TOKEN_URL, params=token_data)
    token_json = response.json()
    
    if "access_token" not in token_json:
        return JsonResponse({"error": "Không lấy được access token từ Facebook", "details": token_json}, status=400)

    access_token = token_json["access_token"]

    # Lấy thông tin người dùng từ Facebook
    user_info_response = requests.get(FACEBOOK_USER_INFO_URL, params={"access_token": access_token})
    user_info = user_info_response.json()

    print("User info từ Facebook:", user_info)  # Debug để kiểm tra dữ liệu nhận được

    email = user_info.get("email")
    name = user_info.get("name")
    fb_id = user_info.get("id")
    
    # Kiểm tra xem người dùng đã tồn tại chưa
    user, created = User.objects.get_or_create(username=email, defaults={"username":email,"email": email, "Full_name": name})
    # Đăng nhập người dùng
    login(request, user)

    if not email:
        return JsonResponse({"error": "Facebook không cung cấp email. Vui lòng sử dụng cách đăng nhập khác."}, status=400)

    # # Kiểm tra và tạo người dùng
    # user, created = User.objects.get_or_create(
    #     username=email if email else fb_id,
    #     defaults={"email": email, "first_name": name}
    # )

    # if user:
    #     login(request, user)
    # else:
    #     return JsonResponse({"error": "Không thể đăng nhập"}, status=400)

    return redirect("/")
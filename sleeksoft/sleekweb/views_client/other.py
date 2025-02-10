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

def register_email_information_cl(request):
    if request.method == 'POST':
        Email  = request.POST.get('EMAIL')
        if Email:
            if not Email_information.objects.filter(Email=Email).exists():
                Email_information.objects.create(Email=Email)
                return JsonResponse({'success': True, 'message': 'Đăng ký Email nhận thông tin thành công'})
            else:
                return JsonResponse({'success': False, 'message': 'Email đăng ký nhận thông tin đã tồn tại'})
        else:
            return JsonResponse({'success': False, 'message': 'Điền đầy đủ thông tin trước khi đăng ký'})
    else:
        return redirect('home_cl')
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

def getpassword_cl(request):
    if request.method == 'GET':
        context = {}
        # context['number_campaign'] = Campaign.objects.all().count()
        # context['number_lead'] = Lead.objects.all().count()
        # context['number_user'] = User.objects.all().count()
        # context['number_user_approve'] = User.objects.all().filter(Q(is_staff=True)|Q(is_manage=True)|Q(is_superuser=True)).count()
        # context['number_user_not_approve'] = User.objects.all().filter(Q(is_staff=False)&Q(is_manage=False)).count()
        return render(request, 'sleekweb/client/getpassword.html', context, status=200)
    else:
        return redirect('getpassword_cl')
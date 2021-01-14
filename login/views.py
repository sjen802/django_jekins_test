from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from django.contrib import auth as Auth
from django.contrib.sessions.models import Session
import random
from datetime import datetime, date, timedelta

from django.core.mail import send_mail

import string
import time
import datetime
from collections import OrderedDict
import json
from django.contrib import auth 

from django.http import QueryDict
from django.contrib.auth.models import User
from itertools import chain

#API(13)隱私權聲明
@csrf_exempt
def privacy_policy(request):
    sid = request.COOKIES['sessionid']
    s = Session.objects.get(pk=sid)
    token = s.session_data

    now_account = s.get_decoded()['account']
    u = Patient.objects.get(username=now_account)
    
    if request.method == "POST":
        data = request.POST
        fb_id = data
        u.fb_id = fb_id
        status="0"
    else:
        status="1"

    return JsonResponse({"status":status})



#API(1)註冊
@csrf_exempt
def register(request):
    
    if request.method == 'POST':

        data = request.POST
        f = RegisterForm(data)

        if f.is_valid():
            account = f.cleaned_data['account']
            phone = f.cleaned_data['phone']
            email = f.cleaned_data['email']
            password = f.cleaned_data['password']

            Patient.objects.create_user(username=account,email=email,phone=phone,password=password,is_active=False)

            status = "0"
            return JsonResponse({'status':status})
    else:
            status = "1"
    return JsonResponse({'status':status})



#API(3)發送認證碼
@csrf_exempt
def verification_send(request):
    try:
        if request.method == 'POST':
            email = request.POST["email"]
            title = "meter123.com 信箱驗證碼"
            code = ''.join([
                random.choice(string.ascii_letters + string.digits)
                for i in range(8)
            ])
            
            email_from = 'mx90127481@gmail.com'
            reciever = email

            EmailAuth.objects.create(code=code, end_time=10)

            send_mail(title, code, email_from, [reciever], fail_silently=False)
            status = '0'
    except:
        pass
        status = "1"
    
    return JsonResponse({'status': status})


#API(4)檢查認證碼
@csrf_exempt
def verification_check(request):
    try:
        if request.method == "POST":
            email = request.POST["email"]
            phone = request.POST["phone"]
            code = request.POST["code"]

            verify = EmailAuth.objects.get(code=code)
            verify.delete()
            status = "0"
    except:
        status = "1"
    return JsonResponse({'status':status})




#API(2) auth
#登入
@csrf_exempt
def user_auth(request):
    if request.method == 'POST':

        username = request.POST['account']
        password = request.POST['password']
        u = Patient.objects.get(username=username)

        if u:
            if u.is_active == False:
                status = "2"
            elif u.is_active == True:

                user = auth.authenticate(username=username,password=password)

                if user:
                    
                    auth.login(request, user)
                    s = Session.objects.all()[0]
                    request.session['account'] = username
                    token = s.session_data
                    status = "0"
                    
                    return JsonResponse({'status':status, 'token':token})
                else:
                    status = "1"
    
    return JsonResponse({'status':status})


#API(5)忘記密碼
@csrf_exempt
def password_forgot(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            phone = request.POST['phone']
            u = Patient.objects.get(email=email)
                    
            mail_title = email + ' New Password'
            mail_from = ''
            mail_to = email
            new_password = ''.join([
            random.choice(string.ascii_letters + string.digits)
            for i in range(8)
            ])
            reciever = email
            send_mail(mail_title, mail_from, mail_to, [reciever], fail_silently=False)

            u.set_password(new_password)
            u.hasto_change_password = True
            u.save()
           
            status = "0"
    except:
        status = "1"
    return JsonResponse({'status':status})


#API(6)重設密碼
@csrf_exempt
def password_reset(request):
    try:
        if request.method == 'POST':
            newpassword = request.POST['password']
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data

            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)
            
            newpasswd = request.POST['password']
            u.set_password(newpasswd)
            u.hasto_change_password = False
            u.save()
            
            status = '0'

    except:
        status = "1"

    return JsonResponse({'status':status})



#切割資料
def GetRequestBody(body_data):
    #body_data = request.body
    b=[]
    c=[]
    d={}
    data = body_data.decode('utf-8')
    data2 = data.split('\r\n\r\n')

    for i in data2:
        a=i.split('\r\n')
        for i in a:
            b=i.split('=')
            c=c+b
    for i in range(len(c)):
        if i%4==0 or i%4==1 or i%4==3:
            continue
        d.update({c[i].replace('"',''):c[i+1]})
    return d




#API(11) 
@csrf_exempt
def user_default(request):
    if request.method == "PATCH":

        data = request.body.decode('utf-8')
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace('%40', '@').split('&') if i.split('=')[1]
        }
        # data = GetRequestBody(data)
        sid = request.COOKIES['sessionid']
        s = Session.objects.get(pk=sid)
        token = s.session_data

    
        now_account = s.get_decoded()['account']
        u = Patient.objects.get(username=now_account)
        
        username = u
        sugar_delta_max = data["sugar_delta_max"]
        sugar_delta_min = data["sugar_delta_min"]
        sugar_morning_max = data["sugar_morning_max"]
        sugar_morning_min = data["sugar_morning_min"]
        sugar_evening_max = data["sugar_evening_max"]
        sugar_evening_min = data["sugar_evening_min"]
        sugar_after_max = data["sugar_after_max"]
        sugar_after_min = data["sugar_after_min"]
        sugar_before_max = data["sugar_before_max"]
        sugar_before_min = data["sugar_before_min"]
        systolic_max = data["systolic_max"]
        systolic_min = data["systolic_min"]
        diastolic_max = data["diastolic_max"]
        diastolic_min = data["diastolic_min"]
        pulse_max = data["pulse_max"]
        pulse_min = data["pulse_min"]
        weight_max = data["weight_max"]
        weight_min = data["weight_min"]
        bmi_max = data["bmi_max"]
        bmi_min = data["bmi_min"]
        body_fat_max = data["body_fat_max"]
        body_fat_min = data["body_fat_min"]

        User_Default.objects.create(username=username,sugar_delta_max=sugar_delta_max, sugar_delta_min=sugar_delta_min, sugar_morning_max=sugar_morning_max,sugar_morning_min=sugar_morning_min,sugar_evening_max=sugar_evening_max, sugar_evening_min=sugar_evening_min, sugar_before_max=sugar_before_max, sugar_before_min=sugar_before_min, sugar_after_max=sugar_after_max, sugar_after_min=sugar_after_min, systolic_max=systolic_max, systolic_min=systolic_min, diastolic_max=diastolic_max, diastolic_min=diastolic_min, pulse_max=pulse_max, pulse_min=pulse_min, weight_max=weight_max, weight_min=weight_min, bmi_max=bmi_max, bmi_min=bmi_min, body_fat_max=body_fat_max, body_fat_min=body_fat_min)
        
        status="0"
        
    else:
        status="1"
    return JsonResponse({"status":status})





#API(7)(12) 個人資料
@csrf_exempt
def user_information(request):
    sid = request.COOKIES['sessionid']
    s = Session.objects.get(pk=sid)
    token = s.session_data

    #print(token)
    now_account = s.get_decoded()['account']
    u = Patient.objects.get(username=now_account)

    
    
    if request.method == "PATCH":

        # data = GetRequestBody(data)
        data = request.body.decode('utf-8')
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace('%40', '@').split('&') if i.split('=')[1]
        }

        name = data["name"]
        birthday = data["birthday"]
        height = data["height"]
        gender = data["gender"]
        # fcm_id = data["fcm_id"]
        address = data["address"]
        weight = data["weight"]
        phone = data["phone"]
        email = data["email"]

        u.name = name
        u.birthday = birthday
        u.height = height
        u.gender = gender
        # u.fcm_id = fcm_id
        u.address = address
        u.weight = weight
        u.phone = phone
        u.email = email
        u.save()

        status="0"
        return JsonResponse({"status":status})

    
    if request.method == "GET":

        sid = request.COOKIES['sessionid']
        s = Session.objects.get(pk=sid)
        token = s.session_data

        now_account = s.get_decoded()['account']

        u = Patient.objects.get(username=now_account)

        f = Patient.objects.filter(username=u)
        p = []
        for i in range(len(f)):
            k = {}
            k ={
            "id":f[i].id,
            "name":f[i].username,
            "account":f[i].username,
            "email":f[i].email,
            "phone":f[i].phone,
            "fb_id":f[i].fb_id,
            "status":f[i].status,
            "group":f[i].group,
            "birthday":f[i].birthday,
            "height":f[i].height,
            "weight":f[i].weight,
            "gender":f[i].gender,
            "address":f[i].address,
            "unread_records":1,
            "verified":f[i].verified,
            "privacy_policy":f[i].privacy_policy,
            "must_change_password":f[i].must_change_password,
            "fcm_id":f[i].fcm_id,
            "badge":87,
            "login_times":f[i].login_times,
            "created_at":f[i].created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at":f[i].updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            p.append(k)



        x = User_Default.objects.filter(username=u)
        y = []
        for i in range(len(x)):
            z = {}
            z ={
                "id":x[i].id,
                "user_id":x[i].id,
                "sugar_delta_max":x[i].sugar_delta_max,
                "sugar_delta_min":x[i].sugar_delta_min,
                "sugar_morning_max":x[i].sugar_morning_max,
                "sugar_morning_min":x[i].sugar_morning_min,
                "sugar_evening_max":x[i].sugar_evening_max,
                "sugar_evening_min":x[i].sugar_evening_min,
                "sugar_before_max":x[i].sugar_before_max,
                "sugar_before_min":x[i].sugar_before_min,
                "sugar_after_max":x[i].sugar_after_max,
                "sugar_after_min":x[i].sugar_after_min,
                "systolic_max":x[i].systolic_max,
                "sugar_after_min":x[i].sugar_after_min,
                "systolic_max":x[i].systolic_max,
                "systolic_min":x[i].systolic_min,
                "diastolic_max":x[i].diastolic_max,
                "diastolic_min":x[i].diastolic_min,
                "pulse_max":x[i].pulse_max,
                "pulse_min":x[i].pulse_min,
                "weight_max":x[i].weight_max,
                "weight_min":x[i].weight_min,
                "bmi_max":x[i].bmi_max,
                "bmi_min":x[i].bmi_min,
                "body_fat_max":x[i].body_fat_max,
                "body_fat_min":x[i].body_fat_min,
                "created_at":x[i].created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at":x[i].updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            y.append(z)

    
        a = User_Setting.objects.filter(username=u)
        b = []
        for i in range(len(a)):
            c = {}
            c ={
            "id":a[i].id,
            "user_id":a[i].username,
            "no_recording_for_a_day":a[i].no_recording_for_a_day,
            "over_max_or_under_min":a[i].over_max_or_under_min,
            "after_meal":a[i].after_meal,
            "unit_of_sugar":a[i].unit_of_sugar,
            "unit_of_weight":a[i].unit_of_weight,
            "unit_of_height":a[i].unit_of_height,
            "created_at":a[i].created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at":a[i].updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            b.append(c)

        status = '0'
        return JsonResponse({'status':status,'user':p,'default':y,'setting':b})

    else:
        status="1"
        return JsonResponse({"status":status})




#API(35)
@csrf_exempt
def user_setting(request):
    if request.method == "PATCH":

        data = request.body.decode('utf-8')
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace('%40', '@').split('&') if i.split('=')[1]
        }
        # data = GetRequestBody(data)
        sid = request.COOKIES['sessionid']
        s = Session.objects.get(pk=sid)
        token = s.session_data

       
        now_account = s.get_decoded()['account']
        u = Patient.objects.get(username=now_account)
        
        username = u
        after_recording = data["after_recording"]
        no_recording_for_a_day = data["no_recording_for_a_day"]
        over_max_or_under_min = data["over_max_or_under_min"]
        after_meal = data["after_meal"]
        unit_of_sugar = data["unit_of_sugar"]
        unit_of_weight = data["unit_of_weight"]
        unit_of_height = data["unit_of_height"]
       
        User_Setting.objects.create(username=username, after_recording=after_recording, no_recording_for_a_day=no_recording_for_a_day, over_max_or_under_min=over_max_or_under_min, after_meal=after_meal, unit_of_sugar=unit_of_sugar, unit_of_weight=unit_of_weight, unit_of_height=unit_of_height)
       
        

        status = "0"

    else:
        status = "1"

    return JsonResponse({'status':status})




#API(30)(31)醫療資訊
@csrf_exempt
def user_medical(request):
    try:
        if request.method == "PATCH":

            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data

            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            data = request.body.decode('utf-8')
            data = {
                i.split('=')[0]: i.split('=')[1]
                for i in data.replace('%40', '@').split('&') if i.split('=')[1]
            }
            # data = GetRequestBody(data)

            diabetes_type = data["diabetes_type"]
            oad = data["oad"]
            insulin = data["insulin"]
            anti_hypertensives = data["anti_hypertensives"]
            
            User_Medical.objects.create(username=u, user_id=u, diabetes_type=diabetes_type, oad=oad, insulin=insulin, anti_hypertensives=anti_hypertensives)

            status="0"

            return JsonResponse({'status':status})
    
        if request.method == "GET":

            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data

            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            f = User_Medical.objects.filter(username=u)
            p = []

            for i in range(len(f)):
                k ={
                    "id":f[i].id,
                    "user_id":f[i].user_id,
                    "diabetes_type":f[i].diabetes_type,
                    "oad":f[i].oad,
                    "insulin":f[i].insulin,
                    "anti_hypertensives":f[i].anti_hypertensives,
                    "created_at":f[i].created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at":f[i].updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }
                p.append(k)
            status = '0'
            return JsonResponse({'status':status,'medical_info':p})

    except:
        status="1"
        return JsonResponse({"status":status})







#API(23)分享
@csrf_exempt
def user_share(request):
    
    if request.method == "POST":

        data = request.POST

        sid = request.COOKIES['sessionid']
        s = Session.objects.get(pk=sid)
        token = s.session_data

        now_account = s.get_decoded()['account']
        u = Patient.objects.get(username=now_account)

        share_type = data['type']
        share_id = data['id']
        relation_type = data['relation_type']
        
        User_Share.objects.create(username=u, user_id=u.id, share_type=share_type, share_id = share_id, friend_type=relation_type)

        status="0"

        return JsonResponse({'status':status})

@csrf_exempt
def user_sharee(request, friend_type):
    if request.method == "GET":

        sid = request.COOKIES['sessionid']
        s = Session.objects.get(pk=sid)
        token = s.session_data
        now_account = s.get_decoded()['account']
        u = Patient.objects.get(username=now_account)
        
        inviter_friend = User_invite.objects.filter(username=u, accept=True, friend_type=friend_type)   #自己為邀請者
        invitee_friend = User_invite.objects.filter(code=u.invite_code, accept=True, friend_type=friend_type)  #自己為受邀者
        result_list = list(chain(inviter_friend, invitee_friend))
        
        share_list = []
        for i in result_list:
            if i.username == u:  #自己為邀請者
                friend = Patient.objects.get(invite_code=i.code)
                share = User_Share.objects.filter(username=friend)
            else:  #自己為受邀者
                friend = Patient.objects.get(username=i.username)
                share = User_Share.objects.filter(username=friend)
            share_list.append(share)

        w = []
        for i in share_list:
            if i.exists():
                i = i.get()
                if i.share_type == "0": #血壓
                    blood_pressure = User_blood_pressure.objects.get(id=i.share_id)
                    friend_info = Patient.objects.get(username = i.username)
                    e ={
                        "id":i.share_id,
                        "user_id":i.user_id,
                        "systolic":blood_pressure.systolic,
                        "diastolic":blood_pressure.diastolic,
                        "pulse":blood_pressure.pulse,
                        "recorded_at":blood_pressure.recorded_at,
                        "user":{
                            "id":friend_info.id,
                            "name":friend_info.username,
                            "account":friend_info.username,
                            "email":friend_info.email,
                            "phone":friend_info.phone,
                            "fb_id":friend_info.fb_id,
                            "status":friend_info.status,
                            "group":friend_info.group,
                            "birthday":friend_info.birthday,
                            "height":friend_info.height,
                            "gender":friend_info.gender,
                            "unread_records":[0,0,0],
                            "verified":friend_info.verified,
                            "privacy_policy":friend_info.privacy_policy,
                            "must_change_password":friend_info.must_change_password,
                            "badge":87,
                            "created_at":friend_info.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "updated_at":friend_info.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                        },
                        "created_at":i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "type":i.share_type
                    }
                    w.append(e)

                elif i.share_type == "1": #weight
                    user_weight = User_body_weight.objects.get(id=i.share_id)
                    friend_info = Patient.objects.get(username = i.username)
                    e ={
                        "id":i.share_id,
                        "user_id":i.user_id,
                        "weight":user_weight.weight,
                        "body_fat":user_weight.body_fat,
                        "bmi":user_weight.bmi,
                        "recorded_at":user_weight.recorded_at,
                        "user":{
                            "id":friend_info.id,
                            "name":friend_info.username,
                            "account":friend_info.username,
                            "email":friend_info.email,
                            "phone":friend_info.phone,
                            "fb_id":friend_info.fb_id,
                            "status":friend_info.status,
                            "group":friend_info.group,
                            "birthday":friend_info.birthday,
                            "height":friend_info.height,
                            "gender":friend_info.gender,
                            "unread_records":[0,0,0],
                            "verified":friend_info.verified,
                            "privacy_policy":friend_info.privacy_policy,
                            "must_change_password":friend_info.must_change_password,
                            "badge":87,
                            "created_at":friend_info.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "updated_at":friend_info.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                        },
                        "created_at":i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "type":i.share_type
                    }
                    w.append(e)

                
                elif i.share_type == "2": #sugar
                    user_sugar = User_blood_sugar.objects.get(id=i.share_id)
                    friend_info = Patient.objects.get(username = i.username)
                    e ={
                        "id":i.share_id,
                        "user_id":i.user_id,
                        "sugar":user_sugar.sugar,
                        "timeperiod":user_sugar.timeperiod,
                        "recorded_at":user_sugar.recorded_at,
                        "user":{
                            "id":friend_info.id,
                            "name":friend_info.username,
                            "account":friend_info.username,
                            "email":friend_info.email,
                            "phone":friend_info.phone,
                            "fb_id":friend_info.fb_id,
                            "status":friend_info.status,
                            "group":friend_info.group,
                            "birthday":friend_info.birthday,
                            "height":friend_info.height,
                            "gender":friend_info.gender,
                            "unread_records":[0,0,0],
                            "verified":friend_info.verified,
                            "privacy_policy":friend_info.privacy_policy,
                            "must_change_password":friend_info.must_change_password,
                            "badge":87,
                            "created_at":friend_info.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "updated_at":friend_info.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                        },
                        "created_at":i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "type":i.share_type
                    }
                    w.append(e)

                elif i.share_type == "3": #diet
                    user_diet = User_diet.objects.get(id=i.share_id)
                    friend_info = Patient.objects.get(username = i.username)
                    e ={
                        "id":i.share_id,
                        "user_id":i.user_id,
                        "description":user_diet.description,
                        "meal":user_diet.meal,
                        "tag":user_diet.tag,
                        "lat":user_diet.lat,
                        "lng":user_diet.lng,
                        "recorded_at":user_sugar.recorded_at,
                        "user":{
                            "id":friend_info.id,
                            "name":friend_info.username,
                            "account":friend_info.username,
                            "email":friend_info.email,
                            "phone":friend_info.phone,
                            "fb_id":friend_info.fb_id,
                            "status":friend_info.status,
                            "group":friend_info.group,
                            "birthday":friend_info.birthday,
                            "height":friend_info.height,
                            "gender":friend_info.gender,
                            "unread_records":[0,0,0],
                            "verified":friend_info.verified,
                            "privacy_policy":friend_info.privacy_policy,
                            "must_change_password":friend_info.must_change_password,
                            "badge":87,
                            "created_at":friend_info.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "updated_at":friend_info.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                        },
                        "created_at":i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "type":i.share_type
                    }
                    w.append(e)
            else:
                pass   

        status = '0'         
        return JsonResponse({'status':status,'records':w})

    else:
        status="1"
        return JsonResponse({"status":status})




#關懷資訊
#API(27)(28)
@csrf_exempt
def user_care(request):
    try:
        if request.method == "POST":

            data = request.POST

            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data

            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            care_message = data['message']
            
            User_Care.objects.create(username=u, care_message=care_message)

            status="0"

            return JsonResponse({'status':status})

        if request.method == "GET":

            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data

            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            f = User_Care.objects.filter(username=u)

            p = []

            for i in range(len(f)):
                k = {}
                k ={
                "id":f[i].id,
                "user_id":u.id,
                "member_id": 0,
                "reply_id":None,
                "message":f[i].care_message,
                "created_at":f[i].created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at":f[i].updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }
                p.append(k)
            status = '0'
            return JsonResponse({'status':status,'cares':p})

    except:
        status="1"
        return JsonResponse({"status":status})



#API(29) 最新消息
@csrf_exempt
def user_news(request):
    if request.method == "GET":

        sid = request.COOKIES['sessionid']
        s = Session.objects.get(pk=sid)
        token = s.session_data

        now_account = s.get_decoded()['account']
        u = Patient.objects.get(username=now_account)

        f = User_Care.objects.filter(username=u)

        p = []

        for i in range(len(f)):
            k = {}
            k ={
            "id":f[i].id,
            "member_id":u.id,
            "group":None,
            "message":f[i].care_message,
            "pushed_at":f[i].created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at":"null",
            "updated_at":"null"
            }
            p.append(k)
        status = '0'
        return JsonResponse({'status':status,'cares':p})

    else:
        status="1"
        return JsonResponse({'status':status})






#API(32)(33)(34) 糖化血色素
@csrf_exempt
def user_a1c(request):
    try:  
        if request.method == "POST":

            data = request.POST

            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            a1c = data['a1c']
            User_a1c.objects.create(username=u, a1c=a1c)
            status="0"

            return JsonResponse({'status':status})

        if request.method == "GET":

            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            f = User_a1c.objects.filter(username=u)
            p = []

            for i in range(len(f)):
                k = {}
                k ={
                "id":f[i].user_id,
                "user_id":f[i].user_id,
                "a1c":f[i].a1c,
                "recorded_at":f[i].recorded_at,
                "created_at":f[i].created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at":f[i].updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }
                p.append(k)
            status = '0'
            return JsonResponse({'status':status,'a1cs':p})
            
        if request.method == 'DELETE':
            
            data = request.body.decode('utf-8')
            data = {
                i.split('=')[0]: i.split('=')[1]
                for i in data.replace('%40', '@').split('&') if i.split('=')[1]
            }
            # data = GetRequestBody(request.body)
            k = data["ids[]"].split(',')
            for i in k:
                print(i)
                d = User_a1c.objects.filter(id=i).delete()

            status = '0'
            return JsonResponse({'status':status})
    
    except:
        status="1"
        return JsonResponse({'status':status})


#API(39) 更新 badge
@csrf_exempt
def user_badge(request):

    sid = request.COOKIES['sessionid']
    s = Session.objects.get(pk=sid)
    token = s.session_data
    now_account = s.get_decoded()['account']
    u = Patient.objects.get(username=now_account)

    data = request.body
    data = data.decode('utf-8')
    data = data.split("=")
    data = {data[0]:data[1]}

    if request.method == "PUT":
        u.badge = data['badge']
        u.save()
        status="0" 
    else:
        status="1"

    return JsonResponse({"status":status})

@csrf_exempt #api(8)
def blood_pressure(request):    #血壓資料上傳
    if request.method == "POST":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            systolic = request.POST['systolic']
            diastolic = request.POST['diastolic']
            pulse = request.POST['pulse']

            User_blood_pressure.objects.create(systolic = systolic, diastolic = diastolic, pulse = pulse, username = u)
            return JsonResponse({"status":"0"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt  #api(9)
def user_weight(request):       #體重資料上傳
    if request.method == "POST":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            weight = request.POST['weight']
            body_fat = request.POST['body_fat']
            bmi = request.POST['bmi']

            User_body_weight.objects.create(weight = weight, body_fat = body_fat, bmi = bmi, username = u)
            return JsonResponse({"status":"0"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt  #api(10)
def blood_sugar(request):           #血糖資料上傳
    if request.method == "POST":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            sugar = request.POST['sugar']
            timeperiod = request.POST['timeperiod']

            User_blood_sugar.objects.create(sugar = sugar, timeperiod = timeperiod, username = u)
            return JsonResponse({"status":"0"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def user_diary(request): #日記列表資料 api(14)
    if request.method == "GET":
        try:
            input_day = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d")
            last_input_date = input_day + timedelta(hours=23,minutes=59,seconds=59)

            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)
            
            blood_pressure = User_blood_pressure.objects.filter(username=u, created_at__range=(input_day, last_input_date))
            body_weight = User_body_weight.objects.filter(username=u, created_at__range=(input_day, last_input_date))
            blood_sugar = User_blood_sugar.objects.filter(username=u, created_at__range=(input_day, last_input_date))
            diet = User_diet.objects.filter(username=u, created_at__range=(input_day, last_input_date))

            sum_blood_pressure = []
            if blood_pressure.exists():
                for i in blood_pressure:
                    i.id = {
                        "id":i.id,
                        "user_id":u.username,
                        "systolic":i.systolic,
                        "diastolic":i.diastolic,
                        "pulse":i.pulse, 
                        "created_at":i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at":i.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    sum_blood_pressure.append(i.id)
            else:
                sum_blood_pressure = {
                    "id":None,
                    "user_id":u.username,
                    "systolic":None,
                    "diastolic":None,
                    "pulse":None, 
                    "created_at":None,
                    "updated_at": None
                }

            sum_body_weight = []
            if body_weight.exists():
                for i in body_weight:
                    i.id = {
                        "id":i.id,
                        "user_id":u.username,
                        "weight":i.weight,
                        "body_fat":i.body_fat,
                        "bmi":i.bmi, 
                        "created_at":i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at":i.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    sum_body_weight.append(i.id)
            else:
                sum_body_weight = {
                    "id":None,
                    "user_id":u.username,
                    "weight":None,
                    "body_fat":None,
                    "bmi":None, 
                    "created_at":None,
                    "updated_at": None
                }

            sum_blood_sugar = []
            if blood_sugar.exists():
                for i in blood_sugar:
                    i.id = {
                        "id":i.id,
                        "user_id":u.username,
                        "sugar":i.sugar,
                        "timeperiod":i.timeperiod,
                        "created_at":i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at":i.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    sum_blood_sugar.append(i.id)
            else:
                sum_blood_sugar = {
                    "id":None,
                    "user_id":u.username,
                    "sugar":None,
                    "timeperiod":None,
                    "created_at":None,
                    "updated_at": None
                }

            sum_diet = []
            if diet.exists():
                for i in diet:
                    image_url = str(request.META['HTTP_HOST']) + "/media/" + str(i.image)
                    i.id = {
                        "id":i.id,
                        "user_id":u.username,
                        "description":i.description,
                        "meal":i.meal,
                        "image_num":i.image_num, 
                        "image":image_url, 
                        "tag":i.tag, 
                        "lat":i.lat, 
                        "lng":i.lng, 
                        "created_at":i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at":i.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    sum_diet.append(i.id)
            else:
                sum_diet = {
                    "id":None,
                    "user_id":u.username,
                    "description":None,
                    "meal":None,
                    "image_num":None,
                    "image":None,
                    "tag":None,
                    "lat":None,
                    "lng":None, 
                    "created_at":None,
                    "updated_at": None
                }
                
            return JsonResponse({"status":"0", "blood_pressure":sum_blood_pressure, "body_weight":sum_body_weight, "blood_sugar":sum_blood_sugar, "diet":sum_diet})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def get_friend_code(request):  #生成好友邀請碼 api(16)
    if request.method == "GET":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            if u.invite_code == None:
                f_code = random.randint(0, 999999999)
                Patient.objects.filter(username=u).update(invite_code=f_code)
                return JsonResponse({"status":"0", "invite_code":f_code})
            else:
                return JsonResponse({"status":"0", "invite_code":u.invite_code})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})



@csrf_exempt
def friend_send(request):  #送出控糖團邀請 api(19)
    if request.method == "POST":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            friend_type = request.POST['type']
            invite_code = request.POST['invite_code']

            friend = Patient.objects.filter(invite_code=invite_code)
            already_friend = User_invite.objects.filter(username = u, code=invite_code)

            if already_friend.exists():
                return JsonResponse({"status":"1"})  #已經邀請過了
            else:
                if friend.exists():
                    User_invite.objects.create(friend_type = friend_type, code = invite_code, username = u)
                    return JsonResponse({"status":"0"})
                else:
                    return JsonResponse({"status":"1"})  #找不到好友
                    
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def friend_accept(request, invite_id):  #接受控糖團邀請 api(20)
    if request.method == "GET":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            invite = User_invite.objects.get(id=invite_id)
            invite.accept = True
            invite.save()
            User_friend.objects.create(Inviter=invite.username,Invitee=u, friend_type=invite.friend_type)
            return JsonResponse({"status":"0"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def friend_refuse(request, invite_id):  #拒絕控糖團邀請 api(21)
    if request.method == "GET":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            User_invite.objects.filter(id=invite_id).update(accept=False)
            return JsonResponse({"status":"0"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def friend_result(request):  #控糖團結果 api(26)
    if request.method == "GET":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            all_friend = User_invite.objects.all()
            if all_friend.exists():
                result = []
                for i in all_friend:
                    friend = Patient.objects.get(invite_code=i.code)
                    result_list = {
                        "id":i.id,
                        "user_id":i.username.id,
                        "relation_id":friend.id,
                        "type":i.friend_type,
                        "status": 1 if i.accept==True else 2,
                        "read": False if i.accept==None else True,
                        "created_at":i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at":i.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "relaction":{
                            "id":friend.id,
                            "name":friend.name,
                            "account":"fb_1",
                            "email":friend.email,
                            "phone":friend.phone,
                            "fb_id":friend.fb_id,
                            "status":friend.status,
                            "group":friend.group,
                            "birthday":friend.birthday,
                            "height":friend.height,
                            "gender":friend.gender,
                            "unread_records":[0,0,0],
                            "verified":friend.verified,
                            "privacy_policy": friend.privacy_policy,
                            "must_change_password": friend.must_change_password,
                            "badge":  friend.badge,
                            "created_at":friend.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "updated_at":friend.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    }
                    result.append(result_list)
                User_invite.objects.filter(username=u).update(inviter_read=True)
            else:
                result = None
            return JsonResponse({"status":"0", "result":result})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def friend_list(request):  #把該使用者的好友列出來 api(17)
    if request.method == "GET":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)
            
            inviter_friend = User_friend.objects.filter(Inviter=u)   #自己為邀請者
            invitee_friend = User_friend.objects.filter(Invitee=u)  #自己為受邀者
            result_list = list(chain(inviter_friend, invitee_friend))
            sum_friend_list = []

            if not result_list:  #如果是空的
               sum_friend_list = None
            else:
                for i in result_list:
                    if i.Inviter == u:  #自己為邀請者
                        friend = Patient.objects.get(username=i.Invitee)
                    else:  #自己為受邀者
                        friend = Patient.objects.get(username=i.Inviter)
                        
                    friend_list = {
                        "id":friend.id,
                        "name":str(friend.username),
                        "account":str(friend.username),
                        "email":friend.email,
                        "phone":friend.phone,
                        "fb_id":friend.fb_id,
                        "status":friend.status,
                        "group":friend.group,
                        "birthday":friend.birthday,
                        "height":friend.height,
                        "gender":friend.gender,
                        "verified":friend.verified,
                        "privacy_policy":friend.privacy_policy,
                        "must_change_password":friend.must_change_password,
                        "badge":friend.badge,
                        "created_at":friend.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at":friend.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "relation_type":i.friend_type,
                    }
                    sum_friend_list.append(friend_list)

            return JsonResponse({"status":"0", "friends":sum_friend_list})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def friend_request(request):  #將邀請人和被邀請人的一些資料列出來給前端 api(18)
    if request.method == "GET":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            not_accept_friend = User_invite.objects.filter(accept=None)
            result = []
            if not_accept_friend.exists():
                
                for i in not_accept_friend:
                    inviter = Patient.objects.get(username=i.username)  #邀請者
                    friend = Patient.objects.get(invite_code=i.code)  #受邀請者
                    result_list = {
                        "id":i.id,
                        "user_id":inviter.id,
                        "relation_id":friend.id,
                        "type":i.friend_type,
                        "status": 0,
                        "created_at":i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at":i.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "user":{
                            "id":inviter.id,
                            "name":inviter.name,
                            "account":"fb_1",
                            "email":inviter.email,
                            "phone":inviter.phone,
                            "fb_id":inviter.fb_id,
                            "status":inviter.status,
                            "group":inviter.group,
                            "birthday":inviter.birthday,
                            "height":inviter.height,
                            "gender":inviter.gender,
                            "unread_records":[0,0,0],
                            "verified":inviter.verified,
                            "privacy_policy": inviter.privacy_policy,
                            "must_change_password": inviter.must_change_password,
                            "badge":  inviter.badge,
                            "created_at":inviter.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "updated_at":inviter.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    }
                    result.append(result_list)
            else:
                result = None
            
            return JsonResponse({"status":"0", "request":result})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def diet(request):  #飲食日記 api(15)
    if request.method == "POST":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            description = request.POST.get('description')
            meal = request.POST.get('meal')
            image = request.FILES.get('image')
            image_num = request.POST.get('image_num')
            tag = request.POST.get('tag')
            lat = request.POST.get('lat')
            lng = request.POST.get('lng')

            User_diet.objects.create(description = description, image = image, image_num = image_num, meal = meal, tag = tag, lat = lat, lng = lng, username=u)
    
            image_setting = User_diet.objects.all().last()
            image_url = str(request.META['HTTP_HOST']) + "/media/" + str(image_setting.image)

            return JsonResponse({"status":"0" , "image_url":image_url})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def records(request):           #搜尋系統的最後一筆api(44)
    if request.method == "POST":
        try:
            diets = request.POST.get('diets', '')

            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            last_blood_pressure = User_blood_pressure.objects.filter(username=u).last()
            last_body_weight = User_body_weight.objects.filter(username=u).last()
            last_blood_sugar = User_blood_sugar.objects.filter(username=u).last()

            # 做None的判斷
            if last_blood_pressure is not None:
                blood_pressure = {
                    "id":last_blood_pressure.id,
                    "user_id":u.id,
                    "systolic":last_blood_pressure.systolic,
                    "diastolic":last_blood_pressure.diastolic, 
                    "pulse":last_blood_pressure.pulse,
                    "created_at":last_blood_pressure.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at":last_blood_pressure.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                blood_pressure = {
                    "id":None,
                    "user_id":u.id,
                    "systolic":None,
                    "diastolic":None, 
                    "pulse":None,
                    "created_at":None,
                    "updated_at":None
                }

            if last_body_weight is not None:
                weights = {
                    "id":last_body_weight.id,
                    "user_id":u.id,
                    "weight":last_body_weight.weight,
                    "body":last_body_weight.body_fat, 
                    "bmi":last_body_weight.bmi,
                    "created_at":last_body_weight.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at":last_body_weight.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                weights = {
                    "id":None,
                    "user_id":u.id,
                    "weight":None,
                    "body":None, 
                    "bmi":None,
                    "created_at":None,
                    "updated_at":None
                }

            if last_blood_sugar is not None:
                blood_sugars = {
                    "id":last_blood_sugar.id,
                    "user_id":u.id,
                    "sugar":last_blood_sugar.sugar,
                    "timeperiod":last_blood_sugar.timeperiod, 
                    "created_at":last_blood_sugar.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at":last_blood_sugar.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                blood_sugars = {
                    "id":None,
                    "user_id":u.id,
                    "sugar":None,
                    "timeperiod":None, 
                    "created_at":None,
                    "updated_at":None
                }

            return JsonResponse({"status":"0", 
                                                "blood_pressure":blood_pressure,
                                                "weights":weights,
                                                "blood_sugars":blood_sugars,
                                                })
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

    elif request.method == "DELETE":   #刪除指定的飲食日記api(40)
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)
            
            blood_pressures_id = request.GET.get('blood_pressures')
            weights_id = request.GET.get('weights')
            blood_sugars_id = request.GET.get('blood_sugars')
            diets_id = request.GET.get('diets')

            User_blood_pressure.objects.filter(username=u, id=blood_pressures_id).delete()
            User_body_weight.objects.filter(username=u, id=weights_id).delete()
            User_blood_sugar.objects.filter(username=u, id=blood_sugars_id).delete()
            User_diet.objects.filter(username=u, id=diets_id).delete()

            return JsonResponse({"status":"0"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def invite_remove(request, friend_id):  #當使用者選擇接受或拒絕邀請後，就可將邀請的列表進行刪除 api(22)
    if request.method == "GET":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            User_invite.objects.filter(code=u.invite_code, accept=True, inviter_read=True).delete()
            User_invite.objects.filter(code=u.invite_code, accept=False, inviter_read=True).delete()
            return JsonResponse({"status":"0"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def friend_remove(request):  #刪除更多好友 api(37)
    if request.method == "GET":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)
            
            data = request.body.decode('utf-8')
            data = {
                i.split('=')[0]: i.split('=')[1]
                for i in data.replace('%40', '@').split('&') if i.split('=')[1]
            }
            # data = GetRequestBody(request.body)

            k = data["ids[]"].split(',')
            
            for i in k:
                d = User_friend.objects.get(id=i)
                d.delete()

            return JsonResponse({"status":"0"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})

@csrf_exempt
def friemd_message(request, friend_id):  #親友團通知 api(36)
    if request.method == "POST":
        try:
            sid = request.COOKIES['sessionid']
            s = Session.objects.get(pk=sid)
            token = s.session_data
            now_account = s.get_decoded()['account']
            u = Patient.objects.get(username=now_account)

            message = request.POST['message']
            User_message.objects.create(username=u, message=message)
            return JsonResponse({"status":"0"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"1"})
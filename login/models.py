from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Patient(User):
    hasto_change_password = models.BooleanField(default=False)
    phone = models.CharField(max_length=17, blank=False, null=True)
    name = models.CharField(max_length=50, blank=False, null=True)
    birthday = models.DateField(blank=False, null=True)
    height = models.DecimalField(max_digits=19,
                                 decimal_places=16,
                                 blank=False,
                                 null=True)
    gender = models.CharField(max_length=1, blank=False, null=True)
    fcm_id = models.CharField(max_length=50, blank=False, null=True)
    address = models.CharField(max_length=50, blank=False, null=True)
    weight = models.DecimalField(max_digits=19,
                                 decimal_places=16,
                                 blank=False,
                                 null=True)
    fb_id = models.CharField(max_length=50, blank=False, null=True)
    status = models.CharField(max_length=50, default='Normal')
    group = models.CharField(max_length=50, blank=False, null=True)
    unread_records = models.DecimalField(max_digits=10,
                                             decimal_places=0,
                                             default=0)

    verified = models.CharField(max_length=1, default='0')
    privacy_policy = models.CharField(max_length=1, default='0')
    must_change_password = models.CharField(max_length=1, default='0')
    badge = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    login_times = models.DecimalField(max_digits=15,
                                      decimal_places=0,
                                      default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    invite_code = models.CharField(null=True, blank=True, max_length=20)

    def __str__(self):
        return self.username


class User_Medical(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    user_id = models.CharField(max_length=30, null=True)
    diabetes_type = models.CharField(max_length=1, null=True)
    oad = models.CharField(max_length=1, null=True)
    insulin = models.CharField(max_length=1, null=True)
    anti_hypertensives = models.CharField(max_length=1, null=True)
    recorded_at = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class User_Default(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    sugar_delta_max = models.DecimalField(max_digits=5,decimal_places=2,null = True)
    sugar_delta_min = models.DecimalField(max_digits=5,decimal_places=2,null = True)
    sugar_morning_max = models.DecimalField(max_digits=5,decimal_places=2,null = True)
    sugar_morning_min = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    sugar_evening_max = models.DecimalField(max_digits = 5 , decimal_places = 2, null = True)
    sugar_evening_min = models.DecimalField(max_digits = 5, decimal_places = 0,null = True)
    sugar_before_max = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    sugar_before_min = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    sugar_after_max = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    sugar_after_min = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    systolic_max = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    systolic_min = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    diastolic_max = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    diastolic_min = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    pulse_max = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    pulse_min = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    weight_max = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    weight_min = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    bmi_max = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    bmi_min = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    body_fat_max = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    body_fat_min = models.DecimalField(max_digits=5,decimal_places=0,null = True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class User_Setting(models.Model):

    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    
    after_recording = models.CharField(max_length=1, default='0')
    no_recording_for_a_day = models.CharField(max_length=1, default='0')
    over_max_or_under_min = models.CharField(max_length=1, default='0')
    after_meal = models.CharField(max_length=1, default='0')
    unit_of_sugar = models.CharField(max_length=1, default='0')
    unit_of_weight = models.CharField(max_length=1, default='0')
    unit_of_height = models.CharField(max_length=1, default='0')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)



class User_a1c(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    user_id = models.CharField(max_length=30, null=True)
    a1c = models.CharField(max_length=30, null=True)
    recorded_at = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class User_Care(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    user_id = models.CharField(max_length=30, null=True)
    care_message = models.CharField(max_length=20)
    # reply_id = models.CharField(max_length=30, null=True)  #發出訊息者
    created_at = models.DateTimeField(auto_now_add=True, null=True) 
    updated_at = models.DateTimeField(auto_now=True, null=True)
    pushed_at = models.DateTimeField(auto_now=True, null=True)


class User_Drug(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    user_id = models.CharField(max_length=30, null=True)
    drug_type = models.CharField(max_length=1, null=True)
    name = models.CharField(max_length=30, null=True)
    recorded_at = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class User_Share(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    user_id = models.CharField(max_length=30, null=True)
    share_type = models.CharField(max_length=1, null=True)
    share_id = models.CharField(max_length=30, null=True)
    relation_type = models.CharField(max_length=1, null=True)
    recorded_at = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class User_Badge(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    badge = models.CharField(max_length=30, null=True)

class User_blood_pressure(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    systolic = models.FloatField(default=5) #預設值為5
    diastolic = models.FloatField(default=5)
    pulse = models.IntegerField(default=5)
    recorded_at = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class User_body_weight(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    weight = models.FloatField(default=5)  #double用FloatField
    body_fat = models.FloatField(default=5)
    bmi = models.FloatField(default=5)
    recorded_at = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class User_blood_sugar(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    sugar = models.IntegerField(default=5)
    timeperiod = models.IntegerField(default=5)
    recorded_at = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class User_diet(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    description = models.IntegerField(default=5)
    meal = models.IntegerField(default=5) #使用者的時段 早餐 午餐 晚餐
    image_num = models.IntegerField(default=5) #照片數量
    image = models.ImageField(upload_to='image/')  #存放圖片的路徑
    tag = models.CharField(max_length=30, null=True)
    lat = models.FloatField(default=5) #緯度
    lng = models.FloatField(default=5) #經度
    recorded_at = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class User_invite(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    friend_type = models.IntegerField(default=2) # 0：醫師團 1：親友團 2：糖友團
    code = models.CharField(max_length=20)
    accept = models.BooleanField(default=None, null=True, blank=True) #接受了沒
    inviter_read = models.BooleanField(default=False) #使用者看過了沒
    created_at = models.DateTimeField(auto_now_add=True, null=True) #邀請發出時間
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
class User_friend(models.Model):
    Inviter = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True, related_name='Inviter')  #邀請者
    Invitee = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True, related_name='Invitee')  #受邀者
    friend_type = models.IntegerField(default=2) # 0：醫師團 1：親友團 2：糖友團
    created_at = models.DateTimeField(auto_now_add=True, null=True) #邀請發出時間
    updated_at = models.DateTimeField(auto_now=True, null=True)

class User_message(models.Model):
    username = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=20)
    # group_id = models.CharField(max_length=30, null=True)
    recorded_at = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True) 
    updated_at = models.DateTimeField(auto_now=True, null=True)
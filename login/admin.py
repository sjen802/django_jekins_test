from django.contrib import admin
from .models import *
# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display = ('username','id', 'invite_code')
class User_DefaultAdmin(admin.ModelAdmin):
    list_display = ('username','id')

class User_SettingAdmin(admin.ModelAdmin):
    list_display = ('username','id')

class User_a1cAdmin(admin.ModelAdmin):
    list_display = ('username','id')

class User_MedicalAdmin(admin.ModelAdmin):
    list_display = ('username',)

class  User_DrugAdmin(admin.ModelAdmin):
    list_display = ('username','id')

class  User_ShareAdmin(admin.ModelAdmin):
    list_display = ('username','id')

class  User_CareAdmin(admin.ModelAdmin):
    list_display = ('username','id')

class  User_BadgeAdmin(admin.ModelAdmin):
    list_display = ('username','id')

class User_blood_pressureAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'systolic', 'diastolic', 'pulse', 'recorded_at', 'created_at', 'updated_at')

class User_body_weightAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'weight', 'body_fat', 'bmi', 'recorded_at', 'created_at', 'updated_at')

class User_blood_sugarAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'sugar', 'timeperiod', 'recorded_at', 'created_at', 'updated_at')

class User_dietAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'description', 'meal', 'image_num', 'image', 'tag', 'lat', 'lng', 'recorded_at', 'created_at', 'updated_at')

class User_inviteAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'friend_type', 'code', 'accept', 'inviter_read','created_at', 'updated_at')

class User_friendAdmin(admin.ModelAdmin):
    list_display = ('Inviter', 'Invitee', 'friend_type', 'created_at', 'updated_at')

class User_messageAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'message', 'recorded_at', 'created_at', 'updated_at')
#admin.site.register(EmailAuth)
admin.site.register(Patient, PatientAdmin)
admin.site.register(User_Default, User_DefaultAdmin)
admin.site.register(User_Setting, User_SettingAdmin)
admin.site.register(User_a1c, User_a1cAdmin)
admin.site.register(User_Medical, User_MedicalAdmin)
admin.site.register(User_Drug, User_DrugAdmin)
admin.site.register(User_Care, User_CareAdmin)
admin.site.register(User_Badge, User_BadgeAdmin)
admin.site.register(User_blood_pressure, User_blood_pressureAdmin)
admin.site.register(User_body_weight, User_body_weightAdmin)
admin.site.register(User_blood_sugar, User_blood_sugarAdmin)
admin.site.register(User_diet, User_dietAdmin)
admin.site.register(User_invite, User_inviteAdmin)
admin.site.register(User_Share, User_ShareAdmin)
admin.site.register(User_friend, User_friendAdmin)
admin.site.register(User_message, User_messageAdmin)
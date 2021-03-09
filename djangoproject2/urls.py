"""djangoproject2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from login.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
urlpatterns = [
    path('here/',here),
    path('admin/', admin.site.urls),
    path('api/user/privacy-policy', privacy_policy),
    path('api/register/', register),
    path('api/verification/send/', verification_send),
    path('api/user/', user_information),
    path('api/auth/', user_auth),
    path('api/user/care/', user_care),
    path('api/user/medical/', user_medical),
    path('api/news/', user_news),
    path('api/user/a1c/', user_a1c),
    path('api/user/badge/', user_badge),
    path('api/user/blood/pressure/', blood_pressure),
    path('api/user/weight/', user_weight),
    path('api/user/blood/sugar/', blood_sugar),
    path('api/user/diary/', user_diary),
    path('api/friend/code/', get_friend_code),
    path('api/friend/send/', friend_send),
    path('api/friend/<int:invite_id>/accept/', friend_accept),
    path('api/friend/<int:invite_id>/refuse/', friend_refuse),
    path('api/friend/results/', friend_result),
    path('api/friend/list/', friend_list),
    path('api/friend/requests/', friend_request),
    path('api/share/', user_share),
    path('api/share/<int:friend_type>', user_sharee),
    path('api/user/default/', user_default),
    path('api/user/setting/', user_setting),
    path('api/friend/<int:friend_id>/remove/', invite_remove),
    path('api/friend/remove/', friend_remove),
    path('api/notification/', friemd_message),
    path('api/user/records/', records)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# @Time       : 2022/4/14 20:07
# @Author     : HUII
# @File       : urls.py
# @Description:

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from common.views.login_record import UserLoginRecordViewSet
from common.views.ocr import GetOcrUrlView, GetOcrVoiceView

router = DefaultRouter()
router.register('record', UserLoginRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ocr/url', GetOcrUrlView.as_view()),
    path('ocr/voice', GetOcrVoiceView.as_view()),
]

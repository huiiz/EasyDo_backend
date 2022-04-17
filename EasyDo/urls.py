# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from EasyDo.settings import MEDIA_ROOT
from utils import collect_news_by_time
urlpatterns = [
    path('', include(('common.urls', 'common'), namespace='common')),
    path('article/', include(('article.urls', 'article'), namespace='article')),
    path('system/', include(('system.urls', 'system'), namespace='system')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    re_path(r'media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
]

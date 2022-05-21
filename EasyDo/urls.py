# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from EasyDo.settings import MEDIA_ROOT

urlpatterns = [
    path('api/', include(('common.urls', 'common'), namespace='common')),
    path('api/article/', include(('article.urls', 'article'), namespace='article')),
    path('api/system/', include(('system.urls', 'system'), namespace='system')),
    path('api/auth/', include(('user.urls', 'user'), namespace='auth')),
    re_path(r'api/media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
]

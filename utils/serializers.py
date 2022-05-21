# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/1 001 22:47
@Remark: 自定义序列化器
"""
from django_restql.mixins import DynamicFieldsMixin
from rest_framework.fields import empty
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer


class CustomModelSerializer(DynamicFieldsMixin, ModelSerializer):
    """
    (1)self.request能获取到rest_framework.request.Request对象
    """

    def __init__(self, instance=None, data=empty, request=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.request: Request = request or self.context.get('request', None)

    def get_request_username(self):
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'username', None)
        return None

    def get_request_name(self):
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'name', None)
        return None

    def get_request_user_id(self):
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'id', None)
        return None

    def get_request_ip(self):
        return self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR', ''))

    def get_user_device(self):
        return self.request.environ.get("HTTP_USER_AGENT")

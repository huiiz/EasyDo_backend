# @Time       : 2022/4/14 23:50
# @Author     : HUII
# @File       : manager.py
# @Description:
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import Users
from utils.HMAC import get_sign
from utils.json_response import DetailResponse, ErrorResponse
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class LoginSerializer(TokenObtainPairSerializer):
    """
    登录的序列化器:
    重写djangorestframework-simplejwt的序列化器
    """

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]

    default_error_messages = {
        'no_active_account': _('账号/密码不正确'),
        'not_manager_yet': _('管理员申请尚未通过，请耐心等待')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        data = super().validate(attrs)
        self.user
        if self.user.manager_type <= 0:
            raise exceptions.AuthenticationFailed(
                self.error_messages["not_manager_yet"],
                "not_manager_yet",
            )
        return {
            "code": 2000,
            "msg": "请求成功",
            "data": data
        }


class LoginView(TokenObtainPairView):
    """
    登录接口
    """
    serializer_class = LoginSerializer
    permission_classes = []


class RegisterSerializer(CustomModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class RegisterViewSet(CustomModelViewSet):
    queryset = Users.objects
    create_serializer_class = RegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone', '')
        invite = request.data.get('invite', '')
        manage_type = 0
        if invite == get_sign('2' + phone):
            manage_type = 2
        elif invite == get_sign('3' + phone):
            manage_type = 3
        else:
            return ErrorResponse(msg='邀请码错误')
        usr = Users.objects.filter(phone=phone)
        if not usr:
            return ErrorResponse(msg='请先在手机应用上注册')
        usr = usr.get(phone=phone)
        if usr.manager_type > 0:
            return ErrorResponse(msg='你已是管理员')
        if usr.manager_type < 0:
            return ErrorResponse(msg='你已提交过申请')
        password = request.data.get('password', '')
        if len(password) < 6:
            return ErrorResponse(msg='密码过短')
        username = request.data.get('username', '')
        if Users.objects.exclude(id=usr.id).filter(username=username):
            return ErrorResponse(msg='用户名已被注册')
        usr.username = username
        usr.manager_type = -1 * manage_type
        usr.set_password(password)
        usr.save()
        return DetailResponse('申请已提交，请等待审核')


class UserInfoSerializer(CustomModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'avatar', 'manager_type']


class UserInfoViewSet(CustomModelViewSet):
    queryset = Users.objects
    serializer_class = UserInfoSerializer

    def list(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        res = serializer.data
        res['roles'] = [['BOSS', '用户管理员', '文章管理员'][res['manager_type'] - 1]]
        res.pop('manager_type')
        return DetailResponse(data=res, msg="获取成功")


class LogoutView(APIView):
    def post(self, request):
        return DetailResponse()

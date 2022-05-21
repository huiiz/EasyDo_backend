# @Time       : 2022/4/14 21:32
# @Author     : HUII
# @File       : login.py
# @Description:
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import Users
from utils.json_response import DetailResponse


# class UserSerializer(serializers.Serializer):
#     phone = serializers.CharField(max_length=11, min_length=11)
#
#     class Meta:
#         model = Users
#         fields = "__all__"
#         read_only_fields = ["id"]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # self.fields['phone'] = serializers.CharField(max_length=11, min_length=11)
#
#     def create(self, validated_data):
#         data = self.initial_data
#         usr = Users.objects.filter(phone=data['phone'])
#         if not usr:
#             usr = Users.objects.create(username=data['phone'], phone=data['phone'])
#             usr.set_password(data['phone'])
#             usr.save()
#             return usr
#         return usr[0]
#
#
# class UserLoginView(APIView):
#     """
#     登录接口
#     """
#     permission_classes = []
#
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#
#         if serializer.is_valid():
#             user = serializer.save()
#             token = RefreshToken.for_user(user)
#             return DetailResponse(data={'token': str(token)})
#         else:
#             return ErrorResponse()


class TestView(APIView):

    def get(self, request):
        print(request.user.id)
        return DetailResponse(data=request.user.username)


class LoginSerializer(TokenObtainPairSerializer):
    """
    登录的序列化器:
    重写djangorestframework-simplejwt的序列化器
    """

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'] = serializers.CharField(min_length=11, max_length=11)
        self.fields.pop('username')
        self.fields.pop('password')

    def validate(self, attrs):
        self.user = Users.objects.filter(**attrs)
        if not self.user:
            self.user = Users.objects.create(phone=attrs['phone'], username=attrs['phone'])
            self.user.set_password(attrs['phone'])
            self.user.save()
        else:
            self.user = self.user[0]
        refresh = self.get_token(self.user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        update_last_login(None, self.user)
        # data['username'] = self.user.name
        # data['userId'] = self.user.id
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

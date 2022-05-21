# @Time       : 2022/4/23 9:13
# @Author     : HUII
# @File       : create_invite_code.py
# @Description:
from rest_framework.views import APIView

from user.models import Users
from utils.HMAC import get_sign
from utils.json_response import ErrorResponse, DetailResponse
from utils.permission import BossPermission


class CreateInviteCodeView(APIView):
    permission_classes = [BossPermission]

    def post(self, *args, **kwargs):
        uid = self.request.data.get('uid', '')
        usr = Users.objects.get(id=uid)
        to_be_type = self.request.data.get('type', 0)
        if usr.manager_type == int(to_be_type):
            return ErrorResponse(msg='该用户已是该权限管理员')
        elif usr.manager_type == -1 * int(to_be_type):
            return ErrorResponse(msg='该用户已申请该权限管理员，请前往审核！')
        if to_be_type not in ['2', '3']:
            return ErrorResponse(msg='管理员类型错误')
        invite_code = get_sign(to_be_type + usr.phone)
        return DetailResponse(data={
            'invite': invite_code
        })

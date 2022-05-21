# @Time       : 2022/5/5 19:56
# @Author     : HUII
# @File       : user_list.py
# @Description:
from user.models import Users
from utils.pagination import CustomPagination
from utils.permission import UserManagePermission
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class UserListSerializer(CustomModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'phone', 'create_datetime', 'manager_type']


class UserListViewSet(CustomModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [UserManagePermission]
    pagination_class = CustomPagination





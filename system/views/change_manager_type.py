# @Time       : 2022/5/5 20:00
# @Author     : HUII
# @File       : change_manager_type.py
# @Description:
from user.models import Users
from utils.permission import BossPermission
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class ManagerTypeChangeSerializer(CustomModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'avatar', 'manager_type']

    def update(self, instance, validated_data):
        manager_type = instance.manager_type
        allow = self.request.data.get('allow') == '1'
        if allow:
            if manager_type < 0:
                instance.manager_type = -1 * manager_type
        else:
            instance.manager_type = 0
        instance.save()
        return instance


class ManagerTypeChangeViewSet(CustomModelViewSet):
    queryset = Users.objects
    update_serializer_class = ManagerTypeChangeSerializer
    permission_classes = [BossPermission]

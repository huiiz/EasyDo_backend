# @Time       : 2022/4/21 20:24
# @Author     : HUII
# @File       : login_record.py
# @Description:

from user.models import LoginRecord
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class UserLoginRecordSerializer(CustomModelSerializer):
    class Meta:
        model = LoginRecord

        fields = []

    def create(self, validated_data):
        validated_data['uid_id'] = self.get_request_user_id()
        validated_data['ip'] = self.get_request_ip()
        validated_data['device'] = self.get_user_device()
        login_record = super().create(validated_data)
        return login_record


class UserLoginRecordViewSet(CustomModelViewSet):
    queryset = LoginRecord.objects
    create_serializer_class = UserLoginRecordSerializer
    # serializer_class = UserLoginRecordSerializer



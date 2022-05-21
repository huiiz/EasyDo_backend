# @Time       : 2022/4/22 23:32
# @Author     : HUII
# @File       : HMAC.py
# @Description:
import base64
import hmac
from hashlib import sha256


def get_sign(data, key='EasydO'):
    key = key.encode('utf-8')
    message = data.encode('utf-8')
    sign = base64.b64encode(hmac.new(key, message, digestmod=sha256).digest())
    sign = str(sign, 'utf-8')
    return sign[:10]


if __name__ == '__main__':
    print(get_sign('213000000000'))

# @Time       : 2022/5/20 17:08
# @Author     : HUII
# @File       : ecloud.py
# @Description: 获得移动云接口服务
import copy
import hmac
import time
import urllib
import uuid
from hashlib import sha1, sha256

import requests

from utils.read_config import get_config

access_key = get_config("ecloud_account", "access_key")
secret_key = get_config("ecloud_account", "secret_key")


# 签名计算
def sign(http_method, playlocd, servlet_path):
    time_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    playlocd['Timestamp'] = time_str
    parameters = copy.deepcopy(playlocd)
    parameters.pop('Signature')
    sorted_parameters = sorted(
        parameters.items(), key=lambda parameters: parameters[0])
    canonicalized_query_string = ''
    for (k, v) in sorted_parameters:
        canonicalized_query_string += '&' + \
                                      percent_encode(k) + '=' + percent_encode(v)
    string_to_sign = http_method + '\n' + percent_encode(servlet_path) + '\n' \
                     + sha256(canonicalized_query_string[1:].encode('utf-8')).hexdigest()

    key = ("BC_SIGNATURE&" + secret_key).encode('utf-8')
    string_to_sign = string_to_sign.encode('utf-8')
    signature = hmac.new(key, string_to_sign, sha1).hexdigest()
    return signature


# 参数编码

def percent_encode(encode_str):
    encode_str = str(encode_str)
    res = urllib.parse.quote(encode_str.encode('utf-8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def request_ecloud_api(method='POST', url='', path='', payload={}):
    """
    向api请求
    :param method: 请求方式，POST或GET，默认POST
    :param url: 请求域名+端口
    :param path: 请求路径，以/开头
    :param payload: 请求数据
    :return: json格式
    """
    headers = {'Content-Type': 'application/json'}
    req_url = get_authed_request_url(method, url, path)
    res = requests.request(method, req_url, headers=headers, json=payload)
    return res.json()


def get_authed_request_url(method='POST', url='', path=''):
    """
    获取鉴权url
    :param method: 请求方式，POST或GET，默认POST
    :param url: 请求域名+端口
    :param path: 请求路径，以/开头
    :return:
    """
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(time.time()))
    # 签名公参，如果有其他参数，同样在此添加
    querystring = {"AccessKey": access_key, "Timestamp": timestamp, "Signature": "", "SignatureMethod": "HmacSHA1",
                   "SignatureVersion": "V2.0", 'SignatureNonce': uuid.uuid4()}
    querystring['Signature'] = sign(method, querystring, path)
    s = '&'.join([f'{k}={v}' for k, v in querystring.items()])
    return f'{url}{path}?{s}'

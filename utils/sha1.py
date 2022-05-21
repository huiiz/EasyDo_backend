# @Time       : 2022/5/20 17:55
# @Author     : HUII
# @File       : sha1.py
# @Description: sha1定长加密算法
import hashlib


def get_sha1(s: str):
    sha = hashlib.sha1(s.encode('utf-8'))
    encrypts = sha.hexdigest()
    return encrypts


if __name__ == '__main__':
    print(get_sha1('合肥工业大学'))

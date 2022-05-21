# @Time       : 2022/5/21 14:57
# @Author     : HUII
# @File       : search_caches.py
# @Description: 搜索缓存
from django.core.cache import cache


def set_cache(key: str, value: str) -> None:
    """
    将搜索转化后字符与对应的原始内容保存在redis中
    :param key: 转换后的内容
    :param value: 转化前的原始搜索内容
    :return: None
    """
    cache.set(key, value, timeout=30 * 60)


def get_cache(key: str) -> str:
    """
    使用转化后字符找到与对应的原始内容
    :param key:
    :return:
    """
    return cache.get(key)

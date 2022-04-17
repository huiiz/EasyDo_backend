# @Time       : 2022/4/15 23:29
# @Author     : HUII
# @File       : initialize.py
# @Description: 初始化数据
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyDo.settings')
django.setup()
from article.models import ArticleCategory

cates = [
    '国内', '国际', '军事', '财经', '娱乐', '体育', '互联网', '科技', '游戏', '女人', '汽车', '房产'
]
# 创建分类
# for cate in cates:
#     ArticleCategory.objects.create(name=cate)
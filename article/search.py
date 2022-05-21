# @Time       : 2022/5/20 23:00
# @Author     : HUII
# @File       : search.py
# @Description: 搜索文章
import os

import django

if __name__ != '__main__':
    from article.models import Article


def search_from_article(keyword: str):
    temp_ls1 = [f"Q(title__icontains='{i}')" for i in list(keyword)]
    temp_ls2 = [f"Q(content__icontains='{i}')" for i in list(keyword)]
    a = Article.objects.filter(status=True).filter(eval('&'.join(temp_ls1)) | eval('&'.join(temp_ls2)))
    return a

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyDo.settings')
    django.setup()
    from article.models import Article

    print(search_from_article('中华人民共和国中央人民政府').values_list(flat=True))

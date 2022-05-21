from django.db import models

from utils.models import CoreModel, table_prefix


class ArticleCategory(CoreModel):
    name = models.CharField(max_length=32, verbose_name='文章分类名', null=True, blank=True)
    ordering = models.IntegerField(default=0, verbose_name='排序', help_text='号大优先，同号者id小优先')

    class Meta:
        db_table = table_prefix + "article_category"
        verbose_name = '文章分类表'
        verbose_name_plural = verbose_name
        ordering = ('ordering', 'id')


class Article(CoreModel):
    title = models.CharField(max_length=255, verbose_name='文章标题', null=True)
    post_time = models.CharField(max_length=32, verbose_name='发布时间', null=True, blank=True)
    source = models.CharField(max_length=64, verbose_name='文章来源', null=True, blank=True)
    category = models.ForeignKey(to='ArticleCategory', verbose_name='文章分类', on_delete=models.CASCADE,
                                 db_column='category',
                                 db_constraint=False, null=True, blank=True, help_text="文章分类")
    tags = models.JSONField(verbose_name="文章标签", help_text="文章标签", null=True, blank=True)
    content = models.TextField(null=True, blank=True, verbose_name='文章内容', help_text='文章内容')
    count = models.IntegerField(verbose_name='阅读数', default=0)
    status = models.BooleanField(verbose_name='文章状态', help_text='文章状态，True为正常，False为禁用', default=True)

    class Meta:
        db_table = table_prefix + "article"
        verbose_name = '文章表'
        verbose_name_plural = verbose_name
        ordering = ('-id',)


class ReadingRecord(CoreModel):
    article = models.ForeignKey(to='Article', verbose_name='文章', db_column='article', on_delete=models.CASCADE,
                                db_constraint=False, null=True, blank=True, help_text="文章")
    user = models.ForeignKey(to='user.Users', verbose_name='用户', db_column='user', on_delete=models.CASCADE,
                             db_constraint=False, null=True, blank=True, help_text="用户")
    # article_cate = models.ForeignKey(to='ArticleCategory', verbose_name='对应文章分类', db_column='acate',
    #                                  on_delete=models.CASCADE,
    #                                  db_constraint=False, null=True, blank=True, help_text="对应文章分类")

    class Meta:
        db_table = table_prefix + "reading_record"
        verbose_name = '用户阅读记录表'
        verbose_name_plural = verbose_name
        ordering = ('-id',)

# class RecommendRecord(CoreModel):

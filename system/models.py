from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.models import CoreModel, table_prefix


#
# class Manager(AbstractUser, CoreModel):
#     username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name='用户账号', help_text="用户账号")
#     avatar = models.CharField(max_length=255, verbose_name="头像", null=True, blank=True, help_text="头像",
#                               default='https://i0.hdslb.com/bfs/article/4bff13b0fef946464e8f155e33cfbeb73269e127.gif')
#     MANAGER_TYPE = (
#         (0, "普通用户"),
#         (1, "大BOSS"),
#         (2, "用户管理员"),
#         (3, "文章管理员"),
#     )
#     manager_type = models.IntegerField(choices=MANAGER_TYPE, default=2, verbose_name="管理员类型", null=True, blank=True,
#                                        help_text="用户类型")
#
#
#     def set_password(self, raw_password):
#         super().set_password(hashlib.md5(raw_password.encode(encoding='UTF-8')).hexdigest())
#
#     class Meta:
#         db_table = table_prefix + "system_manager"
#         verbose_name = '用户表'
#         verbose_name_plural = verbose_name
#         ordering = ('-create_datetime',)


class OperationLog(CoreModel):
    request_modular = models.CharField(max_length=64, verbose_name="请求模块", null=True, blank=True, help_text="请求模块")
    request_path = models.CharField(max_length=400, verbose_name="请求地址", null=True, blank=True, help_text="请求地址")
    request_body = models.TextField(verbose_name="请求参数", null=True, blank=True, help_text="请求参数")
    request_method = models.CharField(max_length=8, verbose_name="请求方式", null=True, blank=True, help_text="请求方式")
    request_msg = models.TextField(verbose_name="操作说明", null=True, blank=True, help_text="操作说明")
    request_ip = models.CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True, help_text="请求ip地址")
    request_browser = models.CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True, help_text="请求浏览器")
    response_code = models.CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True, help_text="响应状态码")
    request_os = models.CharField(max_length=64, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    json_result = models.TextField(verbose_name="返回信息", null=True, blank=True, help_text="返回信息")
    status = models.BooleanField(default=False, verbose_name="响应状态", help_text="响应状态")

    class Meta:
        db_table = table_prefix + 'system_operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Config(CoreModel):
    key = models.CharField(max_length=64, verbose_name="键", null=True, blank=True, help_text="配置键")
    value = models.TextField(verbose_name="值", null=True, blank=True, help_text="配置值")

    class Meta:
        db_table = table_prefix + 'system_config'
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name
        ordering = ('id',)
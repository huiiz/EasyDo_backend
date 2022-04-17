import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.models import CoreModel, table_prefix


class Users(AbstractUser, CoreModel):
    phone = models.CharField(max_length=11, verbose_name='手机号')
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name='用户账号', help_text="用户账号")
    avatar = models.CharField(max_length=255, verbose_name="头像", null=True, blank=True, help_text="头像",
                              default='https://i0.hdslb.com/bfs/article/4bff13b0fef946464e8f155e33cfbeb73269e127.gif')
    MANAGER_TYPE = (
        (0, "普通用户"),
        (1, "大BOSS"),
        (2, "用户管理员"),
        (3, "文章管理员"),
    )
    manager_type = models.IntegerField(choices=MANAGER_TYPE, default=0, verbose_name="用户类型", null=True, blank=True,
                                       help_text="用户类型")

    def set_password(self, raw_password):
        super().set_password(hashlib.md5(raw_password.encode(encoding='UTF-8')).hexdigest())

    class Meta:
        db_table = table_prefix + "users"
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class LoginRecord(CoreModel):
    uid = models.ForeignKey(to='Users', verbose_name='用户', on_delete=models.CASCADE, db_column='uid',
                            db_constraint=False, null=True, blank=True, help_text="登录用户")
    ip = models.GenericIPAddressField(verbose_name='登录IP地址')
    device = models.CharField(max_length=255, verbose_name='用户设备型号')

    class Meta:
        db_table = table_prefix + "login_record"
        verbose_name = '登录记录表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

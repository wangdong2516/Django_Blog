from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
	"""
		自定义用户模型类，继承AbstractUser
		配置项：AUTH_USER_MODEL指向的模型类
		里面有username的验证，password的验证和first_name，last_name，email，is_staff，is_active
		等字段的定义
	"""
	mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
	email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

	class Meta:
		db_table = 'users'
		verbose_name = '用户'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.username

	def get_absolute_url(self) -> str:
		"""
			定义该对象使用的url，如果对象定义了此方法，则在后台站点对象编辑页面上将具有“在站点上查看”链接
		:return: url
		"""
		return "/user/%i/" % self.id

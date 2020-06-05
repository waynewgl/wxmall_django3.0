# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from DjangoUeditor.models import UEditorField
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe

from ckeditor_uploader.fields import RichTextUploadingField


from mBusi import settings as setting


import uuid
import os
import calendar, time, datetime


def timestamp():
    return 0


# Create your models here.
class ProfileType(models.Model):
    class Meta:
        verbose_name = u'用户类型'
        verbose_name_plural = u'用户类型'

    name = models.CharField(u'用户类型', max_length=20, default="补货员")
    description = models.CharField(u'描述', max_length=1024, default="")

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name


class shopType(models.Model):
    class Meta:
        verbose_name = u'商家类型'
        verbose_name_plural = u'商家类型'

    def get_file_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        return os.path.join('uploads/shop_type/', filename)

    name = models.CharField(u'商家型号名称', max_length=1024, null=True, default='')
    description = models.TextField(u'描述', blank=True,  default='')

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name


# user model  -> inherit default model
class Profile(AbstractUser):
    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'

    def get_avatar_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        userPath = 'uploads/avatar/' + str(self.company.id) + '/'
        return os.path.join(userPath, filename)

    SEX_CHOICES = (
        ('未知', "未知"),
        ('男', "男"),
        ('女', "女"),
    )

    sex = models.CharField(u'性别',  choices=SEX_CHOICES, default='未知', max_length=50, null=True)
    birthDate = models.DateField(u'出生日期', blank=True, null=True, default='1970-01-01')
    nickname = models.CharField(u'昵称', max_length=50, default="", null=True)

    city = models.CharField(u'城市', max_length=50, default="", null=True, blank=True)
    province = models.CharField(u'省份', max_length=50, default="", null=True, blank=True)
    country = models.CharField(u'国家', max_length=50, default="", null=True, blank=True)

    mobile = models.CharField(
        u'手机账号',
        max_length=255,
        help_text=_('手机账号'),
        error_messages={
            'unique': _("该手机号已被注册."),
        },
    )

    wx_openid = models.CharField(u'微信唯一标识符openId', unique=True, max_length=50, null=True, blank=True)

    avatar = models.ImageField(upload_to=get_avatar_path, null=True, blank=True)
    avatarUrl = models.CharField(u'微信图像URL', max_length=500, null=True, blank=True)
    # companyName = models.CharField(u'公司名字', max_length=50, blank=True, default='', null=True)
    userType = models.ForeignKey(ProfileType, verbose_name='用户类型', on_delete=models.CASCADE, default='', null=True,
                                 blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='所属公司', null=True)

    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='上级用户', null=True, blank=True)

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):
            # 在Python3中使用 def __str__(self):
            return self.username + ' - 公司: ' + str(self.company)


class UserAddress(models.Model):
    class Meta:
        verbose_name = u'用户地址'
        verbose_name_plural = u'用户地址'

    province = models.CharField(u'省份', max_length=50, default="", null=True)
    city = models.CharField(u'市', max_length=50, default="", null=True)
    district = models.CharField(u'区', max_length=50, default="", null=True)
    cityCode = models.CharField(u'区域码', max_length=50, default="", null=True)
    address = models.CharField(u'地址详情', max_length=50, default="", null=True)
    mobile = models.CharField(u'手机号码', max_length=50, default="", null=True)

    user_id = models.ForeignKey('Profile', db_column='user_id',  on_delete=models.CASCADE, verbose_name='所属用户', null=True, blank=True)

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):
            # 在Python3中使用 def __str__(self):
            return self.province + self.city + self.district + self.address


class CompanyType(models.Model):
    class Meta:
        verbose_name = u'公司类型'
        verbose_name_plural = u'公司类型'

    type = models.IntegerField(
        u' 0：未知，1：加盟公司，2：总公司 ',
        default=0,
        validators=[MaxValueValidator(2), MinValueValidator(0)]
    )
    name = models.CharField(u'类型名称', max_length=20, null=True, default='')
    describe = models.CharField(u'类型描述', max_length=200, null=True, default='')

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name


class Company(models.Model):
    class Meta:
        verbose_name = u'公司'
        verbose_name_plural = u'公司'

    def get_logo_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        path = 'uploads/company/' + str(self.leader.id) + '/'
        return os.path.join(path, filename)

    def get_acc_file_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        path = 'uploads/company/' + str(self.leader.id) + '/acc/file/'
        return os.path.join(path, filename)

    def get_acc_img_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        path = 'uploads/company/' + str(self.leader.id) + '/acc_img/'
        return os.path.join(path, filename)

    def get_public_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        path = 'uploads/company/' + str(self.leader.id) + '/' + 'publicKey/'
        # print(path)
        return os.path.join(path, filename)

    def get_private_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        path = 'uploads/company/' + str(self.leader.id) + '/' + 'privateKey/'
        return os.path.join(path, filename)

    name = models.CharField(u'公司名称', max_length=100, default='', unique=True)
    address = models.CharField(u'公司地址', max_length=100, null=True, default='')
    mobile = models.CharField(u'公司电话', max_length=100, null=True, default='')
    logo = models.ImageField(upload_to=get_logo_path, null=True, blank=True)
    describe = models.CharField(u'公司简介', max_length=500, null=True, default='')
    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    offic_acc_url = models.CharField(u'公众号URL', max_length=100, null=True, default='')
    offic_acc_contents = RichTextUploadingField(u'公众号内容', blank=True, default='')

    ali_appId = models.CharField(u'支付宝-公司支付APPID', max_length=255, null=True, blank=True, default='')
    ali_publicKey = models.TextField(u'支付宝-支付宝公钥', null=True, blank=True)
    ali_privateKey = models.TextField(u'支付宝-应用私钥', null=True, blank=True)
    ali_notifyUrl = models.CharField(u'支付宝-支付通知url', max_length=255,  null=True, blank=True)

    leader = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='公司负责人', related_name='leader')
    type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, verbose_name='公司类型')

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name


class shopAdsType(models.Model):
    class Meta:
        verbose_name = u'商家广告类型'
        verbose_name_plural = u'商家广告类型'

    adsType = models.IntegerField(
        u'0- 图片, 1 - 视频, 2 - 商品分类, 3 - 商品,  4 - 其他（可以自定义）',
        unique=True,
        default=0,
        validators=[MaxValueValidator(4), MinValueValidator(0)]
    )

    description = models.TextField(u'描述', blank=True, default='', max_length=120)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='所属公司', null=True)

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return str(self.description)


class WaShopAds(models.Model):
    class Meta:
        verbose_name = u'商家广告'
        verbose_name_plural = u'商家广告'

    def get_file_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        return os.path.join('uploads/ads/', filename)

    img = models.FileField(u'媒体文件', upload_to=get_file_path)
    title = models.CharField(u'标题', max_length=1024, null=True, default='')
    # type = models.CharField(u'类型', max_length=1024, null=True, default='')
    description = models.TextField(u'描述', blank=True, default='', max_length=1024)
    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    shopAdsType = models.ForeignKey(shopAdsType, on_delete=models.CASCADE, verbose_name='广告类型', null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='所属公司', null=True)

    category = models.ForeignKey('ShopItemCategory', db_column='category_id', on_delete=models.CASCADE, verbose_name='所属商品种类', null=True,
                                 blank=True)
    shopItem = models.ForeignKey('ShopItem', db_column='shopItem_id', on_delete=models.CASCADE, verbose_name='所属商品', null=True, blank=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return " " + self.title + "  " + self.description

    def image_tag(self):
        if self.img:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.img.url)
        else:
            return '无'
    image_tag.short_description = '图片'


class Tag(models.Model):
    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u'标签'

    title = models.CharField(
        _('标签名称'),
        unique=True,
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A title with that tag already exists."),
        },
    )
    description = models.TextField(u'描述', default="", blank=True)
    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.title


class Brand(models.Model):
    class Meta:
        verbose_name = '商品品牌'
        verbose_name_plural = '商品品牌'

    title = models.CharField(
        _('标签名称'),
        unique=True,
        max_length=255,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        default='默认',
        error_messages={
            'unique': _("该品牌已经存在"),
        },
    )

    status = models.IntegerField(
        u'0- 未激活, 1 - 激活, 2- 过期',
        default=1,
        validators=[MaxValueValidator(2), MinValueValidator(0)]
    )
    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    description = models.TextField(u'描述', default="", blank=True)

    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='所属公司', null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
            return self.title


class ShopItemCategory(models.Model):
    class Meta:
        verbose_name = u'商品种类'
        verbose_name_plural = u'商品种类'

    def get_shopItemCategory_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        path = 'uploads/company/' + str(self.company.id) + '/shopItemCategory/'
        return os.path.join(path, filename)

    pagePriority = models.IntegerField(
        u'0- 其他, 1 - 首页 (应用APP或小程序放置位置)',
        default=0,
        validators=[MaxValueValidator(1), MinValueValidator(0)],
    )

    img = models.FileField(u'小图', upload_to=get_shopItemCategory_path, null=True, blank=True)
    img_large = models.FileField(u'大图', upload_to=get_shopItemCategory_path, null=True, blank=True)

    name = models.CharField(u'商品种类名称', max_length=1024, null=True, default='')
    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='所属公司', null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name


class WaShop(models.Model):
    class Meta:
        verbose_name = u'商家'
        verbose_name_plural = u'商家'
        permissions = (
            ('view_shop', 'View shop'),
        )

    def get_shop_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        path = 'uploads/shop/' + str(self.company.id) + '/'
        return os.path.join(path, filename)

    name = models.CharField(u'商家名称', max_length=1024, null=True, default='')
    img = models.FileField(upload_to=get_shop_path, null=True, blank=True)
    description = models.TextField(u'描述', blank=True, default='', max_length=1024)

    shopSn = models.CharField(
        u'商家SN',
        unique=True,
        max_length=50,
        help_text=_('商家sn'),
        error_messages={
            'unique': _("商家SN已经存在"),
        },
    )

    status = models.IntegerField(
        u'0：未激活状态，1：正常运作, 2：注销，',
        help_text='0：未激活状态，1：正常运作, 2：注销，',
        default=1,
        validators=[MaxValueValidator(2), MinValueValidator(0)]
    )

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    shopType = models.ForeignKey(shopType, on_delete=models.CASCADE, verbose_name='所属商家类型', null=True, blank=True)
    shopAds = models.ManyToManyField(WaShopAds, verbose_name='广告', blank=True)
    owner = models.ForeignKey('Profile', verbose_name='店长', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='所属公司', null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
            return '(商家ID ' + str(self.id) + ") - " + self.name + " - 所属公司(厂家): " + str(self.company)


class ShopItem(models.Model):
    class Meta:
        verbose_name = u'商品'
        verbose_name_plural = u'商品'

    def get_shopItem_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        path = 'uploads/shopItem/' + str(self.category.id) + '/'
        return os.path.join(path, filename)

    title = models.CharField(
        _('商品名称'),
        unique=True,
        max_length=255,
        default='默认',
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("该商品已经存在"),
        },
    )

    description = models.CharField(u'描述', blank=True, max_length=1024)
    content = RichTextUploadingField(u'商品内容', blank=True, default='')

    price = models.FloatField(
        u'零售价格',
        validators=[MaxValueValidator(9999999), MinValueValidator(0)],
        error_messages={
            'unique': _("价格不能低于0"),
        }
    )

    storage = models.IntegerField(
        u'当前存货',
        help_text='当前存货',
        validators=[MaxValueValidator(99999), MinValueValidator(0)],
        error_messages={
            'unique': _("当前存货不能低于"),
        }
    )

    originalPrice = models.FloatField(u'出厂价格', help_text=u'出厂价格',
                                      validators=[MaxValueValidator(9999999), MinValueValidator(0)], null=True)

    status = models.IntegerField(
        u'-0- 未激活, 1 - 激活, 2 - 过期',
        default=1,
        validators=[MaxValueValidator(2), MinValueValidator(0)]
    )

    totalSell = models.IntegerField(
        u'销量', help_text=u'销量',
        default=0,
        null=True,
        blank=True,
        validators=[MaxValueValidator(9999999), MinValueValidator(0)]
    )

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    img = models.FileField(u'图片', upload_to=get_shopItem_path, null=True, blank=True)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='所属品牌', null=True)
    # tags = models.ManyToManyField(Tag, verbose_name='标签')

    shop = models.ForeignKey(WaShop, verbose_name='商家', on_delete=models.CASCADE)
    category = models.ForeignKey(ShopItemCategory, on_delete=models.CASCADE, verbose_name='商品种类', null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.title
               # + " " + str(timezone.localtime(self.pub_date).strftime('%Y/%m/%d  %H:%M'))

    def image_tag(self):
        if self.img:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.img.url)
        else:
            return '无'
    image_tag.short_description = '图片'


class shopOperationCode(models.Model):
    class Meta:
        unique_together = (('shopSn', 'shopVerifyCode'),)
        verbose_name = u'店家操作校验'
        verbose_name_plural = u'商品种类'

    shopSn = models.CharField(verbose_name='所属店家', max_length=255)
    shopVerifyCode = models.CharField(u'店家操作校验码', max_length=200, null=True, default='')
    codeUpdateTime = models.CharField(u'验证码更新时间戳', max_length=200, null=True, default='')
    timeExpired = models.CharField(u'检验码过期时间间隔', max_length=1024, null=True, default='2')
    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)


class ItemOrder(models.Model):
    class Meta:
        verbose_name = u'商品订单'
        verbose_name_plural = u'商品订单'

    orderNum = models.BigIntegerField(u'订单号', primary_key=True, error_messages={
            'unique': _("订单号重复"),
        })

    orderTitle = models.CharField(u'订单标题', max_length=255, error_messages={
            'null': _("需要提供商品名称或者相关标题"),
        })

    totalPrice = models.FloatField(u'总价', error_messages={
            'null': _("需要提供商品总价"),
        })

    orderAddress = models.CharField(u'订单快递位置', max_length=500, default='', error_messages={
            'null': _("订单快递位置"),
        })

    shopItem = models.ManyToManyField(ShopItem, through='ItemOrderShopItems', verbose_name='所属商品', help_text='',
                                      error_messages={'null': _("需要提供该订单的商品ID")})

    shop = models.ForeignKey(WaShop, on_delete=models.CASCADE, verbose_name='所属商家',  help_text='shop_id', null=True,
                               error_messages={'null': _("需要提供所属商家ID")})

    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='所属公司', help_text='company_id',
                                null=True, error_messages={'null': _("需要提供公司ID")})

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='所属用户', help_text='user_id', null=True, blank=True, error_messages={'null': _("需要提供购买用户ID")})

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    update_timestamp = models.BigIntegerField(u'操作时间戳',  null=True, blank=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return ''


class ItemOrderShopItems(models.Model):
    class Meta:
        verbose_name = u'商品订单详情列表'
        verbose_name_plural = u'商品订单详情列表'

    shopItem = models.ForeignKey(ShopItem, verbose_name='商品', on_delete=models.CASCADE, related_name='shopItems',
                                 null=True)
    itemOrder = models.ForeignKey(ItemOrder, verbose_name='所属订单', on_delete=models.CASCADE, related_name='itemOrders',
                                  null=True)

    totalBuy = models.IntegerField(u'商品购买数量', default=0, validators=[MaxValueValidator(999999), MinValueValidator(0)])
    totalPrice = models.FloatField(u'总价',  default=0, validators=[MaxValueValidator(999999), MinValueValidator(0)])
    price = models.FloatField(u'单价', default=0, validators=[MaxValueValidator(999999), MinValueValidator(0)])

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return '订单:' + str(self.itemOrder.orderNum) + " -  " + '\n 商品名称: ' + str(self.shopItem.title) +\
               " - " + "\n 总价:" + str(self.totalPrice)


class ItemOrderStatus(models.Model):
    class Meta:
        verbose_name = u'订单状态'
        verbose_name_plural = u'订单状态'

    orderStatus = models.IntegerField(
        u'0- 等待支付中, 1 - 已支付, 2 - 已取消, 3 - 未付款交易超时关闭，或支付完成后全额退款, 4 - 退款中 5- 该订单未被扫描 6- 交易结束，不可退款  ',
        help_text='0- 等待支付中, 1 - 已支付, 2 - 已取消, 3 - 未付款交易超时关闭，或支付完成后全额退款, 4 - 退款中 5- 该订单未被扫描 6- 交易结束，不可退款  ',
        default=0,
        validators=[MaxValueValidator(6), MinValueValidator(0)],
        null=True
    )

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    update_timestamp = models.BigIntegerField(u'操作时间戳', null=True)

    buyer_user_id = models.CharField(max_length=255, help_text='支付宝用户ID, 默认生成, 无需填写', null=True, blank=True)
    buyer_logon_id = models.CharField(max_length=255, help_text='支付宝用户登录ID, 默认生成, 无需填写', null=True, blank=True)

    company_id = models.IntegerField(help_text='公司ID', null=True, blank=True)
    orderNum = models.OneToOneField(ItemOrder, primary_key=True, default=1, on_delete=models.CASCADE, verbose_name='所属订单',
                                    help_text='itemOrder_id', error_messages={'null': _("需要提供该订单的商品ID")})

    orderCompleteStatus = models.IntegerField(
        u'0 - 未出货 1 - 已出货  2-部分出货',
        help_text='0 - 未出货, 1 -已出货  2-部分出货',
        default=0,
        validators=[MaxValueValidator(2), MinValueValidator(0)],
        null=True
    )

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return str(self.orderNum) + ' : ' + str(self.buyer_user_id) + ' : ' + str(self.buyer_logon_id)


class Comment(models.Model):
    class Meta:
        verbose_name = u'商品评论'
        verbose_name_plural = u'商品评论'

    title = models.CharField(u'标题', max_length=1024, null=True, default='')
    description = models.CharField(u'描述', blank=True, max_length=1024)

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='所属用户')
    shopItem = models.ForeignKey(ShopItem, on_delete=models.CASCADE,  verbose_name='所属商品')

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return str(self.id) + " " + self.title


class ProfileAvatar(models.Model):
    class Meta:
        verbose_name = u'头像'
        verbose_name_plural = u'头像'

    img = models.FileField(upload_to='upload/avatar')
    # article = models.ForeignKey(Article, default="")
    upload_time = models.DateTimeField(u'上传时间', auto_now=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.img.url


class ImageUploader(models.Model):
    class Meta:
        verbose_name = u'商品图片'
        verbose_name_plural = u'商品图片'

    def get_shopItem_path(self, filename):
        # ext = filename.split('.')[-1]
        filename = "%s-%s" % (uuid.uuid4(), filename)
        path = 'uploads/shopitem/' + str(self.shopItem.id) + '/'
        return os.path.join(path, filename)

    img = models.FileField(u'图片', upload_to=get_shopItem_path)
    # article = models.ForeignKey(Article, default="")
    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    shopItem = models.ForeignKey(ShopItem, on_delete=models.CASCADE)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.img.url + " " + self.shopItem.title


class AreasInfo(models.Model):
    id = models.CharField(u'区域编号', primary_key=True, max_length=50, default='0')
    name = models.CharField(u'区域名称', max_length=50, null=True, default='')
    areaLevel = models.CharField(u'区域层级', max_length=50, null=True, default='')
    parent_id = models.CharField(u'区域母编号', max_length=50, null=True, default='')

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.id + ' name:' + self.name


class shopLocation(models.Model):
    class Meta:
        verbose_name = u'商家地址'
        verbose_name_plural = u'商家地址'

    # status = models.IntegerField(
    #     u'-0-不使用 , 1 - 当前使用, 2 - 过期',
    #     default=0,
    #     validators=[MaxValueValidator(2), MinValueValidator(0)]
    # )

    longitude = models.CharField(u'经度', max_length=50, null=True, default='', blank=True)
    latitude = models.CharField(u'纬度', max_length=50, null=True, default='', blank=True)
    provinceKey = models.CharField(u'省份编码', max_length=50, null=True, default='', blank=True)
    provinceName = models.CharField(u'省份', max_length=50, null=True, default='', blank=True)
    cityKey = models.CharField(u'县市编码', max_length=50, null=True, default='', blank=True)
    cityName = models.CharField(u'县市', max_length=50, null=True, default='', blank=True)
    regionKey = models.CharField(u'区编码', max_length=50, null=True, default='', blank=True)
    regionName = models.CharField(u'区', max_length=50, null=True, default='', blank=True)
    # fullAddress = models.CharField(u'全部地址', max_length=200, null=True, default='', blank=True)
    addressDetail = models.CharField(u'地址详情', max_length=200, null=True, default='', blank=True)

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    shop = models.OneToOneField(WaShop, primary_key=True, on_delete=models.CASCADE, verbose_name='所属商家')

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return str(self.provinceName) + str(self.cityName) + str(self.regionName) + str(self.addressDetail)


class shopLocationHistory(models.Model):
    class Meta:
        verbose_name = u'商家历史地址'
        verbose_name_plural = u'商家历史地址'

    # status = models.IntegerField(
    #     u'-0-不使用 , 1 - 当前使用, 2 - 过期',
    #     default=0,
    #     validators=[MaxValueValidator(2), MinValueValidator(0)]
    # )

    longitude = models.CharField(u'经度', max_length=50, null=True, default='', blank=True)
    latitude = models.CharField(u'纬度', max_length=50, null=True, default='', blank=True)
    provinceKey = models.CharField(u'省份编码', max_length=50, null=True, default='')
    provinceName = models.CharField(u'省份', max_length=50, null=True, default='')
    cityKey = models.CharField(u'县市编码', max_length=50, null=True, default='')
    cityName = models.CharField(u'县市', max_length=50, null=True, default='')
    regionKey = models.CharField(u'区编码', max_length=50, null=True, default='')
    regionName = models.CharField(u'区', max_length=50, null=True, default='')
    # fullAddress = models.CharField(u'全部地址', max_length=200, null=True, default='', blank=True)
    addressDetail = models.CharField(u'地址详情', max_length=200, null=True, default='', blank=True)

    entry_date = models.DateTimeField(u'生成时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    shop = models.ForeignKey(WaShop, on_delete=models.CASCADE, verbose_name='所属商家')

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return str(self.provinceName) + str(self.cityName) + str(self.regionName) + str(self.addressDetail)
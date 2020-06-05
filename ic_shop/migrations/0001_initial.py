# Generated by Django 3.0 on 2020-03-06 19:26

import ckeditor_uploader.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ic_shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('sex', models.CharField(choices=[('未知', '未知'), ('男', '男'), ('女', '女')], default='未知', max_length=50, null=True, verbose_name='性别')),
                ('birthDate', models.DateField(blank=True, default='1970-01-01', null=True, verbose_name='出生日期')),
                ('nickname', models.CharField(default='', max_length=50, null=True, verbose_name='昵称')),
                ('city', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='城市')),
                ('province', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='省份')),
                ('country', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='国家')),
                ('mobile', models.CharField(error_messages={'unique': '该手机号已被注册.'}, help_text='手机账号', max_length=255, verbose_name='手机账号')),
                ('wx_openid', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='微信唯一标识符openId')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=ic_shop.models.Profile.get_avatar_path)),
                ('avatarUrl', models.CharField(blank=True, max_length=500, null=True, verbose_name='微信图像URL')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AreasInfo',
            fields=[
                ('id', models.CharField(default='0', max_length=50, primary_key=True, serialize=False, verbose_name='区域编号')),
                ('name', models.CharField(default='', max_length=50, null=True, verbose_name='区域名称')),
                ('areaLevel', models.CharField(default='', max_length=50, null=True, verbose_name='区域层级')),
                ('parent_id', models.CharField(default='', max_length=50, null=True, verbose_name='区域母编号')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='默认', error_messages={'unique': '该品牌已经存在'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=255, unique=True, verbose_name='标签名称')),
                ('status', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(0)], verbose_name='0- 未激活, 1 - 激活, 2- 过期')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('description', models.TextField(blank=True, default='', verbose_name='描述')),
            ],
            options={
                'verbose_name': '商品品牌',
                'verbose_name_plural': '商品品牌',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, unique=True, verbose_name='公司名称')),
                ('address', models.CharField(default='', max_length=100, null=True, verbose_name='公司地址')),
                ('mobile', models.CharField(default='', max_length=100, null=True, verbose_name='公司电话')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=ic_shop.models.Company.get_logo_path)),
                ('describe', models.CharField(default='', max_length=500, null=True, verbose_name='公司简介')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('offic_acc_url', models.CharField(default='', max_length=100, null=True, verbose_name='公众号URL')),
                ('offic_acc_contents', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='公众号内容')),
                ('ali_appId', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='支付宝-公司支付APPID')),
                ('ali_publicKey', models.TextField(blank=True, null=True, verbose_name='支付宝-支付宝公钥')),
                ('ali_privateKey', models.TextField(blank=True, null=True, verbose_name='支付宝-应用私钥')),
                ('ali_notifyUrl', models.CharField(blank=True, max_length=255, null=True, verbose_name='支付宝-支付通知url')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader', to=settings.AUTH_USER_MODEL, verbose_name='公司负责人')),
            ],
            options={
                'verbose_name': '公司',
                'verbose_name_plural': '公司',
            },
        ),
        migrations.CreateModel(
            name='CompanyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(0)], verbose_name=' 0：未知，1：加盟公司，2：总公司 ')),
                ('name', models.CharField(default='', max_length=20, null=True, verbose_name='类型名称')),
                ('describe', models.CharField(default='', max_length=200, null=True, verbose_name='类型描述')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '公司类型',
                'verbose_name_plural': '公司类型',
            },
        ),
        migrations.CreateModel(
            name='ItemOrder',
            fields=[
                ('orderNum', models.BigIntegerField(error_messages={'unique': '订单号重复'}, primary_key=True, serialize=False, verbose_name='订单号')),
                ('orderTitle', models.CharField(error_messages={'null': '需要提供商品名称或者相关标题'}, max_length=255, verbose_name='订单标题')),
                ('totalPrice', models.FloatField(error_messages={'null': '需要提供商品总价'}, verbose_name='总价')),
                ('orderAddress', models.CharField(default='', error_messages={'null': '订单快递位置'}, max_length=500, verbose_name='订单快递位置')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('update_timestamp', models.BigIntegerField(blank=True, null=True, verbose_name='操作时间戳')),
                ('company', models.ForeignKey(error_messages={'null': '需要提供公司ID'}, help_text='company_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.Company', verbose_name='所属公司')),
            ],
            options={
                'verbose_name': '商品订单',
                'verbose_name_plural': '商品订单',
            },
        ),
        migrations.CreateModel(
            name='ProfileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='补货员', max_length=20, verbose_name='用户类型')),
                ('description', models.CharField(default='', max_length=1024, verbose_name='描述')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '用户类型',
                'verbose_name_plural': '用户类型',
            },
        ),
        migrations.CreateModel(
            name='shopAdsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adsType', models.IntegerField(default=0, unique=True, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(0)], verbose_name='0- 图片, 1 - 视频, 2 - 商品分类, 3 - 商品,  4 - 其他（可以自定义）')),
                ('description', models.TextField(blank=True, default='', max_length=120, verbose_name='描述')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.Company', verbose_name='所属公司')),
            ],
            options={
                'verbose_name': '商家广告类型',
                'verbose_name_plural': '商家广告类型',
            },
        ),
        migrations.CreateModel(
            name='ShopItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='默认', error_messages={'unique': '该商品已经存在'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=255, unique=True, verbose_name='商品名称')),
                ('description', models.CharField(blank=True, max_length=1024, verbose_name='描述')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='商品内容')),
                ('price', models.FloatField(error_messages={'unique': '价格不能低于0'}, validators=[django.core.validators.MaxValueValidator(9999999), django.core.validators.MinValueValidator(0)], verbose_name='零售价格')),
                ('storage', models.IntegerField(error_messages={'unique': '当前存货不能低于'}, help_text='当前存货', validators=[django.core.validators.MaxValueValidator(99999), django.core.validators.MinValueValidator(0)], verbose_name='当前存货')),
                ('originalPrice', models.FloatField(help_text='出厂价格', null=True, validators=[django.core.validators.MaxValueValidator(9999999), django.core.validators.MinValueValidator(0)], verbose_name='出厂价格')),
                ('status', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(0)], verbose_name='-0- 未激活, 1 - 激活, 2 - 过期')),
                ('totalSell', models.IntegerField(blank=True, default=0, help_text='销量', null=True, validators=[django.core.validators.MaxValueValidator(9999999), django.core.validators.MinValueValidator(0)], verbose_name='销量')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('img', models.FileField(blank=True, null=True, upload_to=ic_shop.models.ShopItem.get_shopItem_path, verbose_name='图片')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.Brand', verbose_name='所属品牌')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
            },
        ),
        migrations.CreateModel(
            name='ShopItemCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagePriority', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(0)], verbose_name='0- 其他, 1 - 首页 (应用APP或小程序放置位置)')),
                ('img', models.FileField(blank=True, null=True, upload_to=ic_shop.models.ShopItemCategory.get_shopItemCategory_path, verbose_name='小图')),
                ('img_large', models.FileField(blank=True, null=True, upload_to=ic_shop.models.ShopItemCategory.get_shopItemCategory_path, verbose_name='大图')),
                ('name', models.CharField(default='', max_length=1024, null=True, verbose_name='商品种类名称')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.Company', verbose_name='所属公司')),
            ],
            options={
                'verbose_name': '商品种类',
                'verbose_name_plural': '商品种类',
            },
        ),
        migrations.CreateModel(
            name='shopType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=1024, null=True, verbose_name='商家型号名称')),
                ('description', models.TextField(blank=True, default='', verbose_name='描述')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '商家类型',
                'verbose_name_plural': '商家类型',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(error_messages={'unique': 'A title with that tag already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, verbose_name='标签名称')),
                ('description', models.TextField(blank=True, default='', verbose_name='描述')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='WaShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=1024, null=True, verbose_name='商家名称')),
                ('img', models.FileField(blank=True, null=True, upload_to=ic_shop.models.WaShop.get_shop_path)),
                ('description', models.TextField(blank=True, default='', max_length=1024, verbose_name='描述')),
                ('shopSn', models.CharField(error_messages={'unique': '商家SN已经存在'}, help_text='商家sn', max_length=50, unique=True, verbose_name='商家SN')),
                ('status', models.IntegerField(default=1, help_text='0：未激活状态，1：正常运作, 2：注销，', validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(0)], verbose_name='0：未激活状态，1：正常运作, 2：注销，')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.Company', verbose_name='所属公司')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='店长')),
            ],
            options={
                'verbose_name': '商家',
                'verbose_name_plural': '商家',
                'permissions': (('view_shop', 'View shop'),),
            },
        ),
        migrations.CreateModel(
            name='ItemOrderStatus',
            fields=[
                ('orderStatus', models.IntegerField(default=0, help_text='0- 等待支付中, 1 - 已支付, 2 - 已取消, 3 - 未付款交易超时关闭，或支付完成后全额退款, 4 - 退款中 5- 该订单未被扫描 6- 交易结束，不可退款  ', null=True, validators=[django.core.validators.MaxValueValidator(6), django.core.validators.MinValueValidator(0)], verbose_name='0- 等待支付中, 1 - 已支付, 2 - 已取消, 3 - 未付款交易超时关闭，或支付完成后全额退款, 4 - 退款中 5- 该订单未被扫描 6- 交易结束，不可退款  ')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('update_timestamp', models.BigIntegerField(null=True, verbose_name='操作时间戳')),
                ('buyer_user_id', models.CharField(blank=True, help_text='支付宝用户ID, 默认生成, 无需填写', max_length=255, null=True)),
                ('buyer_logon_id', models.CharField(blank=True, help_text='支付宝用户登录ID, 默认生成, 无需填写', max_length=255, null=True)),
                ('company_id', models.IntegerField(blank=True, help_text='公司ID', null=True)),
                ('orderNum', models.OneToOneField(default=1, error_messages={'null': '需要提供该订单的商品ID'}, help_text='itemOrder_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ic_shop.ItemOrder', verbose_name='所属订单')),
                ('orderCompleteStatus', models.IntegerField(default=0, help_text='0 - 未出货, 1 -已出货  2-部分出货', null=True, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(0)], verbose_name='0 - 未出货 1 - 已出货  2-部分出货')),
            ],
            options={
                'verbose_name': '订单状态',
                'verbose_name_plural': '订单状态',
            },
        ),
        migrations.CreateModel(
            name='shopLocation',
            fields=[
                ('longitude', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='经度')),
                ('latitude', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='纬度')),
                ('provinceKey', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='省份编码')),
                ('provinceName', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='省份')),
                ('cityKey', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='县市编码')),
                ('cityName', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='县市')),
                ('regionKey', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='区编码')),
                ('regionName', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='区')),
                ('addressDetail', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='地址详情')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ic_shop.WaShop', verbose_name='所属商家')),
            ],
            options={
                'verbose_name': '商家地址',
                'verbose_name_plural': '商家地址',
            },
        ),
        migrations.CreateModel(
            name='WaShopAds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.FileField(upload_to=ic_shop.models.WaShopAds.get_file_path, verbose_name='媒体文件')),
                ('title', models.CharField(default='', max_length=1024, null=True, verbose_name='标题')),
                ('description', models.TextField(blank=True, default='', max_length=1024, verbose_name='描述')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('category', models.ForeignKey(blank=True, db_column='category_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.ShopItemCategory', verbose_name='所属商品种类')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.Company', verbose_name='所属公司')),
                ('shopAdsType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.shopAdsType', verbose_name='广告类型')),
                ('shopItem', models.ForeignKey(blank=True, db_column='shopItem_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.ShopItem', verbose_name='所属商品')),
            ],
            options={
                'verbose_name': '商家广告',
                'verbose_name_plural': '商家广告',
            },
        ),
        migrations.AddField(
            model_name='washop',
            name='shopAds',
            field=models.ManyToManyField(blank=True, to='ic_shop.WaShopAds', verbose_name='广告'),
        ),
        migrations.AddField(
            model_name='washop',
            name='shopType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.shopType', verbose_name='所属商家类型'),
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(default='', max_length=50, null=True, verbose_name='省份')),
                ('city', models.CharField(default='', max_length=50, null=True, verbose_name='市')),
                ('district', models.CharField(default='', max_length=50, null=True, verbose_name='区')),
                ('cityCode', models.CharField(default='', max_length=50, null=True, verbose_name='区域码')),
                ('address', models.CharField(default='', max_length=50, null=True, verbose_name='地址详情')),
                ('mobile', models.CharField(default='', max_length=50, null=True, verbose_name='手机号码')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('user_id', models.ForeignKey(blank=True, db_column='user_id', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
            options={
                'verbose_name': '用户地址',
                'verbose_name_plural': '用户地址',
            },
        ),
        migrations.CreateModel(
            name='shopOperationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopSn', models.CharField(max_length=255, verbose_name='所属店家')),
                ('shopVerifyCode', models.CharField(default='', max_length=200, null=True, verbose_name='店家操作校验码')),
                ('codeUpdateTime', models.CharField(default='', max_length=200, null=True, verbose_name='验证码更新时间戳')),
                ('timeExpired', models.CharField(default='2', max_length=1024, null=True, verbose_name='检验码过期时间间隔')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '店家操作校验',
                'verbose_name_plural': '商品种类',
                'unique_together': {('shopSn', 'shopVerifyCode')},
            },
        ),
        migrations.CreateModel(
            name='shopLocationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='经度')),
                ('latitude', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='纬度')),
                ('provinceKey', models.CharField(default='', max_length=50, null=True, verbose_name='省份编码')),
                ('provinceName', models.CharField(default='', max_length=50, null=True, verbose_name='省份')),
                ('cityKey', models.CharField(default='', max_length=50, null=True, verbose_name='县市编码')),
                ('cityName', models.CharField(default='', max_length=50, null=True, verbose_name='县市')),
                ('regionKey', models.CharField(default='', max_length=50, null=True, verbose_name='区编码')),
                ('regionName', models.CharField(default='', max_length=50, null=True, verbose_name='区')),
                ('addressDetail', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='地址详情')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ic_shop.WaShop', verbose_name='所属商家')),
            ],
            options={
                'verbose_name': '商家历史地址',
                'verbose_name_plural': '商家历史地址',
            },
        ),
        migrations.AddField(
            model_name='shopitem',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.ShopItemCategory', verbose_name='商品种类'),
        ),
        migrations.AddField(
            model_name='shopitem',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ic_shop.WaShop', verbose_name='商家'),
        ),
        migrations.CreateModel(
            name='ProfileAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.FileField(upload_to='upload/avatar')),
                ('upload_time', models.DateTimeField(auto_now=True, null=True, verbose_name='上传时间')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '头像',
                'verbose_name_plural': '头像',
            },
        ),
        migrations.CreateModel(
            name='ItemOrderShopItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalBuy', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(999999), django.core.validators.MinValueValidator(0)], verbose_name='商品购买数量')),
                ('totalPrice', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(999999), django.core.validators.MinValueValidator(0)], verbose_name='总价')),
                ('price', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(999999), django.core.validators.MinValueValidator(0)], verbose_name='单价')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('itemOrder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='itemOrders', to='ic_shop.ItemOrder', verbose_name='所属订单')),
                ('shopItem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shopItems', to='ic_shop.ShopItem', verbose_name='商品')),
            ],
            options={
                'verbose_name': '商品订单详情列表',
                'verbose_name_plural': '商品订单详情列表',
            },
        ),
        migrations.AddField(
            model_name='itemorder',
            name='shop',
            field=models.ForeignKey(error_messages={'null': '需要提供所属商家ID'}, help_text='shop_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.WaShop', verbose_name='所属商家'),
        ),
        migrations.AddField(
            model_name='itemorder',
            name='shopItem',
            field=models.ManyToManyField(error_messages={'null': '需要提供该订单的商品ID'}, through='ic_shop.ItemOrderShopItems', to='ic_shop.ShopItem', verbose_name='所属商品'),
        ),
        migrations.AddField(
            model_name='itemorder',
            name='user',
            field=models.ForeignKey(blank=True, error_messages={'null': '需要提供购买用户ID'}, help_text='user_id', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户'),
        ),
        migrations.CreateModel(
            name='ImageUploader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.FileField(upload_to=ic_shop.models.ImageUploader.get_shopItem_path, verbose_name='图片')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('shopItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ic_shop.ShopItem')),
            ],
            options={
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ic_shop.CompanyType', verbose_name='公司类型'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=1024, null=True, verbose_name='标题')),
                ('description', models.CharField(blank=True, max_length=1024, verbose_name='描述')),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('shopItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ic_shop.ShopItem', verbose_name='所属商品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
            options={
                'verbose_name': '商品评论',
                'verbose_name_plural': '商品评论',
            },
        ),
        migrations.AddField(
            model_name='brand',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.Company', verbose_name='所属公司'),
        ),
        migrations.AddField(
            model_name='profile',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.Company', verbose_name='所属公司'),
        ),
        migrations.AddField(
            model_name='profile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='profile',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='上级用户'),
        ),
        migrations.AddField(
            model_name='profile',
            name='userType',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='ic_shop.ProfileType', verbose_name='用户类型'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]

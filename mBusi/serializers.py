from rest_framework import serializers
from ic_shop import models as model
from django.contrib.auth import get_user_model
from mBusi import settings as setting

from django.http import request

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, max_length=1024)
    password = serializers.CharField(required=False, max_length=1024)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'nickname')


class ProfileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.ProfileType
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(help_text='手机账户名', required=True)
    password = serializers.CharField(help_text='密码', required=True, write_only=True)
    sex = serializers.CharField(help_text='性别', allow_null=True, allow_blank=True, required=False)
    birthDate = serializers.CharField(help_text='出生日期', allow_null=True, allow_blank=True, required=False)
    avatar = serializers.FileField(help_text='头像', allow_null=True, required=False)
    nickname = serializers.CharField(help_text='头像', allow_null=True, allow_blank=True, required=False)
    mobile = serializers.CharField(help_text='手机号', allow_null=False, allow_blank=False, required=True,
                                   error_messages={
                                       'required': '需填写手机号'})
    company_id = serializers.CharField(help_text='公司名称', allow_null=True, allow_blank=True, required=False)
    wx_openid = serializers.CharField(help_text='微信open_id', required=True)

    class Meta:
        model = model.Profile
        fields = 'id', 'username', 'password', 'sex', 'birthDate', 'is_active', 'first_name', 'last_name', \
                 'email', 'nickname', 'mobile', 'avatar', 'last_login', 'company_id', 'wx_openid', 'city', 'avatarUrl', 'province',\
                 'country'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Tag
        fields = '__all__'


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.ProfileAvatar
        fields = '__all__'


class shopTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.shopType
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Brand
        fields = 'id', 'title', 'status', 'description'


class ShopItemCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = model.ShopItemCategory
        fields = '__all__'


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.UserAddress
        fields = '__all__'


class ShopItemSerializer(serializers.ModelSerializer):
    brand_id = serializers.CharField(help_text='brand_id', required=False)
    shop_id = serializers.CharField(help_text='shop_id', required=False)
    brandName = serializers.SerializerMethodField('get_shopItemBrand', read_only=True)
    categoryName = serializers.SerializerMethodField('get_shopItemCategory', read_only=True)
    file_prefix = serializers.SerializerMethodField('get_hostUrl', read_only=True)
    imgs = serializers.SerializerMethodField('get_shopItemImages', read_only=True)

    # tag_id = serializers.CharField(help_text='tag_id', required=False, read_only=True)
    # storage = ShopItemStorageSerializer(many=True, source='shopItems', required=False, read_only=True)
    # img = serializers.FileField(help_text='img file', required=False)

    class Meta:
        model = model.ShopItem
        fields = '__all__'

    def get_hostUrl(self, obj):
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri('/').strip('/')
        return ''

    def get_shopItemBrand(self, obj):
        try:
            shopItemBrand = model.Brand.objects.get(id=obj.brand_id)
            return shopItemBrand.title
        except model.ShopItem.DoesNotExist:
            return ''

    def get_shopItemCategory(self, obj):
        try:
            shopItemCategory = model.ShopItemCategory.objects.get(id=obj.category_id)
            return shopItemCategory.name
        except model.ShopItemCategory.DoesNotExist:
            return ''

    def get_shopItemImages(self, obj):
        try:
            shopItemImages = model.ImageUploader.objects.filter(shopItem_id=obj.id).order_by('-entry_date').values()
            request = self.context.get('request', None)
            file_prefix = ''
            if request is not None:
                file_prefix = request.build_absolute_uri('/').strip('/')

            if shopItemImages:
                arr_shopItem = []
                for item in shopItemImages:
                    item['img'] = file_prefix + '/media/' + item['img']
                    arr_shopItem.append(item)
                return arr_shopItem
        except model.ImageUploader.DoesNotExist:
            return []


class shopAdsTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = model.shopAdsType
        fields = '__all__'


class ImageUploaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.ImageUploader
        fields = '__all__'


#shop - WaShop
class WaShopSerializer(serializers.ModelSerializer):
    class Meta:
        # depth = 1
        model = model.WaShop
        fields = '__all__'

    name = serializers.CharField(help_text='name', required=True)
    description = serializers.CharField(help_text='description', required=False)
    updateVersion = serializers.FloatField(help_text='更新存货-版本号', required=False, default='1.0')
    status = serializers.CharField(required=True)

    republishStatus = serializers.CharField(help_text='商品补货状态码，0：无需补货，1：待补货，2：亟待补货', required=True, write_only=True)

    shopType_id = serializers.CharField(help_text='shopType_id', required=True, write_only=True)
    company_id = serializers.CharField(help_text='company_id', required=True, write_only=True)

    shopLocation = serializers.SerializerMethodField('Get_shopLocation', read_only=True)
    shopTypeName = serializers.SerializerMethodField('Get_shopTypeName', read_only=True)
    shopCompany = serializers.SerializerMethodField('Get_shopCompany', read_only=True)

    def Get_shopLocation(self, obj):
        try:
            shopLocation = list(model.shopLocation.objects.filter(shop=obj.id).values())
            # print(shopItem)
            if len(shopLocation) > 0:
                shopLocation[0]['fullAddress'] = shopLocation[0]['provinceName'] + shopLocation[0]['cityName'] \
                                             + shopLocation[0]['regionName'] + shopLocation[0]['addressDetail']

                return shopLocation[0]
        except model.shopLocation.DoesNotExist:
            return ''

    def Get_shopTypeName(self, obj):
        try:
            shopType = model.shopType.objects.get(id=obj.shopType_id)
            # print(shopItem)
            if shopType:
                return shopType.name
        except model.shopType.DoesNotExist:
            return ''

    def Get_shopCompany(self, obj):
        try:
            shopCompany = model.Company.objects.get(id=obj.company_id)
            # print(shopItem)
            if shopCompany:
                return shopCompany.name
        except model.Company.DoesNotExist:
            return ''


class shopOperationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.shopOperationCode
        fields = '__all__'


class shopLocationSerializer(serializers.ModelSerializer):
    shop = WaShopSerializer(read_only=True, required=False)
    fullAddress = serializers.SerializerMethodField('Get_shopFullAddress',required=False, read_only=True)

    class Meta:
        # depth = 1
        model = model.shopLocation
        fields = '__all__'

    def Get_shopFullAddress(self, obj):
        return obj.provinceName + obj.cityName + obj.regionName + obj.addressDetail


class WaShopAdsSerializer(serializers.ModelSerializer):
    category_id = serializers.CharField(help_text='category_id', required=True)
    shopItem_id = serializers.CharField(help_text='shopItem_id', required=True)
    shopAdsType = serializers.SerializerMethodField('Get_shopAdsType',required=False, read_only=True)

    def Get_shopAdsType(self, obj):
        try:
            shopAdsType = model.shopAdsType.objects.get(id=obj.shopAdsType_id)
            # print(shopItem)
            if shopAdsType:
                return shopAdsType.adsType
        except model.shopAdsType.DoesNotExist:
            return ''

    class Meta:
        model = model.WaShopAds
        fields = 'category_id', 'shopItem_id', 'img', 'title', 'description', 'shopAdsType', 'company',


class shopLocationHistorySerializer(serializers.ModelSerializer):
    # shop_id = serializers.CharField(help_text='shop_id', required=True)

    class Meta:
        model = model.shopLocationHistory
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.ImageUploader
        fields = '__all__'


class ItemOrderShopItemsSerializer(serializers.ModelSerializer):
    shopItem_id = serializers.CharField(help_text='shopItem_id', required=True)
    itemOrder_id = serializers.CharField(help_text='itemOrderNum', required=True)

    class Meta:
        model = model.ItemOrderShopItems
        fields = '__all__'


class ItemOrderSerializer(serializers.ModelSerializer):
    shop_id = serializers.CharField(help_text='shop_id', required=False)
    company_id = serializers.CharField(help_text='company_id', required=True)
    user_id = serializers.CharField(help_text='user_id', required=True)
    # retailPrice = serializers.CharField(help_text='零售价', required=True)
    orderTitle = serializers.CharField(help_text='商品名称', required=True)
    orderNum = serializers.CharField(help_text='商品订单号 - 无需填写，后台生成', required=False)
    update_timestamp = serializers.CharField(help_text='订单生成当前时间戳 - 无需填写，后台生成', required=False)
    orderStatus = serializers.CharField(help_text='订单状态', required=False, read_only=True)
    # totalCount = serializers.CharField(help_text='商品总数', required=True)
    totalPrice = serializers.CharField(help_text='totalPrice', required=True)
    orderAddress = serializers.CharField(help_text='orderAddress', required=True)
    entry_date = serializers.CharField(help_text='订单生成时间', required=False, read_only=True)

    itemOrderDetail = serializers.SerializerMethodField('Get_itemOrderStatus', read_only=True)
    shopItems = serializers.SerializerMethodField('Get_shopItems', read_only=True)
    address = serializers.SerializerMethodField('Get_address', required=False, read_only=True)

    class Meta:
        model = model.ItemOrder
        fields = 'orderTitle', 'orderAddress', 'totalPrice', 'shopItems', \
                 'shop_id', 'company_id', 'user_id', 'orderNum', 'update_timestamp', 'orderStatus', \
                 'itemOrderDetail', 'address', 'entry_date'

    # '0- 等待支付中, 1 - 已支付, 2 - 已取消, 3 - 未付款交易超时关闭，或支付完成后全额退款, 4 - 退款中 5- 该订单未被扫描 6- 交易结束，不可退款
    def Get_itemOrderStatus(self, obj):
        try:
            orderStatus = model.ItemOrderStatus.objects.get(orderNum_id=obj.orderNum)
            statusTitle = '等待付款'
            if orderStatus.orderStatus == 1:
                statusTitle = '已支付'
            if orderStatus.orderStatus == 2:
                statusTitle = '已取消'
            if orderStatus.orderStatus == 3:
                statusTitle = '已关闭'
            if orderStatus.orderStatus == 4:
                statusTitle = '退款中'
            if orderStatus.orderStatus == 5:
                statusTitle = '等待付款'

            return{
                'statusTitle': statusTitle,
                'status': orderStatus.orderStatus,
                'buyer_user_id': orderStatus.buyer_user_id,
                'buyer_logon_id': orderStatus.buyer_logon_id,
                'orderCompleteStatus': orderStatus.orderCompleteStatus,
            }
        except model.ItemOrderStatus.DoesNotExist:
            return {}

    def Get_shopItems(self, obj):
        try:
            itemOrderShopItems = list(model.ItemOrderShopItems.objects.filter(itemOrder__orderNum=obj.orderNum).values())
            arr_itemOrderShopItem = []
            request = self.context.get('request', None)
            prefix = ''
            if request is not None:
                prefix = request.build_absolute_uri('/').strip('/')

            for item in itemOrderShopItems:
                shopItem = model.ShopItem.objects.get(id=item['shopItem_id'])
                item['title'] = shopItem.title
                item['description'] = shopItem.description
                if shopItem.img:
                    item['img'] = prefix + shopItem.img.url
                else:
                    item['img'] = ''

                arr_itemOrderShopItem.append(item)
            return arr_itemOrderShopItem
        except model.ItemOrderShopItems.DoesNotExist:
            return []

    def Get_address(self, obj):
        try:
            user = model.Profile.objects.get(id=obj.user_id)
            return {
                "mobile": user.mobile,
                "name": user.nickname,
                "detail": obj.orderAddress
            }
        except model.Profile.DoesNotExist:
            return {}


class ItemOrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = model.ItemOrderStatus
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(help_text='user_id', required=True)
    shopItem_id = serializers.CharField(help_text='shopItem_id', required=True)

    class Meta:
        model = model.Comment
        fields = 'title', 'description', 'user_id', 'shopItem_id'


class CompanyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.CompanyType
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    type_id = serializers.CharField(help_text='type_id, 公司类型ID', required=True)
    leader_id = serializers.CharField(help_text='leader_id, 公司负责人ID', required=True)
    file_prefix = serializers.SerializerMethodField('Get_hostUrl', read_only=True)

    class Meta:
        model = model.Company
        fields = 'id', 'name', 'describe', 'address', 'leader_id', 'mobile', 'type_id', 'logo', 'file_prefix',\
                 'offic_acc_url', 'offic_acc_contents'

    def Get_hostUrl(self, obj):
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri('/').strip('/')
        return ''


class AreaInfoRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.AreasInfo
        fields = '__all__'

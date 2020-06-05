from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

from ic_shop.api.v1 import apiViews
from ic_shop.api.v1 import authentication as jwt_auth

from rest_framework_nested import routers
router = routers.DefaultRouter()

from django.conf.urls import url, include
# from rest_framework import routers
from .apiViews import *


"""
brand router
"""
router.register(r'brand', apiViews.BrandViewSet)
brand_shopItem_router = routers.NestedSimpleRouter(router, r'brand', lookup='brand')
brand_shopItem_router.register(r'shopItem', apiViews.ShopItemViewSet, basename='shopItem')


"""
shopItem router
"""
router.register(r'shopItem', apiViews.ShopItemViewSet)
# /shopItem/1/tag/
shopItem_tag_router = routers.NestedSimpleRouter(router, r'shopItem', lookup='shopItem')
shopItem_tag_router.register(r'tag', apiViews.TagViewSet, basename='tag')

# /shopItem/1/comment/
shopItem_comment_router = routers.NestedSimpleRouter(router, r'shopItem', lookup='shopItem')
shopItem_comment_router.register(r'comment', apiViews.CommentViewSet, basename='comment')

# /shopItem/1/itemOrder/
shopItem_itemOrder_router = routers.NestedSimpleRouter(router, r'shopItem', lookup='shopItem')
shopItem_itemOrder_router.register(r'itemOrder', apiViews.ItemOrderViewSet, basename='itemOrder')


"""
item order router
"""
router.register(r'itemOrder', apiViews.ItemOrderViewSet)


"""
tag router
"""
router.register(r'tag', apiViews.TagViewSet)
# /tag/1/shopItem/
tag_item_router = routers.NestedSimpleRouter(router, r'tag', lookup='tag')
tag_item_router.register(r'shopItem', apiViews.ShopItemViewSet, basename='shopItem')


"""
user router
"""
router.register(r'userType', apiViews.ProfileTypeViewSet)
router.register(r'user', apiViews.ProfileViewSet)


"""
user address
"""

user_address_router = routers.NestedSimpleRouter(router, r'user', lookup='user')
user_address_router.register(r'userAddress', apiViews.UserAddressViewSet, basename='userAddress')


"""
user  router
"""

user_shop_router = routers.NestedSimpleRouter(router, r'user', lookup='user')
user_shop_router.register(r'shop', apiViews.WaShopViewSet, basename='shop')


"""
user itemOrder router
"""

user_itemOrder_router = routers.NestedSimpleRouter(router, r'user', lookup='user')
user_itemOrder_router.register(r'itemOrder', apiViews.ItemOrderViewSet, basename='itemOrder')


"""
shopType -> shop router
"""
router.register(r'shopType', apiViews.shopTypeViewSet)
shopType_shop_router = routers.NestedSimpleRouter(router, r'shopType', lookup='shopType')
shopType_shop_router.register(r'shop', apiViews.WaShopViewSet, basename='shop')



"""
waShop shopItem router
"""
router.register(r'shop', apiViews.WaShopViewSet)
waShop_shopItem_router = routers.NestedSimpleRouter(router, r'shop', lookup='shop')
waShop_shopItem_router.register(r'shopItem', apiViews.ShopItemViewSet, basename='shopItem')


waShop_waShopAds_router = routers.NestedSimpleRouter(router, r'shop', lookup='shop')
waShop_waShopAds_router.register(r'shopAds', apiViews.WaShopAdsViewSet, basename='shopAds')


# """
# shop -> shop location router
# """
# shop_shopSlot_router = routers.NestedSimpleRouter(router, r'shop', lookup='shop')
# shop_shopSlot_router.register(r'shopSlot', apiViews.shopSlotViewSet, basename='shopSlot')
#

router.register(r'uploadAvatar', apiViews.ProfileAvatarViewSet)


"""
shop ads router
"""
router.register(r'shopAds', apiViews.WaShopAdsViewSet)


"""
comment router
"""
router.register(r'comment', apiViews.CommentViewSet)


"""
company router  company/user/     company/shop/
"""
router.register(r'company', apiViews.CompanyViewSet)
company_user_router = routers.NestedSimpleRouter(router, r'company', lookup='company')
company_user_router.register(r'user', apiViews.ProfileViewSet, basename='user')

company_shop_router = routers.NestedSimpleRouter(router, r'company', lookup='company')
company_shop_router.register(r'shop', apiViews.WaShopViewSet, basename='shop')

company_brand_router = routers.NestedSimpleRouter(router, r'company', lookup='company')
company_brand_router.register(r'brand', apiViews.BrandViewSet, basename='brand')

company_category_router = routers.NestedSimpleRouter(router, r'company', lookup='company')
company_category_router.register(r'shopItemCategory', apiViews.ShopItemCategoryViewSet, basename='shopItemCategory')


"""
location router
"""
router.register(r'location', apiViews.shopLocationViewSet)

"""
shop user router
"""
waShop_user_router = routers.NestedSimpleRouter(router, r'shop', lookup='shop')
waShop_user_router.register(r'user', apiViews.ProfileViewSet, basename='user')


"""
operation code
"""
router.register(r'shopOperationCode', apiViews.shopOperationCodeViewSet)


"""
shopItem category
"""
router.register(r'shopItemCategory', apiViews.ShopItemCategoryViewSet)
category_shopItem_router = routers.NestedSimpleRouter(router, r'shopItemCategory', lookup='shopItemCategory')
category_shopItem_router.register(r'shopItem', apiViews.ShopItemViewSet, basename='shopItem')


"""
item order status
"""
router.register(r'itemOrderStatus', apiViews.ItemOrderStatusViewSet)


"""
user address
"""
router.register(r'userAddress', apiViews.UserAddressViewSet)



urlpatterns = [
        url(r'^api/', include(router.urls)),
        url(r'^api/', include(tag_item_router.urls)),  # tag/1/article/
        url(r'^api/', include(shopType_shop_router.urls)),  # shopType/1/shop/
        url(r'^api/', include(shopItem_comment_router.urls)),  # shopItem/1/comment/
        url(r'^api/', include(shopItem_tag_router.urls)),  # shopItem/1/tag/
        url(r'^api/', include(shopItem_itemOrder_router.urls)),  # shopItem/1/itemOrder/
        url(r'^api/', include(shopItem_itemOrder_router.urls)),  # shopItem/1/itemOrder/
        url(r'^api/', include(waShop_shopItem_router.urls)),  # shop/1/shopItem/
        url(r'^api/', include(waShop_waShopAds_router.urls)),  # shop/1/shopAds/
        url(r'^api/', include(company_user_router.urls)),  # company/1/user/
        url(r'^api/', include(company_shop_router.urls)),  # company/1/shop/
        url(r'^api/', include(user_shop_router.urls)),  # user/1/shop/
        url(r'^api/', include(waShop_user_router.urls)),  # shop/1/user/
        url(r'^api/', include(company_brand_router.urls)),  # company/1/brand/
        url(r'^api/', include(company_category_router.urls)),  # company/1/shopItemCategory/
        url(r'^api/', include(user_itemOrder_router.urls)),  # user/1/itemOrder/
        url(r'^api/', include(category_shopItem_router.urls)),  # shopItemCategory/1/shopItem/
        url(r'^api/', include(brand_shopItem_router.urls)),  # brand/1/shopItem/
        url(r'^api/', include(user_address_router.urls)),  # user/1/userAddress/


        # customize api
        url(r'^api/itemOrderRefund/', apiViews.itemOrderRefund),
        url(r'^api/systemTime/', apiViews.systemTime),
        url(r'^api/weather/', apiViews.weather),
        url(r'^api/mobileVerifyCode/', apiViews.mobileVerifyCode),
        url(r'^api/requestWeixinOpenId/', apiViews.requestWeixinOpenId),
        url(r'^api/allCities/', apiViews.allCities),

        url(r'^api/login/', LoginViewSet.as_view()),
        # url(r'^api/login/', jwt_auth.obtain_jwt_token),
        url(r'^api/refresh/', jwt_auth.refresh_jwt_token),
        url(r'^api/verify/', jwt_auth.verify_jwt_token),

        url(r'^doc/', include_docs_urls(title='mBusi API', permission_classes=[])),

        url('ckeditor/', include('ckeditor_uploader.urls')),
]

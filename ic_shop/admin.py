# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ic_shop import models as model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin
from django.apps import AppConfig

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django import forms

from django.contrib.admin import AdminSite



# Register your models here.


""" 
  customise admin UI allows one to edit at parent model page, inline - > model,  admin -> model Admin
"""


def admin_pages_size():
    return 15


""" 
    inline 
"""


class shopInline(admin.TabularInline):
    model = model.WaShop
    show_change_link = False


class shopAdsTypeInline(admin.TabularInline):
    model = model.shopAdsType


class shopAdsInline(admin.TabularInline):
    model = model.WaShop.shopAds.through


class ItemOrderShopItemsInline(admin.TabularInline):
    model = model.ItemOrder.shopItem.through


class ImageInline(admin.TabularInline):
    model = model.ImageUploader


class CommentInline(admin.TabularInline):
    model = model.Comment

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(CommentInline, self).get_readonly_fields(request, obj)
        else:
            return 'user',


class LocationInline(admin.TabularInline):
    extra = 1
    model = model.shopLocation
    list_per_page = admin_pages_size()


class ShopItemCategoryInline(admin.TabularInline):
    model = model.ShopItemCategory


class ItemOrderStatusInline(admin.StackedInline):
    show_change_link = True
    model = model.ItemOrderStatus


""" 
    admin 
"""


class WaShopAdmin(admin.ModelAdmin):
    def get_form(self, request, *args, **kwargs):
        form = super(WaShopAdmin, self).get_form(request, *args, **kwargs)
        if not request.user.is_superuser:
            choices = []
            user = model.Profile.objects.get(company=request.user.company_id)
            choices.append((user.id, user.username))
            form.base_fields['owner'].choices = choices
        form.request = request
        return form

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.company != request.user.company:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.company != request.user.company:
            return False
        return True

    def get_queryset(self, request):
        qs = super(WaShopAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company=request.user.company)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(WaShopAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'company', 'shopType',

    ordering = ('id',)
    list_display = ('id', 'name', 'company', 'owner')
    list_display_links = ('name',)
    # search_fields = ['id', 'name', 'company']
    list_filter = ('entry_date', 'update_time',)
    # search_fields = ('company', 'location', )
    filter_horizontal = ('shopAds',)
    inlines = (LocationInline, )
    list_per_page = admin_pages_size()


class ShopItemImageAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if not request.user.is_superuser:
            return False


class CommentAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if not request.user.is_superuser:
            return False

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(CommentAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'user',


class UsershopAdmin(admin.ModelAdmin):
    list_per_page = admin_pages_size()


class ShopItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'pagePriority', )
    list_display_links = ('name',)

    def get_queryset(self, request):
        qs = super(ShopItemCategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company=request.user.company)

    def get_form(self, request, *args, **kwargs):
        form = super(ShopItemCategoryAdmin, self).get_form(request, *args, **kwargs)
        if not request.user.is_superuser:
            choices = []
            company = model.Company.objects.get(id=request.user.company_id)
            choices.append((company.id, company.name))
            form.base_fields['company'].choices = choices
        form.request = request
        return form


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', )
    list_display_links = ('title',)

    def get_queryset(self, request):
        qs = super(BrandAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company=request.user.company)

    def get_form(self, request, *args, **kwargs):
        form = super(BrandAdmin, self).get_form(request, *args, **kwargs)
        if not request.user.is_superuser:
            choices = []
            company = model.Company.objects.get(id=request.user.company_id)
            choices.append((company.id, company.name))
            form.base_fields['company'].choices = choices
        form.request = request
        return form


class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ('orderNum', 'orderTitle', 'shop', 'company', 'entry_date', 'totalPrice', 'status', 'completeStatus')
    inlines = (ItemOrderShopItemsInline, ItemOrderStatusInline, )
    list_filter = ('entry_date', 'shopItem', 'shop', 'company')
    list_per_page = admin_pages_size()

    class Media:
        js = ("refresh.js",)

    def get_queryset(self, request):
        qs = super(ItemOrderAdmin, self).get_queryset(request).order_by('-entry_date')
        if request.user.is_superuser:
            return qs
        return qs.filter(company=request.user.company).order_by('-entry_date')

    def status(self, obj):
        return obj.itemorderstatus.orderStatus

    def completeStatus(self, obj):
        return obj.itemorderstatus.orderCompleteStatus

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ItemOrderAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'company', 'user', 'shop', 'shopItem', 'orderNum',

# class ShopItemshopForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(ShopItemshopForm, self).__init__(*args, **kwargs)
#         if self.instance:
#             try:
#                 shop = model.shop.objects.all()
#                 # wtf = model.Profile.objects.filter(company_id=shop.company_id)
#                 w = self.fields['shop'].widget
#                 choices = []
#                 for choice in shop:
#                     choices.append((choice.id, choice.name))
#                 w.choices = choices
#             except model.shop.DoesNotExist:
#                 return


class ShopItemAdmin(admin.ModelAdmin):
    def get_form(self, request, *args, **kwargs):
        form = super(ShopItemAdmin, self).get_form(request, *args, **kwargs)
        if not request.user.is_superuser:
            choices = []
            brand_choices = []
            category_choices = []

            shop = model.WaShop.objects.filter(company=request.user.company_id)
            if shop:
                for item in shop:
                    choices.append((item.id, item.name))
            form.base_fields['shop'].choices = choices

            category = model.ShopItemCategory.shop.filter(company=request.user.company_id)
            if category:
                for item in category:
                    category_choices.append((item.id, item.name))
            form.base_fields['category'].choices = category_choices

            brand = model.Brand.objects.filter(company=request.user.company_id)
            if brand:
                for item in brand:
                    brand_choices.append((item.id, item.title))
            form.base_fields['brand'].choices = brand_choices
        form.request = request
        return form

    # def get_readonly_fields(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return super(ShopItemAdmin, self).get_readonly_fields(request, obj)
    #     else:
    #         return 'shop',

    def get_queryset(self, request):
        qs = super(ShopItemAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        company = model.Company.objects.get(id=request.user.company_id)
        arr_shop_ids = []
        shop = model.WaShop.objects.filter(company_id=company.id).values()
        if shop:
            for item in shop:
                arr_shop_ids.append(item['id'])
        return qs.filter(shop__in=arr_shop_ids)

    list_display = ('id', 'title', 'brand', 'category', 'price', 'totalSell',
                    'originalPrice', 'storage', 'image_tag', 'status', 'entry_date', 'shop',)
    list_display_links = ('title',)
    # raw_id_fields = ("shopSlot",)
    list_filter = ('brand', 'category', 'totalSell', 'price', 'status', 'entry_date', 'update_time')
    inlines = (ImageInline, CommentInline)
    save_as = True
    ordering = ('id',)
    list_per_page = admin_pages_size()


class shopAdsTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'company', 'adsType')
    list_display_links = ('description',)

    def get_queryset(self, request):
        qs = super(shopAdsTypeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company_id=request.user.company_id)

    def get_form(self, request, *args, **kwargs):
        form = super(shopAdsTypeAdmin, self).get_form(request, *args, **kwargs)
        if not request.user.is_superuser:
            choices = []
            company = model.Company.objects.get(id=request.user.company_id)
            choices.append((company.id, company.name))
            form.base_fields['company'].choices = choices
        form.request = request
        return form


class WaShopAdsAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(WaShopAdsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company_id=request.user.company_id)

    def get_form(self, request, *args, **kwargs):
        form = super(WaShopAdsAdmin, self).get_form(request, *args, **kwargs)
        if not request.user.is_superuser:
            choices = []
            company = model.Company.objects.get(id=request.user.company_id)
            choices.append((company.id, company.name))
            form.base_fields['company'].choices = choices
        form.request = request
        return form

    list_display_links = ('title',)
    list_display = ('id', 'title', 'description', 'image_tag', 'shopItem', 'category', 'entry_date')



class GroupAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(GroupAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'groups',

    list_per_page = admin_pages_size()


class CompanyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(CompanyAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'leader', 'type',

    def get_queryset(self, request):
        qs = super(CompanyAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.company_id)

    list_per_page = admin_pages_size()


class ProfileAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'sex', 'birthDate', 'is_staff', 'userType', )

    def has_change_permission(self, request, obj=None):
        # if request.user.is_superuser:
        #     return True
        # if obj is not None and obj != request.user:
        #     return False
        return True

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return 'is_staff',

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ProfileAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'username', 'is_superuser', 'user_permissions', 'is_active', 'company', 'groups',

    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company_id=request.user.company_id)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'sex', 'birthDate', 'nickname', 'mobile', 'avatar',
                                      'last_login', 'company')}),
        ('权限', {'fields': ('groups', 'user_permissions', 'is_active', 'is_superuser', 'is_staff',)}),
    )
    list_filter = ('company', 'is_active', 'is_superuser', 'is_staff', 'sex')

    pass

ProfileAdmin.list_display += ('company',)


admin.site.register(model.ProfileType)
admin.site.register(model.Profile, ProfileAdmin)
admin.site.register(model.Brand, BrandAdmin)
admin.site.register(model.ShopItem, ShopItemAdmin)
admin.site.register(model.ItemOrder, ItemOrderAdmin)
admin.site.register(model.Tag)
admin.site.register(model.Comment, CommentAdmin)
admin.site.register(model.ImageUploader, ShopItemImageAdmin)
admin.site.register(model.shopType)
admin.site.register(model.WaShop, WaShopAdmin)
admin.site.register(model.WaShopAds, WaShopAdsAdmin)
admin.site.register(model.Company, CompanyAdmin)
admin.site.register(model.CompanyType)
admin.site.register(model.shopLocation)
admin.site.register(model.shopAdsType, shopAdsTypeAdmin)
admin.site.register(model.ShopItemCategory, ShopItemCategoryAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)


admin.site.site_url = '/'
admin.site.site_header = '微商城后台管理系统'
admin.site.site_title = '微商城系统'
# admin.site.site_index_title = '冰糕机系统'
admin.site.name = '微商城系统'

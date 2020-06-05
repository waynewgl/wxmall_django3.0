# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render


from rest_framework.permissions import IsAuthenticated
from mBusi import serializers as ic_serializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_extensions.bulk_operations.mixins import ListDestroyModelMixin
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.settings import api_settings

#coding:utf-8
from rest_framework import generics, viewsets, mixins, status
from rest_framework.response import Response
from mBusi.serializers import *
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
# from datetime import datetime
from rest_framework.decorators import api_view

from django.http import Http404
from django.db.models import Sum, Count

from django.conf import settings

import calendar, time, datetime

from ic_shop.api.v1.payment import alipay as alipay

import logging
logger = logging.getLogger("django")  # 为loggers中定义的名称


import urllib.request as ur
import urllib.parse
import hashlib
import json
import random
import re, json

from dysms_python import demo_sms_send as sms

from django.core.cache import cache

import ssl, os

ssl._create_default_https_context = ssl._create_unverified_context


alipaySecrectKey = 76


#
@api_view(['GET', 'POST' ])
def alipayCallback(request):
    # new_article = model.ShopItem.objects.filter(id=1)
    # if not new_article:
    #     return render(request, 'home.html')

    # t = time.time()
    #
    # print(t)  # 原始时间数据
    # print(int(t))  # 秒级时间戳
    # print(int(round(t * 1000)))  # 毫秒级时间戳
    # # logger.info("some info...", new_article[0].title)

    company = model.Company.objects.get(id=4)

    # print(company.ali_publicKey.url)
    # my_file = open(data.ali_publicKey.url, 'r')
    # txt = my_file.read()
    # print(txt)
    t = time.time()
    payUrl = alipay.preCreateOrder(company.ali_appId, company.ali_publicKey, company.ali_privateKey, company.ali_notifyUrl,  '冰淇淋12356', alipaySecrectKey*int(round(t * 1000)), 0.01)

    return render(request, 'home.html', {'info_dict': {
        'paymentCodeUrl': payUrl,
        'request': request
    }})


def add(request, a, b):

    c = int(a) + int(b)
    return HttpResponse(str(c))


def generate_verification_code():
    ''' 随机生成6位的验证码 '''
    code_list = []
    # for i in range(6):
    #     alpha = chr(random.randint(65, 90))  # random.randrange(65,91)
    #     alpha_lower = chr(random.randint(97, 122))  # random.randrange(65.91)
    #     num = str(random.randint(0, 9))
    #     ret = random.choice([alpha, num, alpha_lower])
    #     code_list.append(ret)

    for i in range(6):
        rand_num = random.randint(0, 9)
        code_list.append(str(rand_num))

    verification_code = ''.join(code_list)

    return verification_code


def phoneFormat(n):
    if len(n) < 11:
        return False

    MOBILE = "^1(3[0-9]|4[57]|5[0-35-9]|7[01678]|8[0-9])\\d{8}$"
    CM = "^1(3[4-9]|4[7]|5[0-27-9]|7[0]|7[8]|8[2-478])\\d{8}$"
    CU = "^1(3[0-2]|4[5]|5[56]|709|7[1]|7[6]|8[56])\\d{8}$"
    CT = "^1(3[34]|53|77|700|8[019])\\d{8}$"

    if re.match(MOBILE, n) or re.match(CM, n) or re.match(CU, n) or re.match(CT, n):
        return True
    else:
        return False


def index(request):
    # result = sms.send_sms(12, 19959235319, '冰糕机后台管理系统', 'SMS_141580741', {'code': 'xs_max'})
    # logger.info('result sms %s', result)
    # company = model.Company.objects.get(id=4)
    return render(request, 'home.html')


# set false to disable auth token
def allow_auth():
    return False


def error_msg(msg, code):
    return {
        "msg": msg
    }


# API VIEW


#获取手机验证码
@api_view(['POST', ])
def mobileVerifyCode(request, format=None):
    logger.info('code %s ', request.data.get('mobile'))
    if not request.data.get('mobile', None):
        return Response({
            'msg': '请输入手机号 - mobile'
        }, status.HTTP_400_BAD_REQUEST)

    if not phoneFormat(request.data.get('mobile')):
        return Response({
            'msg': '手机格式不正确'
        }, status.HTTP_400_BAD_REQUEST)

    verifyCode = generate_verification_code()
    result = sms.send_sms(request.data.get('mobile', None),  request.data.get('mobile', None), '冰糕机后台管理系统', 'SMS_141580741',
                          {'code': verifyCode})
    result = json.loads(result)
    if result.get('Code') == "isv.MOBILE_NUMBER_ILLEGAL":
        return Response({
            'msg': '手机格式不正确'
        }, status.HTTP_400_BAD_REQUEST)

    cache.set(str(request.data.get('mobile')), verifyCode, timeout=300)  # 保存手机验证码5分钟
    logger.info('save code %s', cache.get(str(request.data.get('mobile'))))
    return Response({
        'msg': 'success',
    }, status.HTTP_200_OK)


#获取微信小程序用户唯一openid
# https://api.weixin.qq.com/sns/jscode2session?appid=wxe48e8968678b3d20&secret=5b3b9a5548c0a293e1457a12519a4e2f&js_code=012L63K3106ysN1FAsL311vNJ31L63Ky&grant_type=authorization_code
@api_view(['GET', ])
def requestWeixinOpenId(request, format=None):
    appCode = request.query_params.get('appCode')
    appId = request.query_params.get('appId')
    appSecret = request.query_params.get('appSecret')

    if not appCode or not appId or not appSecret:
        return Response({
            'msg': '需提供code, appId, appSecret'
        }, status.HTTP_400_BAD_REQUEST)

    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appId + '&secret=' + appSecret \
          + '&js_code=' + appCode + '&grant_type=authorization_code'

    try:
        with ur.urlopen(url) as f:
            data = f.read()
            data_json = json.loads(data.decode('utf-8'))

            if data_json.get('errcode') == 40013:
                return Response('appid无效', status.HTTP_400_BAD_REQUEST)

            if data_json.get('errcode') == 40163:
                return Response('code已经失效', status.HTTP_400_BAD_REQUEST)

            if data_json.get('errcode') == 40125:
                return Response('secret已经失效', status.HTTP_400_BAD_REQUEST)

            return Response({
                'msg': 'success',
                'open_id': data_json.get('openid'),
                'session_key': data_json.get('session_key'),
            }, status.HTTP_200_OK)
    except urllib.request.HTTPError:
        return Response('not found', status.HTTP_204_NO_CONTENT)


#获取天气
@api_view(['GET', ])
def weather(request, format=None):
    """
    \n
    get: \n
        e.g. \n
            ...v1/api/weather/?cityName=fuzhou  \n
        result:\n
    """

    cityName = request.query_params.get('cityName')

    if not cityName:
        return Response(error_msg('cityName must be provided', status.HTTP_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST)

    if cache.get(cityName) is not None:
        return Response(cache.get(cityName), status.HTTP_200_OK)

    url = 'http://api.seniverse.com/v3/weather/now.json?key=siwdjgwcpypfoqiv&location=' + cityName + '&language=zh-Hans&unit=c'
    encodedStr = urllib.parse.quote(url, safe="/:=&?#+!$,;'@()*[]")
    try:
        with ur.urlopen(encodedStr) as f:
            data = f.read()
            data_json = json.loads(data.decode('utf-8'))
            if data_json.get('status_code') == 'AP010010':
                return Response(error_msg('no found', status.HTTP_204_NO_CONTENT), status.HTTP_204_NO_CONTENT)

            if data_json.get('results'):
                result = {}
                data = data_json.get('results')[0]
                result['city'] = data.get('location').get('name')
                result['path'] = data.get('location').get('path')
                result['timezone'] = data.get('location').get('timezone')
                result['timezone_offset'] = data.get('location').get('timezone_offset')
                result['temperature'] = data.get('now').get('temperature')
                result['description'] = data.get('now').get('text')
                result['last_update'] = data.get('last_update')

                cache.set(result['city'], result, timeout=60*30)

                # date = datetime.datetime.strptime(result['last_update'], "%Y-%m-%dT%H:%M:%S+08:00")
                # timeInterval = time.mktime(date.timetuple())
                # timeInterval = int(round(timeInterval * 1000))
                return Response(result, status.HTTP_200_OK)

            return Response(error_msg('not found', status.HTTP_204_NO_CONTENT), status.HTTP_204_NO_CONTENT)
    except urllib.request.HTTPError:
        return Response(error_msg('not found', status.HTTP_204_NO_CONTENT), status.HTTP_204_NO_CONTENT)


@api_view(['GET', ])
def systemTime(request, format=None):
    t = time.time()
    return Response({
        'date': datetime.datetime.now(),
        'time': int(round(t * 1000))
    }, status.HTTP_200_OK)


@api_view(['GET', ])
def allCities(request, format=None):
    json_path = os.path.join(settings.MEDIA_ROOT, "", "", "getAllRegion.json")
    return HttpResponse(open(json_path, 'r'), content_type='application/json; charset=utf8')


class LoginViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = User.objects.get(username__iexact=username)

            if user.check_password(password):
                # logger.info("user = %s", username)
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                # logger.info('token:', token)
                response_data = {
                    'id': user.id,
                    'username': user.username,
                    'token': token
                }
                return Response(response_data)

            return Response(error_msg('密码错误', status.HTTP_400_BAD_REQUEST), status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(error_msg('用户不存在', status.HTTP_400_BAD_REQUEST), status=status.HTTP_400_BAD_REQUEST)


class ProfileAvatarViewSet(viewsets.ModelViewSet):
    """ 
        Profile avatar 
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (IsAuthenticated,)

    queryset = model.ProfileAvatar.objects.all()
    # queryset.query.set_limits(0, 5)
    serializer_class = ic_serializer.ProfileAvatarSerializer


class ProfileTypeViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """ 
       Profile Type Tag
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication, )
        permission_classes = (IsAuthenticated,)

    queryset = model.ProfileType.objects.all()
    # queryset.query.set_limits(0, 5)
    serializer_class = ic_serializer.ProfileTypeSerializer


# inherits abstractUser
class ProfileViewSet(viewsets.ModelViewSet):
        """ 
         User profile, include auth user Model
        """
        # if allow_auth():
        #     authentication_classes = (JSONWebTokenAuthentication,)
        #     permission_classes = (IsAuthenticated,)

        queryset = model.Profile.objects.all()
        serializer_class = ic_serializer.ProfileSerializer

        def list(self, request, *args, **kwargs):
            wx_openid = request.query_params.get('openId')
            if wx_openid:
                try:
                    user = model.Profile.objects.get(wx_openid=wx_openid)
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    # print(user)
                    return Response({
                        "nickname": user.nickname,
                        "avatarUrl": user.avatarUrl,
                        "sex": user.sex,
                        "country": user.country,
                        "city": user.city,
                        "province": user.province,
                        "company_id":user.company_id,
                        "wx_openid": user.wx_openid,
                        "id": user.id,
                        "token": token
                    }, status=status.HTTP_200_OK)
                except model.Profile.DoesNotExist:
                    return Response(error_msg('用户不存在', status.HTTP_204_NO_CONTENT), status=status.HTTP_204_NO_CONTENT)

            return super(ProfileViewSet, self).list(self, request, *args, **kwargs)

        def get_queryset(self):
            shop_pk = self.kwargs.get('shop_pk', None)
            logger.info('getting request  user  %s ', self.kwargs)

            if shop_pk:
                # logger.info('getting request shop user  %s ', shop_pk)
                return model.Profile.objects.filter(shop=shop_pk).order_by('id')

            company_pk = self.kwargs.get('company_pk', None)
            if company_pk:
                return model.Profile.objects.filter(company=company_pk).order_by('id')

            return super(ProfileViewSet, self).get_queryset().order_by('id')

        def create(self, request, *args, **kwargs):
            logger.info('getting request data create user %s', request.data.copy())

            try:
                username = request.data["username"]
            except KeyError:
                username = ""

            try:
                password = request.data["password"]
            except KeyError:
                password = ""

            try:
                mobile = request.data["mobile"]
            except KeyError:
                mobile = ""

            if not phoneFormat(mobile):
                return Response({
                    'msg': '手机格式不正确'
                }, status.HTTP_400_BAD_REQUEST)

            try:
                verifyCode = request.data["verifyCode"]
            except KeyError:
                verifyCode = ""

            try:
                wx_openid = request.data["wx_openid"]
            except KeyError:
                wx_openid = ""

            if not request.data or username == "" or password == "" or mobile == "" or wx_openid == "":
                return Response({
                    "msg": '需提供用户相关信息'
                }, status=status.HTTP_400_BAD_REQUEST)

            if model.Profile.objects.filter(wx_openid=wx_openid):
                return Response({
                    "msg": '用户已经存在'
                }, status=status.HTTP_400_BAD_REQUEST)

            if model.Profile.objects.filter(username=request.data.get("username")):
                return Response({
                    "msg": '用户已经存在'
                }, status=status.HTTP_400_BAD_REQUEST)

            if model.Profile.objects.filter(mobile=request.data.get("mobile")):
                return Response({
                    "msg": '该手机号已经存在'
                }, status=status.HTTP_400_BAD_REQUEST)

            if verifyCode == "":
                return Response({
                    "msg": '需要提供验证码'
                }, status=status.HTTP_400_BAD_REQUEST)

            verifyCode_cached = cache.get(str(mobile))
            logger.info('  %s  --- %s - get code %s ', '',  cache.get(request.data.get("mobile")),  verifyCode_cached)
            if not verifyCode_cached:
                return Response({
                    "msg": '验证码不存在'
                }, status=status.HTTP_400_BAD_REQUEST)

            if str(verifyCode_cached) != str(verifyCode): #校验手机匹配的验证码
                return Response({
                    "msg": '验证码不正确'
                }, status=status.HTTP_400_BAD_REQUEST)

            return super(ProfileViewSet, self).create(request, *args, **kwargs)

        def partial_update(self, request, *args, **kwargs):
            # print('profile data %s', request.data.copy())

            return super(ProfileViewSet, self).partial_update(request, *args, **kwargs)


class shopOperationCodeViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """ 
       shop operation code
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication, )
        permission_classes = (IsAuthenticated,)

    queryset = model.shopOperationCode.objects.all()
    serializer_class = ic_serializer.shopOperationCodeSerializer

    def list(self, request, *args, **kwargs):
        """ 
             list:

                {\n
                     get shopOperationCode by sn \n
                     e.g: \n
                         .../api/shopOperationCode/?sn=SN-400788776655
                 }
         """

        shopSn = request.query_params.get('sn')
        try:
            operationCode = list(model.shopOperationCode.objects.filter(shopSn=shopSn).values())

            if len(operationCode) > 0:
                t = time.time()
                operationCode[0]['systemTime'] = int(round(t * 1000))
                return Response(operationCode[0], status=status.HTTP_200_OK)
            return Response(error_msg('no found', status.HTTP_204_NO_CONTENT), status=status.HTTP_400_BAD_REQUEST)
        except model.shopOperationCode.DoesNotExist:
            return Response(error_msg('no found', status.HTTP_204_NO_CONTENT), status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        shop_code_data = request.data.copy()

        # /book/1/chapter/
        # if self.kwargs.get('book_pk', None):
        #     chapter_data['book_id'] = self.kwargs.get('book_pk', None)
        #     if not Book.objects.filter(id=se.get('book_pk', None)):
        #         return Response('book.py not found', status=status.HTTP_404_NOT_FOUND)lf.kwargs

        logger.info('getting request data create category %s', shop_code_data)
        t = time.time()
        # t_encode = uuid.uuid4() + t
        t_sn = str(shop_code_data.get('shopSn')) + str(t)
        t_encode = t_sn.encode("utf8")

        hash = hashlib.md5(t_encode).hexdigest().upper()

        try:
            operationCode = model.shopOperationCode.objects.get(shopSn=shop_code_data.get('shopSn'))
            operationCode.shopVerifyCode = hash
            operationCode.codeUpdateTime = str(int(round(t * 1000)))
            operationCode.save()
            return Response({
                'code': hash,
                'updateTime': operationCode.codeUpdateTime
            }, status=status.HTTP_200_OK)

        except model.shopOperationCode.DoesNotExist:
            operationCode = model.shopOperationCode.objects.create(shopSn=shop_code_data.get('shopSn'),
                                                                     shopVerifyCode=hash,
                                                                     codeUpdateTime=str(int(round(t * 1000)))
                                                                     )
            return Response({
                'code': hash,
                'updateTime': operationCode.codeUpdateTime
            }, status=status.HTTP_201_CREATED)


class shopTypeViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """
        shop type
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (IsAuthenticated,)

    queryset = model.shopType.objects.all()
    serializer_class = ic_serializer.shopTypeSerializer

    def get_queryset(self):
        logger.info('getting request data shop type %s ', self.kwargs)
        # book_id = self.kwargs.get('book_pk', None)
        # if book_id:
        #     return Category.objects.filter(book=book_id).order_by('id')
        return super(shopTypeViewSet, self).get_queryset().order_by('id')

    def create(self, request, *args, **kwargs):
        shop_type_data = request.data.copy()

        # /book/1/chapter/
        # if self.kwargs.get('book_pk', None):
        #     chapter_data['book_id'] = self.kwargs.get('book_pk', None)
        #     if not Book.objects.filter(id=se.get('book_pk', None)):
        #         return Response('book.py not found', status=status.HTTP_404_NOT_FOUND)lf.kwargs

        logger.info('getting request data create category %s', shop_type_data)
        serializer = ic_serializer.shopTypeSerializer(data=shop_type_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        error_msg = {
            'code': status.HTTP_400_BAD_REQUEST,
            'msg': serializer.errors
        }

        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """ 
            e.g. 
            {\n
                delete bulk of child resources, add header: X-BULK-OPERATION : true \n
                # Request \n
                DELETE ../shopType/1/shop/ HTTP/1.1 \n
                Accept: application/json  \n
                X-BULK-OPERATION: true \n
            }
        """
        return super(shopTypeViewSet, self).destroy(request, *args, **kwargs)


class WaShopViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """ 
         list:
             {\n
                 list all shops by cityKey \n
                 e.g: \n
                     .../api/shop/?cityKey=350010
             }\n
             
             {\n
                 list all shops by status \n
                 0：未激活状态，1：正常运作，2、用户购买中，3、补货中，4：离线状态，5：报废，
                 
                 or faultStatus（如果查询多个，传array）,  temperatureStatus,  republishStatus
                 e.g: \n
                     .../api/shop/?status=7
             }\n
             
            {\n
                 list all shops by sn \n
                 e.g: \n
                     .../api/shop/?sn=SN-400788776655
             }
     """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (IsAuthenticated,)

    queryset = model.WaShop.objects.all()
    serializer_class = ic_serializer.WaShopSerializer

    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk', None)
        if user_pk:
            logger.info('getting request user shop  %s ', user_pk)
            status = self.request.query_params.get('status')
            if status:
                # logger.info('getting request data shop status %s ', self.kwargs)
                result = model.WaShop.objects.filter(owner=user_pk, status=status).order_by('id')
                return result

            return model.WaShop.objects.filter(owner=user_pk).order_by('id')

        company_pk = self.kwargs.get('company_pk', None)
        if company_pk:
            return model.WaShop.objects.filter(company=company_pk).order_by('-entry_date')

        cityKey = self.request.query_params.get('cityKey')
        # logger.info('getting request data shop  %s ', cityKey)
        if cityKey:
            # logger.info('getting request data shop  %s ', self.kwargs)
            result = model.WaShop.objects.filter(shoplocation__cityKey=cityKey).order_by('id')
            return result

        shopSn = self.request.query_params.get('sn')
        logger.info('getting request data shop status %s ', shopSn)
        if shopSn:
            # logger.info('getting request data shop status %s ', self.kwargs)
            return model.WaShop.objects.filter(shopSn=shopSn)

        return super(WaShopViewSet, self).get_queryset().order_by('id')

    def create(self, request, *args, **kwargs):
        shop_data = request.data.copy()

        # /book/1/chapter/
        # if self.kwargs.get('book_pk', None):
        #     chapter_data['book_id'] = self.kwargs.get('book_pk', None)
        #     if not Book.objects.filter(id=se.get('book_pk', None)):
        #         return Response('book.py not found', status=status.HTTP_404_NOT_FOUND)lf.kwargs

        logger.info('getting request data create category %s', shop_data)
        serializer = ic_serializer.WaShopSerializer(data=shop_data)

        if serializer.is_valid():
            if serializer.save():
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        error_msg = {
            'code': status.HTTP_400_BAD_REQUEST,
            'msg': serializer.errors
        }

        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        shop_data = request.data.copy()

        logger.info('getting request data create image data %s', shop_data)

        return super(WaShopViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """ 
            e.g. 
            {\n
                delete bulk of child resources, add header: X-BULK-OPERATION : true \n
                # Request \n
                DELETE ../shop/1/shopItem/ HTTP/1.1 \n
                Accept: application/json  \n
                X-BULK-OPERATION: true \n
            }
        """
        return super(WaShopViewSet, self).destroy(request, *args, **kwargs)


class WaShopAdsViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """
        shop ads
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (IsAuthenticated,)

    queryset = model.WaShopAds.objects.all()
    serializer_class = ic_serializer.WaShopAdsSerializer

    def get_queryset(self):
        logger.info('getting request data shop ads %s ', self.kwargs)
        shop_id = self.kwargs.get('shop_pk', None)
        if shop_id:
            try:
                shop = model.WaShop.objects.get(id=shop_id)
                return shop.shopAds.filter(washop__id=shop_id).order_by('id')  # many to many
            except model.WaShop.DoesNotExist:
                return self.queryset.none()

        return super(WaShopAdsViewSet, self).get_queryset().order_by('id')

    def create(self, request, *args, **kwargs):
        shop_ads_data = request.data.copy()

        # /book/1/chapter/
        # if self.kwargs.get('book_pk', None):
        #     chapter_data['book_id'] = self.kwargs.get('book_pk', None)
        #     if not Book.objects.filter(id=se.get('book_pk', None)):
        #         return Response('book.py not found', status=status.HTTP_404_NOT_FOUND)lf.kwargs

        logger.info('getting request data create shop_ads_data %s', shop_ads_data)
        serializer = ic_serializer.WaShopAdsSerializer(data=shop_ads_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        error_msg = {
            'code': status.HTTP_400_BAD_REQUEST,
            'msg': serializer.errors
        }

        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """ 
            e.g. 
            {\n
                delete bulk of child resources, add header: X-BULK-OPERATION : true \n
                # Request \n
                DELETE ../shop/1/shopAds/ HTTP/1.1 \n
                Accept: application/json  \n
                X-BULK-OPERATION: true \n
            }
        """
        return super(WaShopAdsViewSet, self).destroy(request, *args, **kwargs)


class ShopItemCategoryViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """
        shop category
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (IsAuthenticated,)

    queryset = model.ShopItemCategory.objects.all()
    serializer_class = ic_serializer.ShopItemCategorySerializer

    def list(self, request, *args, **kwargs):

        paginator = PageNumberPagination()

        # /tag/1/shopItem/
        company_id = self.kwargs.get('company_pk', None)
        pageSize = self.request.query_params.get('page', None)

        if company_id:
            # use serizlizer to query.... by setting many=True you tell drf that queryset contains mutiple items
            category_list = ShopItemCategorySerializer(self.get_queryset().filter(company_id=company_id).order_by('-entry_date'),
                                                       context={'request': request, }, many=True).data
            if not pageSize:
                return Response({
                    'count': len(category_list),
                    'results': category_list
                }, status=status.HTTP_200_OK)

            page = paginator.paginate_queryset(category_list, request)
            if page is not None:
                return paginator.get_paginated_response(page)

            return Response({
                    'count': len(category_list),
                    'results': category_list
                }, status=status.HTTP_200_OK)

        return super(ShopItemCategoryViewSet, self).list(self, request, *args, **kwargs)

    def get_queryset(self):
        return super(ShopItemCategoryViewSet, self).get_queryset().order_by('entry_date')


class BrandViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """
        shop brand
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (IsAuthenticated,)

    queryset = model.Brand.objects.all()
    serializer_class = ic_serializer.BrandSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        logger.info('getting request data shop ads %s ', self.kwargs)
        company_id = self.kwargs.get('company_pk', None)
        if company_id:
            return model.Brand.objects.filter(company_id=company_id).order_by('id')
        return super(BrandViewSet, self).get_queryset().order_by('id')

    def create(self, request, *args, **kwargs):
        brand_data = request.data.copy()

        # /book/1/chapter/
        # if self.kwargs.get('book_pk', None):
        #     chapter_data['book_id'] = self.kwargs.get('book_pk', None)
        #     if not Book.objects.filter(id=se.get('book_pk', None)):
        #         return Response('book.py not found', status=status.HTTP_404_NOT_FOUND)lf.kwargs

        logger.info('getting request data create shop_ads_data %s', brand_data)
        serializer = ic_serializer.BrandSerializer(data=brand_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        error_msg = {
            'code': status.HTTP_400_BAD_REQUEST,
            'msg': serializer.errors
        }

        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return super(BrandViewSet, self).destroy(request, *args, **kwargs)


class ShopItemViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """ 
        article \n
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (IsAuthenticated,)

    queryset = model.ShopItem.objects.all()
    serializer_class = ic_serializer.ShopItemSerializer

    """ 
        list method example  - not used
    """
    # def list(self, request, *args, **kwargs):
    #
    #     paginator = PageNumberPagination()
    #
    #     # /tag/1/shopItem/
    #     tag_id = self.kwargs.get('tag_pk', None)
    #     if tag_id:
    #         tag_item = ShopItemSerializer(self.get_queryset().filter(tags=tag_id), many=True).data
    #         page = paginator.paginate_queryset(tag_item, request)
    #         if page is not None:
    #             return paginator.get_paginated_response(page)
    #         return Response(tag_item)
    #
    #     shop_id = self.kwargs.get('shop_pk', None)
    #     if shop_id:
    #         shopItemList = ShopItemSerializer(self.get_queryset().filter(shop=shop_id), many=True).data
    #         page = paginator.paginate_queryset(shopItemList, request)
    #         if page is not None:
    #             # for shopItem in page:
    #             #     for key, value in shopItem.items():
    #             #         print(key, value)
    #
    #             return paginator.get_paginated_response(page)
    #
    #         return Response(shopItemList)
    #
    #     shopItemList = ShopItemSerializer(self.get_queryset().all(), many=True).data
    #     page = paginator.paginate_queryset(shopItemList, request)
    #     if page is not None:
    #         return paginator.get_paginated_response(page)
    #
    #     return Response(shopItemList)

    def list(self, request, *args, **kwargs):

        paginator = PageNumberPagination()

        # /tag/1/shopItem/
        category_id = self.kwargs.get('shopItemCategory_pk', None)
        pageSize = self.request.query_params.get('page', None)

        if category_id:
            category_item_list = ShopItemSerializer(self.get_queryset().filter(category_id=category_id).order_by('-entry_date'),
                                                    context={'request': request, },  many=True).data
            if not pageSize:
                return Response({
                    'count': len(category_item_list),
                    'results': category_item_list
                }, status=status.HTTP_200_OK)

            page = paginator.paginate_queryset(category_item_list, request)
            if page is not None:
                return paginator.get_paginated_response(page)

            return Response({
                    'count': len(category_item_list),
                    'results': category_item_list
                }, status=status.HTTP_200_OK)

        return super(ShopItemViewSet, self).list(self, request, *args, **kwargs)

    def get_queryset(self):
        logger.info('getting request data shopItem - %s ', self.kwargs)

        # /tag/1/shopItem/
        tag_id = self.kwargs.get('tag_pk', None)
        if tag_id:
            return model.ShopItem.objects.filter(tags=tag_id)

        shop_id = self.kwargs.get('shop_pk', None)
        if shop_id:
            logger.info('getting request shop id %s ', self.kwargs)
            return self.queryset.filter(shop=shop_id).order_by('-entry_date')

        brand_id = self.kwargs.get('brand_pk', None)
        if brand_id:
            return model.ShopItem.objects.filter(brand_id=brand_id).order_by('-entry_date')

        return super(ShopItemViewSet, self).get_queryset().order_by('-entry_date')

    def create(self, request, *args, **kwargs):
        shop_item_data = request.data.copy()
        arr_image = request.FILES.getlist('images')

        # # /shop/1/shopItem/
        # if self.kwargs.get('shop_pk', None):
        #     shop_item_data['shop_id'] = self.kwargs.get('shop_pk', None)
        #     if not model.shopType.objects.filter(id=self.kwargs.get('shop_pk', None)):
        #         return Response('shop not found', status=status.HTTP_404_NOT_FOUND)

        logger.info('getting request data create shop item %s', shop_item_data)

        shop_item_id = -1  # 用于图片保存，关联article id
        serializer = ic_serializer.ShopItemSerializer(data=shop_item_data)
        if serializer.is_valid():
            serializer.save()
            shop_item_id = serializer.data['id']

        error_msg = {
            'msg': serializer.errors
        }

        if shop_item_id == -1:
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        # 文章图片数量不为0， 进行保存
        if len(arr_image) != 0:
            image_data = {}
            for img in arr_image:
                image_data["img"] = img
                image_data["shopItem"] = shop_item_id
                image_serializer = ic_serializer.ImageSerializer(data=image_data)
                if image_serializer.is_valid():
                    image_serializer.save()

        msg = {
            'shopItem_id': serializer.data["id"]
        }

        return Response(msg, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """ 
            e.g. 
            {\n
                delete bulk of resources, add header: X-BULK-OPERATION : true \n
                # Request \n
                DELETE /shop/1/shopItem/ HTTP/1.1 \n
                Accept: application/json  \n
                X-BULK-OPERATION: true \n
            }
        """
        return super(ShopItemViewSet, self).destroy(request, *args, **kwargs)


class ItemOrderViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """ 
      list: \n
        {\n
            获取某一个订单 \n
            ../v1/api/itemOrder/31007414801512422/ \n  \n
            
            订单状态  e.g \n
            orderStatus : 0- 等待支付中, 1 - 已支付, 2 - 已取消, 3 - 未付款交易超时关闭，或支付完成后全额退款, 4 - 退款中 5- 该订单未被扫描  6- 交易结束，不可退款  
            
        }
     create: \n
        {\n
            创建订单  e.g \n
            
            {\n
                "company_id":4, \n
                "orderTitle":"商品平成", \n
                "totalPrize":0.01, \n
                "totalCount":2, \n
                "retailPrice":0.01, \n
                "totalPrice":0.02, \n
                "shopItem":【
                    {
                        id:1
                    }
                    ,
                    {
                    }
                】, \n
                "shop_id":1 \n
                "user_id":21 \n
                "orderAddress": 福州某区 \n
            }
        }
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (IsAuthenticated,)

    queryset = model.ItemOrder.objects.all()
    serializer_class = ic_serializer.ItemOrderSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_pk', None)
        if user_id:
            return model.ItemOrder.objects.filter(user_id=user_id).order_by('-entry_date')

        return super(ItemOrderViewSet, self).get_queryset().order_by('-entry_date')

    def create(self, request, *args, **kwargs):
        shopItemOrderData = request.data.copy()

        if shopItemOrderData.get('user_id', None) is None:
            return Response('user_id is required', status=status.HTTP_400_BAD_REQUEST)

        if shopItemOrderData.get('company_id', None) is None:
            return Response('company_id is required', status=status.HTTP_400_BAD_REQUEST)

        if shopItemOrderData.get('orderTitle', None) is None:
            return Response('orderTitle is required', status=status.HTTP_400_BAD_REQUEST)

        if shopItemOrderData.get('totalPrice', None) is None:
            return Response('totalPrice is required', status=status.HTTP_400_BAD_REQUEST)

        if shopItemOrderData.get('shopItems', None) is None:
            return Response('shopItems is required, e.g shopItems:[ {}, {}]', status=status.HTTP_400_BAD_REQUEST)

        if shopItemOrderData.get('orderAddress', None) is None:
            return Response('orderAddress is required', status=status.HTTP_400_BAD_REQUEST)

        try:
            company = model.Company.objects.get(id=shopItemOrderData.get('company_id', None))
        except model.Company.DoesNotExist:
            return Response('company not found', status=status.HTTP_404_NOT_FOUND)

        t = time.time()
        r = random.randint(1, 50)
        # print(alipaySecrectKey * int(round(t * 1000)))

        shopItemOrderData['orderNum'] = r * alipaySecrectKey * int(round(t))
        shopItemOrderData['update_timestamp'] = int(round(t * 1000))

        # if company.ali_appId and company.ali_publicKey and company.ali_privateKey:
        if company:
            # logger.info('getting request data create item order %s', shopItemOrderData)
            serializer = ic_serializer.ItemOrderSerializer(data=shopItemOrderData)
            if serializer.is_valid():
                serializer.save()

                logger.info('get shopItems %s', shopItemOrderData.get("shopItems"))
                # 生成订单商品列表
                for shopItem in shopItemOrderData.get("shopItems"):
                    shopItem['itemOrder_id'] = shopItemOrderData['orderNum']
                    serializer = ic_serializer.ItemOrderShopItemsSerializer(data=shopItem)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # 保存订单状态
                orderStatus = {}
                orderStatus['orderNum'] = shopItemOrderData['orderNum']
                orderStatus['orderStatus'] = 5
                orderStatus['update_timestamp'] = shopItemOrderData['update_timestamp']
                orderStatus['company_id'] = shopItemOrderData.get('company_id', None)
                orderItem_serializer = ic_serializer.ItemOrderStatusSerializer(data=orderStatus)
                if orderItem_serializer.is_valid():
                    orderItem_serializer.save()

                # result = alipay.preCreateOrder(company.ali_appId, company.ali_publicKey, company.ali_privateKey,
                #                                company.ali_notifyUrl, shopItemOrderData.get('orderTitle', None),
                #                                shopItemOrderData['orderNum'],
                #                                shopItemOrderData.get('totalPrize', None))
                return Response('', status=status.HTTP_201_CREATED)

            error_msg = {
                'code': status.HTTP_400_BAD_REQUEST,
                'msg': serializer.errors
            }
        else:
            return Response({
                "msg": '该公司支付校验签名无效',
            }, status=status.HTTP_400_BAD_REQUEST)

        # /book/1/chapter/
        # if self.kwargs.get('book_pk', None):
        #     chapter_data['book_id'] = self.kwargs.get('book_pk', None)
        #     if not Book.objects.filter(id=se.get('book_pk', None)):
        #         return Response('book.py not found', status=status.HTTP_404_NOT_FOUND)lf.kwargs

        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        shopItemOrderData = request.data.copy()

        if int(shopItemOrderData.get('totalCount')) < 0 or int(shopItemOrderData.get('actualTotalCount')) < 0:
            return Response('数量不能小于0', status=status.HTTP_400_BAD_REQUEST)

        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            itemOrderData = serializer.data

            # 保存订单状态
            try:
                orderStatus = model.ItemOrderStatus.objects.get(orderNum=itemOrderData.get('orderNum'))
                t = time.time()
                orderStatus.update_timestamp = int(round(t * 1000))

                if shopItemOrderData.get('totalCount') != shopItemOrderData.get('actualTotalCount'):
                    orderStatus.orderCompleteStatus = 2

                if shopItemOrderData.get('totalCount') == shopItemOrderData.get('actualTotalCount'):
                    orderStatus.orderCompleteStatus = 1
                orderStatus.save()
                return Response({
                    "msg": "success"
                }, status=status.HTTP_200_OK)
            except model.ItemOrderStatus.DoesNotExist:
                return Response({
                    "msg": '订单错误，更新订单状态失败'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            orderNum = self.kwargs.get('pk', None)
            if orderNum is not None:
                try:
                    itemOrderStatus = model.ItemOrderStatus.objects.get(orderNum=orderNum)
                    # if itemOrderStatus.orderStatus == 2:
                    #     return Response('该订单已取消', status=status.HTTP_200_OK)
                    try:
                        company = model.Company.objects.get(id=itemOrderStatus.company_id)

                        # result = alipay.cancel_the_order(orderNum, company.ali_appId, company.ali_publicKey,
                        #                                  company.ali_privateKey, company.ali_notifyUrl)
                        # if result.get('code') == '10000':
                        #     itemOrderStatus.orderStatus = 2
                        #     itemOrderStatus.save()
                        #     return Response('该订单已取消', status=status.HTTP_200_OK)

                        itemOrderStatus.orderStatus = 2
                        itemOrderStatus.save()
                        return Response({
                            "msg": '该订单已取消'
                        }, status=status.HTTP_200_OK)

                    except model.Company.DoesNotExist:
                        return Response({
                            "msg": '该订单关联方无效'
                        }, status=status.HTTP_404_NOT_FOUND)

                except model.ItemOrderStatus.DoesNotExist:
                    return Response({
                        "msg": '该订单不存在'
                    }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "msg": '需要提供订单号orderNum'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            pass

        return Response({
            "msg": '该订单不存在'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', ])
def itemOrderRefund(request):
    """ 
        post: \n
           e.g. 
           \n
            {\n
                "orderNum":31007707122106743  \n
            }\n
           
       """
    orderNum = request.data.get('orderNum')
    if orderNum:
        try:
            itemOrder = model.ItemOrder.objects.get(orderNum=orderNum)
            orderStatus = model.ItemOrderStatus.objects.get(orderNum_id=itemOrder.orderNum)
            if orderStatus.orderStatus == 3:
                return Response('该订单已经完成退款', status=status.HTTP_200_OK)
            try:
                company = model.Company.objects.get(id=itemOrder.company_id)
                result = alipay.need_refund(itemOrder.orderNum, company.ali_appId, company.ali_publicKey, company.ali_privateKey, company.ali_notifyUrl,
                                            itemOrder.totalPrize, str(itemOrder.orderNum*100))
                if result.get('code') == '10000':
                    orderStatus.orderStatus = 3
                    orderStatus.buyer_logon_id = result.get('buyer_logon_id')
                    orderStatus.buyer_user_id = result.get('buyer_user_id')
                    orderStatus.save()
                    return Response({
                        "msg": '该订单已经完成退款'
                    }, status=status.HTTP_200_OK)

                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            except model.Company.DoesNotExist:
                return Response({
                    "msg": '订单不合法，无法查询对应公司'
                }, status=status.HTTP_404_NOT_FOUND)

        except model.ItemOrder.DoesNotExist:
            return Response({
                "msg": '查无此订单'
            }, status=status.HTTP_404_NOT_FOUND)

    #
    # # print(company.ali_publicKey.url)
    # # my_file = open(data.ali_publicKey.url, 'r')
    # # txt = my_file.read()
    # # print(txt)
    # t = time.time()
    # result = alipay.need_refund(company.ali_appId, company.ali_publicKey, company.ali_privateKey, company.ali_notifyUrl,
    #                             0.01, ordrNum)

    return Response(orderNum, status=status.HTTP_404_NOT_FOUND)


class ItemOrderStatusViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """
       list: \n
        {\n
            获取某一个订单 \n
            ../v1/api/itemOrderStatus/31007414801512422/ \n  \n
            
            订单状态  e.g \n
            orderStatus : 0- 等待支付中, 1 - 已支付, 2 - 已取消, 3 - 未付款交易超时关闭，或支付完成后全额退款, 4 - 退款中 5- 该订单未被扫描  6- 交易结束，不可退款  
            
        }
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (IsAuthenticated,)

    queryset = model.ItemOrderStatus.objects.all()
    serializer_class = ic_serializer.ItemOrderStatusSerializer

    def get_queryset(self):
        orderNumber = self.kwargs.get('pk', None)
        if orderNumber:
            try:
                theItemOrder = model.ItemOrderStatus.objects.get(orderNum_id=orderNumber)
                if theItemOrder.orderStatus == 3 or theItemOrder.orderStatus == 6:
                    return super(ItemOrderStatusViewSet, self).get_queryset()

                try:
                    company = model.Company.objects.get(id=theItemOrder.company_id)
                    result = alipay.query_the_order(theItemOrder.orderNum_id, company.ali_appId,
                                                        company.ali_publicKey, company.ali_privateKey, company.ali_notifyUrl)
                        # 'code': '40004', 'msg': 'Business Failed', 'sub_code': 'ACQ.TRADE_NOT_EXIST'   - 订单生成，用户未扫描
                        # 'trade_status': 'WAIT_BUYER_PAY' 'buyer_logon_id': '376***@qq.com' 'buyer_user_id': '2088012375384674'  'code': '10000', 'msg': 'Success' - 订单生成，用户扫描二维码，但是等待支付中
                        # 'code': '10000', 'msg': 'Success', 'buyer_logon_id': '376***@qq.com' 'buyer_user_id': '2088012375384674'  'trade_status': 'TRADE_SUCCESS'

                    if result['code'] == '40004':
                        theItemOrder.orderStatus = 5

                    if result['code'] == '10000' and result['trade_status'] == 'TRADE_SUCCESS':
                        theItemOrder.orderStatus = 1

                    if result['code'] == '10000' and result['trade_status'] == 'WAIT_BUYER_PAY':
                        theItemOrder.orderStatus = 0

                    if result['code'] == '10000' and result['trade_status'] == 'TRADE_CLOSED':
                        theItemOrder.orderStatus = 3

                    if result['code'] == '10000' and result['trade_status'] == 'TRADE_FINISHED':
                        theItemOrder.orderStatus = 6

                    if result.get('buyer_logon_id'):
                        theItemOrder.buyer_logon_id = result.get('buyer_logon_id')

                    if result.get('buyer_user_id'):
                        theItemOrder.buyer_user_id = result.get('buyer_user_id')

                    if theItemOrder.orderStatus == 1:
                        t = time.time()
                        theItemOrder.update_timestamp = int(round(t * 1000))

                    theItemOrder.save()
                    return super(ItemOrderStatusViewSet, self).get_queryset()
                except model.Company.DoesNotExist:
                    return
            except model.ItemOrderStatus.DoesNotExist:
                return

        return super(ItemOrderStatusViewSet, self).get_queryset().order_by('-entry_date')


class CommentViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """
        comment
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (IsAuthenticated,)

    queryset = model.Comment.objects.all()
    serializer_class = ic_serializer.CommentSerializer

    def get_queryset(self):
        logger.info('getting request data comment %s ', self.kwargs)

        # /shopItem/1/comment/
        shop_item_id = self.kwargs.get('shopItem_pk', None)
        if shop_item_id:
            return model.Comment.objects.filter(shopItem=shop_item_id)

        return super(CommentViewSet, self).get_queryset().order_by('id')

    def create(self, request, *args, **kwargs):
        item_data = request.data.copy()

        # shopItem/1/comment/
        if self.kwargs.get('shopItem_pk', None):
            item_data['shop_item_id'] = self.kwargs.get('shopItem_pk', None)
            if not model.ShopItem.objects.filter(id=self.kwargs.get('shopItem_pk', None)):
                return Response('shop item not found', status=status.HTTP_404_NOT_FOUND)

        logger.info('getting request data create comment %s', item_data)
        serializer = ic_serializer.CommentSerializer(data=item_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        error_msg = {
            'code': status.HTTP_400_BAD_REQUEST,
            'msg': serializer.errors
        }

        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """ 
            e.g. 
            {\n
                delete bulk of resources, add header: X-BULK-OPERATION : true \n
                # Request \n
                DELETE ../article/1/comment/ HTTP/1.1 \n
                Accept: application/json  \n
                X-BULK-OPERATION: true \n
            }
        """
        return super(CommentViewSet, self).destroy(request, *args, **kwargs)


class TagViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """ 
       article tag
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication, )
        permission_classes = (IsAuthenticated,)

    queryset = model.Tag.objects.all()
    # queryset.query.set_limits(0, 5)
    serializer_class = ic_serializer.TagSerializer

    def get_queryset(self):
        logger.info('getting request data tag %s ', self.kwargs)
        article_id = self.kwargs.get('article_pk', None)
        if article_id:
            return model.Tag.objects.filter(article=article_id).order_by('id')
        return super(TagViewSet, self).get_queryset().order_by('id')

    def create(self, request, *args, **kwargs):
        logger.info('getting request data tag %s', request.data)
        serializer = ic_serializer.TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        error_msg = {
            'code': status.HTTP_400_BAD_REQUEST,
            'msg': serializer.errors
        }

        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """ 
            e.g. 
            {\n
                delete bulk of resources, add header: X-BULK-OPERATION : true \n
                # Request \n
                DELETE ../tag/ HTTP/1.1 \n
                Accept: application/json  \n
                X-BULK-OPERATION: true \n
            }
        """
        return super(TagViewSet, self).destroy(request, *args, **kwargs)


class CompanyViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
        """
            company location 
        """
        if allow_auth():
            authentication_classes = (JSONWebTokenAuthentication,)
            permission_classes = (IsAuthenticated,)

        queryset = model.Company.objects.all().order_by('id')
        serializer_class = ic_serializer.CompanySerializer


class shopLocationViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
        """
            shop location
        """
        if allow_auth():
            authentication_classes = (JSONWebTokenAuthentication,)
            permission_classes = (IsAuthenticated,)

        queryset = model.shopLocation.objects.all().order_by('id')
        serializer_class = ic_serializer.shopLocationSerializer
        pagination_class = PageNumberPagination

        #     paginator = PageNumberPagination()
        #
        #     # /tag/1/shopItem/
        #     tag_id = self.kwargs.get('tag_pk', None)
        #     if tag_id:
        #         tag_item = ShopItemSerializer(self.get_queryset().filter(tags=tag_id), many=True).data
        #         page = paginator.paginate_queryset(tag_item, request)
        #         if page is not None:
        #             return paginator.get_paginated_response(page)
        #         return Response(tag_item)

        def get_queryset(self):
            cityKey = self.request.query_params.get('cityKey')
            if cityKey:
                return model.shopLocation.objects.filter(cityKey=cityKey)

            return super(shopLocationViewSet, self).get_queryset().order_by('id')

        def update(self, request, *args, **kwargs):
            requestData = request.data.copy()
            requestData['shop'] = self.kwargs.get('pk', None)

            serializer = ic_serializer.shopLocationHistorySerializer(data=requestData)
            if serializer.is_valid():
                serializer.save()

            return super(shopLocationViewSet, self).update(request, *args, **kwargs)


class ImageUploaderViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
        """
            image uploader
        """
        if allow_auth():
            authentication_classes = (JSONWebTokenAuthentication,)
            permission_classes = (IsAuthenticated,)

        queryset = model.ImageUploader.objects.all().order_by('id')
        serializer_class = ic_serializer.ImageUploaderSerializer


class UserAddressViewSet(ListDestroyModelMixin, viewsets.ModelViewSet):
    """
        user address
    """
    if allow_auth():
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (IsAuthenticated,)

    queryset = model.UserAddress.objects.all().order_by('id')
    serializer_class = ic_serializer.UserAddressSerializer

    def get_queryset(self):
        logger.info('getting request data tag %s ', self.kwargs)
        user_id = self.kwargs.get('user_pk', None)
        if user_id:
            return model.UserAddress.objects.filter(user_id=user_id).order_by('-entry_date')
        return super(UserAddressViewSet, self).get_queryset().order_by('id')



from alipay import AliPay
import time

import ssl, base64


# alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkuXkfbkvCrzarADVuiZrKVWPup9vEqtgAif78Q9Xm9GsDsYVN/1+jQs5KMp8AXSOl6e+AKlggubfcSNw4zg+CSVJewyM+Q1cTwAbCy7Tf5P0uO2LEaUOWxah4qMxnWMF6S8/Fzko7zFR400u8u9olPcjVux4jLhpccFlyZye8WZnpl7vEwaQdZZ9EuVMnxEN5qJh6+mGJYMgEy6AsgjT6YsUZMnMi//klmWRYx2a+CFukApi2UJWcu77v7/tK9jkucerGb1ZMpvq3FyGCdD/6HC8zFzGAeiqnHP7cpXmnJ4yyaPczvjltX1bhJImn56sjcpDwgQsOHREWmygvgwtTQIDAQAB
# -----END PUBLIC KEY-----'''

# app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
# MIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCDSSiV8MxycckqvRcJvwvwfwhTJuBSZSiSbXruzdofp72gi42VM649mnkwYJyqFD18T3xXgm6Fv88DKEUVbRXEOcvECsqCaJoFzobAnsMB/A9MKBDQvGXzmyQoptM4mBWELKbte+iNPZCP52vyzIrlOkIrsVAsqkk9Vttn10cYtTRrEkSPo3mHjGK8P8Q6N74gLujBJxj2VnrMOcW7yF45dOMBbabd5sEjqGqTZUJSqc14Qd414sqAi2XErxGjGf4rBxZzlVMwbMt4ngYCfWXcwETut2/uagvyivi2Pv3OSiFdtf9sOXnpGv3BrtAMaTfddQeMb9CVCf8xaPS+jxH1AgMBAAECggEANPQTPLdNn3Op0mVGn5XBeRWkA/YQUOuge79Q8HVzX4VHBTSEvQOFai+eZhbx2eAkFLnyy1E+xw/grcNWahf/yZAOUlqP6B3M0j7FN3hR68EBYpReg/MZpDKVWRhA5fjh5Ngl1HBAEogcgQ61Cc/azi67deglEH7235jjEnVQpfQM2lHFWcol6mID3F+fwdkKI6leegx6FRgDoqsficwUwGRbxVLMLzBuSlPzUgkHk9ypcaAFGXvh5uWTvBt+BzgZtZ02HmiB2avGrQL+8yjEFMqTA9FqpH+EMwR455Mtk3Ty48KsPZfwTVdqu5U0iNjtfMruWP339pyh233lee3ZQQKBgQC+iDLtGUapYoyIqMkm5b4UduWAXUc1z3E5Vz1RLwBzGp0gCVZQ+CB94hW5D8NJaP9UWUkLajGkcChd9HS4A7j/xLEzgL4/KoIMQeAruv4gkhqbe0WBYDeZyJCVGbtn0EKD+dRbTgfe0EOO5k92qOsaHBjutHRBkEUwhjT43jRofQKBgQCwZXi1YwmChx+YZFpucVjBQ+oIk823yfZQDfl4byZqGVnDxC0/I50b0EMXGs3nqmx/wwNfXHwuMQJfhO3Dhn0M6O6ES8bJUK9Wv8y/bq7x83r0hXkw1kR9uNtNeN/PVnanZaXyIjiFhuYdMAP8B5KWBSWtsfVQBmjMzuIVGLSA2QJ/XQgj1aGB3zM/a3r+vP9w0I09gnAJVTz1DAqM5hcNISbdkcb9XovJUa4S7UnFERMzmPv/rpMrqh8ZlsbGNxOaQUjJPVyfiDg5R8Lisnebnku4sjJ+va09eNl1v1fRKd+GmuphxjNTpHgMhLnwEwBny1fs1KFIIrtPDWJ6ewoEjQKBgCyWmbqP/DloWo40378HG75OonvkkJ2iiYaW4baVsgojulMH5cAOCoqbTDos5ltm8uIgs1uJj0JF1Sm7+jXwau+2eYQre2Yr5QZymRjSq5oxR6VDj+zOXKXC8nxUz44jdv69bQMVr1/hR42dM4SjjWQqjOmpEC9YT2ll6jQW+JmRAoGBALzWyEX2oJNKO9ZmDe6xooVk3sT/8+U4muF1iZbtTRnXvmjQ9MoPsD5TdBNNIguoFsu2mhLfa1XLidxy5ps2AZawueUEXrUaHDl113HyrhFf656hr+Rw6Nv8QmvFJGLJp7FvnmzWD0//4xt1wrwFtIG8p1N7le19Eq3ZPkNKM8BO
# -----END RSA PRIVATE KEY-----'''

# 注意：一个是支付宝公钥，一个是应用私钥

# APP_ID = '2018090361238320'
NOTIFY_URL = "https://your_domain/alipay_callback"


def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'=' * (4 - missing_padding)
    return base64.decodebytes(data)


def init_alipay_cfg(appID:str, publicKey:str, privateKey:str, callbackUrl:str):
    '''
    初始化alipay配置
    :return: alipay 对象
    '''

    ssl._create_default_https_context = ssl._create_unverified_context
    publicKey = '''-----BEGIN PUBLIC KEY-----\n ''' + publicKey + '''\n-----END PUBLIC KEY-----'''
    privateKey = '''-----BEGIN RSA PRIVATE KEY-----\n''' + privateKey + '''\n-----END RSA PRIVATE KEY-----'''
    # print(publicKey)

    alipay = AliPay(
        appid=appID,
        app_notify_url=callbackUrl,  # 默认回调url
        # app_private_key_string=app_private_key_string,
        # alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        app_private_key_string=privateKey,
        alipay_public_key_string=publicKey,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False  # 默认False ,若开启则使用沙盒环境的支付宝公钥
    )
    return alipay


def get_qr_code(code_url):
    '''
    生成二维码
    :return None
    '''
    # print(code_url)
    # qr = qrcode.QRCode(
    #     version=1,
    #     error_correction=qrcode.constants.ERROR_CORRECT_H,
    #     box_size=10,
    #     border=1
    # )
    # qr.add_data(code_url)  # 二维码所含信息
    # img = qr.make_image()  # 生成二维码图片
    # img.save(r'C:\Users\SEEMORE\Desktop\qr_test_ali.png')
    # print('二维码保存成功！')


def preCreateOrder(appID:str, publicKey:str, privateKey:str, callBackUrl:str, subject: 'order_desc', out_trade_no: int, total_amount: (float, 'eg:0.01')):
    '''
    创建预付订单
    :return None：表示预付订单创建失败  [或]  code_url：二维码url
    '''
    result = init_alipay_cfg(appID, publicKey, privateKey, callBackUrl).api_alipay_trade_precreate(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount)
    #print('返回值：', result)
    code_url = result.get('qr_code')
    if not code_url:
        #print(result.get('预付订单创建失败：', 'msg'))
        return
    else:
        return result
        # return code_url


def query_order(out_trade_no: int, cancel_time: int and 'secs'):
    '''
    :param out_trade_no: 商户订单号
    :return: None
    '''
    # print('预付订单已创建,请在%s秒内扫码支付,过期订单将被取消！' % cancel_time)
    # check order status
    _time = 0
    for i in range(10):
        # check every 3s, and 10 times in all

        # print("now sleep 2s")
        time.sleep(2)

        result = init_alipay_cfg().api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            # print('订单已支付!')
            # print('订单查询返回值：', result)
            break

        _time += 2
        if _time >= cancel_time:
            cancel_order(out_trade_no, cancel_time)
            return


def query_the_order(out_trade_no: int, appID:str, publicKey:str, privateKey:str, callBackUrl:str):
    return init_alipay_cfg(appID, publicKey, privateKey, callBackUrl).api_alipay_trade_query(out_trade_no=out_trade_no)


def cancel_the_order(out_trade_no: int, appID:str, publicKey:str, privateKey:str, callBackUrl:str):
    result = init_alipay_cfg(appID, publicKey, privateKey, callBackUrl).api_alipay_trade_cancel\
        (out_trade_no=out_trade_no)
    return result


def cancel_order(out_trade_no: int, cancel_time=None):
    '''
    撤销订单
    :param out_trade_no:
    :param cancel_time: 撤销前的等待时间(若未支付)，撤销后在商家中心-交易下的交易状态显示为"关闭"
    :return:
    '''
    result = init_alipay_cfg().api_alipay_trade_cancel(out_trade_no=out_trade_no)
    # print('取消订单返回值：', result)
    resp_state = result.get('msg')
    action = result.get('action')
    if resp_state == 'Success':
        if action == 'close':
            if cancel_time:
                return 'cancel'
                #print("%s秒内未支付订单，订单已被取消！" % cancel_time)
        elif action == 'refund':
            return 'refund'
            #print('该笔交易目前状态为：', action)

        return action

    else:
        #print('请求失败：', resp_state)
        return


def need_refund(out_trade_no: int or str, appID:str, publicKey:str, privateKey:str, callBackUrl:str, refund_amount: int or float, out_request_no: str):
    '''
    退款操作
    :param out_trade_no: 商户订单号
    :param refund_amount: 退款金额，小于等于订单金额
    :param out_request_no: 商户自定义参数，用来标识该次退款请求的唯一性,可使用 out_trade_no_退款金额*100 的构造方式
    :return:
    '''
    result = init_alipay_cfg(appID, publicKey, privateKey, callBackUrl).api_alipay_trade_refund(out_trade_no=out_trade_no,
                                                       refund_amount=refund_amount,
                                                       out_request_no=out_request_no)

    return result  # 接口调用成功则返回result


def refund_query(out_request_no: str, out_trade_no: str or int):
    '''
    退款查询：同一笔交易可能有多次退款操作（每次退一部分）
    :param out_request_no: 商户自定义的单次退款请求标识符
    :param out_trade_no: 商户订单号
    :return:
    '''
    result = init_alipay_cfg().api_alipay_trade_fastpay_refund_query(out_request_no, out_trade_no=out_trade_no)

    if result["code"] == "10000":
        return result  # 接口调用成功则返回result
    else:
        return result["msg"]  # 接口调用失败则返回原因


# if __name__ == '__main__':
#     cancel_order(1527212120)
#     subject = "话费余额充值"
#     out_trade_no = int(time.time())
#     total_amount = 0.01
#     preCreateOrder(subject, out_trade_no, total_amount)
#
#     query_order(out_trade_no, 40)
#
#     print('5s后订单自动退款')
#     time.sleep(5)
#     print(need_refund(out_trade_no, 0.01, '111'))
#
#     print('5s后查询退款')
#     time.sleep(5)
#     print(refund_query(out_request_no='111', out_trade_no=out_trade_no))
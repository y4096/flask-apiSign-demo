# -*- coding: utf-8 -*-
#
# Python Client
#

from hashlib import sha256



class RequestClient(object):
    """ 接口签名客户端示例 """

    def __init__(self):
        self._accesskey_id = "demo_id"
        self._accesskey_secret = "demo_secret"

    def _sign(self, parameters):
        """ 签名
        @param parameters dict: uri请求参数(包含除signature外的公共参数)
        """
        if "signature" in parameters:
            parameters.pop("signature")
        # NO.1 参数排序
        _my_sorted = sorted(parameters.items(), key=lambda parameters: parameters[0])
        # NO.2 排序后拼接字符串
        canonicalizedQueryString = ''
        for (k, v) in _my_sorted:
            canonicalizedQueryString += '{}={}&'.format(k, v)
        canonicalizedQueryString += self._accesskey_secret
        # NO.3 加密返回签名: signature
        return sha256(canonicalizedQueryString.encode("utf-8")).hexdigest().upper()

    def set_signature_headers(self, params):
        # 设置headers
        signature_headers = dict(accesskey_id=self._accesskey_id)
        signature_headers.update(signature=self._sign({**params, **signature_headers}))
        return signature_headers

    def request(self):
        """测试用例"""
        import requests
        params = dict(a=1,b=2)
        url = 'http://192.168.255.10:1798?c=2'
        signature_headers = self.set_signature_headers(params)
        signature_headers['signature'] = 'demo_ida'
        print(signature_headers)
        # return requests.get(url, params=params, headers=signature_headers).json()
        return requests.post(url, json=params, headers=signature_headers).json()


if __name__ == '__main__':
    r = RequestClient()
    print(r.request())



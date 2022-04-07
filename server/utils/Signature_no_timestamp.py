# -*- coding: utf-8 -*-

from hashlib import sha256
from functools import wraps
from flask import request, jsonify


class Signature(object):
    """ 接口签名认证 """

    def __init__(self):
        self._accessKeys = [
            {"accesskey_id": "demo_id", "accesskey_secret": "demo_secret"}
        ]

    def _check_req_accesskey_id(self, req_accesskey_id):
        """ 校验accesskey_id
        @pram req_accesskey_id str: 请求参数中的用户标识id
        """
        if req_accesskey_id in [i['accesskey_id'] for i in self._accessKeys if "accesskey_id" in i]:
            return True
        return False

    def _get_accesskey_secret(self, accesskey_id):
        """ 根据accesskey_id获取对应的accesskey_secret
        @pram accesskey_id str: 用户标识id
        """
        return [i['accesskey_secret'] for i in self._accessKeys if i.get('accesskey_id') == accesskey_id][0]

    def _sign(self, parameters):
        """ 签名
        @param parameters dict: 除signature外请求的所有查询参数(公共参数和私有参数)
        """
        if "signature" in parameters:
            parameters.pop("signature")
        accesskey_id = parameters["accesskey_id"]
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''
        for (k, v) in sortedParameters:
            canonicalizedQueryString += '{}={}&'.format(k, v)
        canonicalizedQueryString += self._get_accesskey_secret(accesskey_id)
        signature = sha256(canonicalizedQueryString.encode("utf-8")).hexdigest().upper()
        return signature

    def _verification(self, req_params):
        """ 校验请求是否有效
        @param req_params dict: 请求的所有查询参数(公共参数和私有参数)
        """
        res = dict(msg='', success=False)
        try:
            req_accesskey_id = req_params["accesskey_id"]
            req_signature = req_params["signature"]
        except KeyError:
            res.update(msg="Invalid public params")
        except Exception:
            res.update(msg="Unknown server error")
        else:
            # NO.1 校验accesskey_id
            if self._check_req_accesskey_id(req_accesskey_id):
                # NO.2 校验签名
                if req_signature == self._sign(req_params):
                    res.update(msg="Verification pass", success=True)
                else:
                    res.update(msg="Invalid query string")
            else:
                res.update(msg="Invalid accesskey_id")
        return res

    def signature_required(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == "GET":
                params = request.args.to_dict()
            elif request.method == "POST":
                params = request.json
                print(params)
            else:
                return jsonify(dict(msg='only GET,POST allowed', success=False))
            headers = request.headers
            signature_headers = {'accesskey_id': headers['Accesskey-Id'], 'signature': headers['Signature']}
            res = self._verification({**params, **signature_headers})
            if res["success"] is True:
                return f(*args, **kwargs)
            else:
                return jsonify(res)

        return decorated_function

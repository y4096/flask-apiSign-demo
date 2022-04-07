# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from utils.Signature_no_timestamp import Signature

# 初始化定义application
app = Flask(__name__)
Sign = Signature()


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.errorhandler(500)
def server_error(error=None):
    message = {
        "msg": "Server error",
        "code": 500
    }
    return jsonify(message), 500


@app.errorhandler(404)
def not_found(error=None):
    message = {
        "msg": "Not found",
        "code": 404
    }
    return jsonify(message), 404


@app.errorhandler(403)
def Permission_denied(error=None):
    message = {
        "msg": "Permission denied",
        "code": 403
    }
    return jsonify(message), 403


@app.route("/", methods=['GET', 'POST'])
@Sign.signature_required
def index():
    # 正确请求将返回以下内容，否则将被signature_required拦截，返回请求验证信息： {"msg": "Invaild message", "success": False}
    return jsonify(ping="pong")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1798, debug=True)

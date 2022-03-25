# -*- coding: utf-8 -*-
"""
    utils.tool
    ~~~~~~~~~~~~~~

    Common function.

    :copyright: (c) 2017 by taochengwei.
    :license: MIT, see LICENSE for more details.
"""

import hashlib, time, datetime

sha256 = lambda pwd: hashlib.sha256(pwd).hexdigest()
get_current_timestamp = lambda: int(time.mktime(datetime.datetime.now().timetuple()))

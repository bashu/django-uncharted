# -*- coding: utf-8 -*-

import re
import simplejson as json

from datetime import datetime, date

JSDATE_REGEX = re.compile(r'"\*\*(new Date\([0-9,]+\))"')


def dumps(value):
    return JSDATE_REGEX.sub(r'\1', json.dumps(value, cls=JSONDateTimeEncoder, use_decimal=True))


class JSONDateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return '**new Date(%i,%i,%i,%i,%i,%i)' % (
                obj.year, obj.month-1, obj.day, obj.hour, obj.minute, obj.second)

        if isinstance(obj, date):
            return '**new Date(%i,%i,%i)' % (obj.year, obj.month-1, obj.day)

        return json.JSONEncoder.default(self, obj)

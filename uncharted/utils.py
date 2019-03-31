# -*- coding: utf-8 -*-

import re
import simplejson as json

from datetime import datetime, date

JSDATE_REGEX = re.compile(r'"\*\*(new Date\([0-9,]+\))"')


def dumps(value):
    return JSDATE_REGEX.sub(r'\1', json.dumps(
        value, cls=JSONDateTimeEncoder, use_decimal=True))


class JSONDateTimeEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return '**new Date(%i,%i,%i,%i,%i,%i)' % (
                o.year, o.month-1, o.day, o.hour, o.minute, o.second)

        if isinstance(o, date):
            return '**new Date(%i,%i,%i)' % (o.year, o.month-1, o.day)

        return json.JSONEncoder.default(self, o)

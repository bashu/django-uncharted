# -*- coding: utf-8 -*-


class FieldError(Exception):
    pass


class FieldDoesNotExist(Exception):
    pass


class ReadOnlyError(AttributeError):
    pass

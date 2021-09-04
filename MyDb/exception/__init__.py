# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:50 下午 
# @Author  : xujunpeng

from utils.logger import logger
import traceback


class BaseException(Exception):
    def __init__(self):
        logger.exception(traceback.format_exc())
        super(BaseException, self).__init__()


class TableExistError(BaseException):
    pass


class TableNameError(BaseException):
    pass


class SchemaNotFountError(BaseException):
    pass

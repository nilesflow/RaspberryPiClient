#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import json

def response(statusCode, dict):
    """
    関数終了共通処理
    """

    return {
        'isBase64Encoded': False,
        'statusCode': statusCode,
        'body':  json.dumps(dict),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def success(message = ""):
    """
    正常終了
    """
    return response(200, {'message' : message})

def error(statusCode, error, description):
    """
    エラー終了
    """
    return response(statusCode, {'error' : error, 'error_description': description})

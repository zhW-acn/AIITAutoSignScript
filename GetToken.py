import json
import logging

import requests

from Const import token_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_token(userCode, password):
    tokenData = {}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; SEA-AL10 Build/HUAWEISEA-AL10)'
    }

    request_data = {
        'password': password,
        'userCode': userCode
    }

    try:
        response = requests.post(token_URL, headers=headers, data=request_data, verify=False, timeout=100)
        if response.status_code == 200:
            respData = json.loads(response.text)
            if respData['flag']:
                logger.info("token请求成功")
                access_token = respData['data']['token']['access_token']
                tokenData['access_token'] = access_token
                userCode = respData['data']['token']['userCode']
                tokenData['userCode'] = userCode
                logger.info("学号："+userCode)
                logger.info("姓名："+respData['data']['token']['userName'])
            else:
                logger.info("认证失败")
                exit()
    except requests.exceptions.SSLError:
        print('获取Token失败。尝试关闭代理')
        exit()
    return tokenData

# 双周报
import time

import requests

from AutoSign import login

retryTime = 1 * 60 * 60
reLoginTime = 1 * 60
signURL = 'http://ims.aiit.edu.cn/signMobile/saveSign.do'
loginURL = 'https://in.aiit.edu.cn/uaac-server/login'
reportURL = 'http://ims.aiit.edu.cn/weeklyMobile/save.do'


# 双周报核心方法
def core():
    # 获取登录会话
    session = None

    while True:
        try:
            session = login()
        except requests.exceptions.SSLError as e:
            print("关闭代理")
        if session is None:
            print("登录失败，等待重试")
            time.sleep(reLoginTime)
            continue
        break

    headers = {
        'Host': 'ims.aiit.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': '349',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SEA-AL10 Build/HUAWEISEA-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046248 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://ims.aiit.edu.cn',
        'X-Requested-With': 'cn.edu.aiit.axx',
        'Referer': 'http://ims.aiit.edu.cn/dist/index.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-JP;q=0.8,en-US;q=0.7,en;q=0.6'
    }

    data = {
        'content': 'test本段时间工作内容1111111111111',
        'completionAndExperience': 'test完成心得111111111111',
        'startDate': '2024-07-07',
        'endDate': '2024-07-20',
        'whetherZc': 'false',
        'docVo': '[]',
        'userCode': '320202010337',
        '_userCode': '320202010337',
        'access_token': '76c8bb52-f91b-47d1-bb2b-7bb1be0bc71d',
        '_userType': '1'
    }

    # 发送 POST 请求
    response = requests.post(reportURL, headers=headers, data=data, verify=False)

    # 检查响应状态码
    if response.status_code == 200:
        print("请求成功")
        print("响应内容：", response.text)
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
        raise ValueError  # 随便抛一个异常


if __name__ == '__main__':
    core()

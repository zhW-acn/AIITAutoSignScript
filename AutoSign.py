# 打卡

import json
import time
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

# 登陆的学号、密码和重试时间
username = '320202010337'
password = 'Wzhwzhwzh@123'
retryTime = 1 * 60 * 60
reLoginTime = 1 * 60
signURL = 'http://ims.aiit.edu.cn/signMobile/saveSign.do'  # 打卡post请求
loginURL = 'https://in.aiit.edu.cn/uaac-server/login'  # 登录


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(doCore, "cron", hour=12, minute=00)  # 每天中午12点打卡

    try:
        while True:
            scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('打卡失败，' + retryTime.__str__() + '秒后重试')
        time.sleep(retryTime)
        scheduler.start()


# 登录
def login():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/126.0.0.0 Safari/537.36'
    }

    login_data = {
        'username': username,
        'password': password
    }

    login_session = requests.Session()

    response = login_session.post(loginURL, headers=headers, data=login_data)

    if response.status_code == 200:
        print("登录成功")
        return login_session
    else:
        print(f"登录失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
        return None


# 获取响应JSON里的打卡排名信息
def get_ranking(json_str):
    data = json.loads(json_str)
    ranking = data['data']['ranking']
    return str(ranking)


def doCore():
    session = None
    try:
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
        core(session)
    except ValueError:
        time.sleep(retryTime)
        core()


# 打卡核心方法
def core(session):
    # 设置要发送的表单数据
    data = {
        'access_token': '76c8bb52-f91b-47d1-bb2b-7bb1be0bc71d',
        '_userCode': username
    }

    headers = {
        # 'Content-Type': 'multipart/form-data; boundary=155e286c-6621-4875-a9ce-7170a730cba2',
        # 'Content-Length': '1165',
        # 'Host': 'ims.aiit.edu.cn',
        # 'Connection': 'Keep-Alive',
        # 'Accept-Encoding': 'gzip',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        #               'Chrome/126.0.0.0 Safari/537.36'
    }

    response = session.post(signURL, headers=headers, data=data, verify=False)

    if response.status_code == 200:
        print("打卡成功，第" + get_ranking(response.text) + "名")
    else:
        print(f"打卡失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
        raise ValueError  # 随便抛一个异常


if __name__ == '__main__':
    main()

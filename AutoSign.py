import argparse
import json
import time
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

retryTime = 1 * 60 * 60
signURL = 'http://ims.aiit.edu.cn/signMobile/saveSign.do'  # 打卡post请求
loginURL = 'https://in.aiit.edu.cn/uaac-server/login'  # 登录


def main():
    scheduler = BlockingScheduler()
    session = login()
    if session is None:
        logger.info('登录失败，检查学号和密码')
        return

    scheduler.add_job(doCore, "cron", hour=hour, minute=minute, args=[session])  # 打卡任务
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info('打卡失败，%d秒后重试', retryTime)
        time.sleep(retryTime)
        doCore(session)


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

    try:
        while True:
            response = login_session.post(loginURL, headers=headers, data=login_data)
            if response.status_code == 200:
                logger.info("%s ------ 登录成功", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                return login_session
            else:
                logger.error("登录失败，状态码: %d", response.status_code)
                logger.error("错误信息: %s", response.text)
                return None
    except requests.exceptions.SSLError:
        logger.info('登陆失败。尝试关闭代理')
        return None


# 获取响应JSON里的打卡排名信息
def get_ranking(json_str):
    data = json.loads(json_str)
    ranking = data['data']['ranking']
    return str(ranking)


def doCore(session):
    try:
        core(session)
    except ValueError:
        logger.info('打卡失败，%d秒后重试', retryTime)
        time.sleep(retryTime)
        core(session)


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
        logger.info("%s ------ 打卡成功，第%s名", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    get_ranking(response.text))
    else:
        logger.error("打卡失败，状态码: %d", response.status_code)
        logger.error("错误信息: %s", response.text)
        raise ValueError  # 随便抛一个异常


# 命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description="安小信实习打卡")
    parser.add_argument('-u', required=True, help='学号')
    parser.add_argument('-p', required=True, help='密码')
    parser.add_argument('-hour', required=True, help='24进制小时')
    parser.add_argument('-minute', required=True, help='分钟')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    username = args.u
    password = args.p
    hour = args.hour
    minute = args.minute
    main()

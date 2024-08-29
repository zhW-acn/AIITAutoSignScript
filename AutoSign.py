import argparse


# import json
# import time
# import requests
# from apscheduler.schedulers.blocking import BlockingScheduler
# import logging
#
# from Const import retryTime, signURL
# from GetToken import get_token
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
#
# def main():
#     scheduler = BlockingScheduler()
#     tokenData = get_token(username, password)
#     scheduler.add_job(doCore, "cron", hour=hour, minute=minute, args=[tokenData])  # 打卡任务
#     try:
#         scheduler.start()
#     except (KeyboardInterrupt, SystemExit):
#         scheduler.shutdown()
#         logger.info('打卡失败，%d秒后重试', retryTime)
#         time.sleep(retryTime)
#         doCore(tokenData)
#
#
# def doCore(tokenData):
#     try:
#         core(tokenData)
#     except ValueError:
#         logger.info('打卡失败，%d秒后重试', retryTime)
#         time.sleep(retryTime)
#         core(tokenData)
#
#
# # 打卡核心方法
# def core(tokenData):
#     # 设置要发送的表单数据
#     data = {
#         'access_token': tokenData.get('access_token'),
#         '_userCode': tokenData.get('userCode')
#     }
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/126.0.0.0 Safari/537.36'
#     }
#
#     response = requests.post(signURL, headers=headers, data=data, verify=False)
#
#     if response.status_code == 200:
#         respData = json.loads(response.text)
#         if respData['flag']:
#             logger.info("%s ------ 打卡成功，第%s名", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
#                         respData['data']['ranking'])
#         else:
#             logger.info("%s ------ 打卡失败", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
#                         response.text)
#     else:
#         logger.error("打卡失败，状态码: %d", response.status_code)
#         logger.error("错误信息: %s", response.text)
#         raise ValueError  # 随便抛一个异常


# 命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description="安小信实习打卡")
    parser.add_argument('-u', required=True, help='手机号')
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
    counter = 0
    for char in password:
        print(char, end="")
        print()  # 打印换行符


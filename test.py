import argparse


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
    print(args)
    print(args.u)

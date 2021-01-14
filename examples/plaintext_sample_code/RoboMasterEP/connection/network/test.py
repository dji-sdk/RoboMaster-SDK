# -*- encoding: utf-8 -*-
# 测试环境：Python 3.6 版本

import socket
import sys

# 组网模式下，机器人当前 IP 地址为 192.168.0.115, 控制命令端口号为 40923
# 机器人 IP 地址根据实际 IP 进行修改
host = "192.168.2.1"
port = 40923

def main():

        address = (host, int(port))

        # 与机器人控制命令端口建立 TCP 连接
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Connecting...")

        s.connect(address)

        print("Connected!")

        while True:

                # 等待用户输入控制指令
                msg = input(">>> please input SDK cmd: ")

                # 当用户输入 Q 或 q 时，退出当前程序
                if msg.upper() == 'Q':
                        break

                # 添加结束符
                msg += ';'

                # 发送控制命令给机器人
                s.send(msg.encode('utf-8'))

                try:
                        # 等待机器人返回执行结果
                        buf = s.recv(1024)

                        print(buf.decode('utf-8'))
                except socket.error as e:
                        print("Error receiving :", e)
                        sys.exit(1)
                if not len(buf):
                        break

        # 关闭端口连接
        s.shutdown(socket.SHUT_WR)
        s.close()

if __name__ == '__main__':
        main()
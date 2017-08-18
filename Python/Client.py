import socket
import threading

# 创建TCP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 向地址：localhost，端口：5550发起连接请求
sock.connect(('localhost', 5550))

# 向服务器发送现在状态，连接成功
sock.send('connect'.encode('utf-8'))

# 接受服务器欢迎消息
print(sock.recv(1024).decode('utf-8'))

# 输入用户名称，并发送至服务器存储
user_name = input('input your name: ')
sock.send(user_name.encode('utf-8'))


def sendmessagethread():
    while True:
        try:
            # 输入消息并发送
            message = input()
            sock.send(message.encode('utf-8'))
            # print(sock.recv(1024).decode())
        except ConnectionAbortedError:
            print('Server closed this connection!')
        except ConnectionResetError:
            print('Server is closed!')


def recvmessagethread():
    while True:
        try:
            # 如果收到消息就显示
            message = sock.recv(1024)
            if message:
                print(message.decode('utf-8'))
            else:
                pass
        except ConnectionAbortedError:
            print('Server closed this connection!')

        except ConnectionResetError:
            print('Server is closed!')

# 创建消息发送线程
sendthread = threading.Thread(target=sendmessagethread)

# 创建消息接收线程
recvthread = threading.Thread(target=recvmessagethread)
threads = [sendthread, recvthread]

for messagethread in threads:
    # 将主线程设为守护线程
    messagethread.setDaemon(True)
    # 开启线程
    messagethread.start()
    # 1.join方法的作用是阻塞主进程，专注执行多线程。
    # 2.多线程多join的情况下，依次执行各线程的join方法，前头一个结束了才能执行后面一个。
    # 3.无参数，则等待到该线程结束，才开始执行下一个线程的join。
    messagethread.join()

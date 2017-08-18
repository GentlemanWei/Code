import socket
import threading

# 创建TCP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 启动地址重用
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定地址：localhost，端口：5550
sock.bind(('localhost', 5550))

# 侦听客户端
sock.listen(5)
print('Server', socket.gethostbyname('localhost'), 'listening ...')

# 用户信息字典
user_dicts = dict()

# socket连接列表
socket_lists = list()


# 把message传给除了despatcher的所有人
def deliver(despatcher, message):

    # 遍历整个连接列表
    for socket_list in socket_lists:
        if socket_list.fileno() != despatcher:
            try:

                # 以utf-8的格式发送message
                socket_list.send(message.encode('utf-8'))
            except TypeError:
                pass


def system_thread(socket_connection, connection_number):
    try:
        user_name = socket_connection.recv(1024).decode('utf-8')
    except ConnectionResetError:
        print('远程主机强迫关闭了一个现有的连接。')
    except socket.error:
        pass
    else:
        # socket对象的fileno()方法返回关于这个socket的文件描述符
        user_dicts[socket_connection.fileno()] = user_name

        # 将当前连接的socket添加到socket_lists中
        socket_lists.append(socket_connection)
        print('connection', connection_number, ' has name :', user_name)

        # 发送系统消息有用户进入聊天室
        deliver(connection_number, '【系统提示：' + user_dicts[connection_number] + ' 进入聊天室】')
        while True:
            try:

                # 接收用户消息
                recvedmessage = socket_connection.recv(1024).decode('utf-8')
                if recvedmessage:
                    # 若消息不为空，将消息进行广播
                    print(user_dicts[connection_number], ':', recvedmessage)
                    deliver(connection_number, user_dicts[connection_number] + ' :' + recvedmessage)

            except (OSError, ConnectionResetError):
                try:

                    # 当出现异常的时候，从列表中移除socket对象
                    socket_lists.remove(socket_connection)
                except OSError:
                    pass

                # 发送系统消息有用户离开聊天室
                print(user_dicts[connection_number], 'exit, ', len(socket_lists), ' person left')
                deliver(connection_number, '【系统提示：' + user_dicts[connection_number] + ' 离开聊天室】')

                # 关闭异常的socket连接
                socket_connection.close()
                return


while True:
    connection, addr = sock.accept()
    print('Accept a new connection', connection.getsockname(), connection.fileno())
    try:
        # connection.settimeout(5)
        request = connection.recv(1024).decode('utf-8')
        if request == 'connect':
            connection.send('welcome to server!'.encode('utf-8'))

            # 为当前连接开辟一个新的线程
            client_thread = threading.Thread(target=system_thread, args=(connection, connection.fileno()))
            # 将主线程设置为守护线程，主线程结束时一并结束所有线程
            client_thread.setDaemon(True)
            client_thread.start()

        else:
            connection.send('please go out!'.encode('utf-8'))
            connection.close()
    except ConnectionResetError:
        pass

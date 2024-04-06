# coding: utf -8
import PySimpleGUI as sg # ライブラリの読み込み
import threading
import sys
import socket
from socket import socket, AF_INET, SOCK_DGRAM ,SOCK_STREAM
import time

# バッファサイズ指定
BUFSIZE = 14600
# テーマの設定
sg.theme("SystemDefault ")

# 事前設定
L1 = [[sg.Text("・IP address "            ,size=(20,1)),
    sg.InputText(default_text="127.0.0.2" ,     text_color = "#000000",background_color ="#ffffff" ,    size=(40,1),    key="-IP_ADDR" )],
    [sg.Text("・port num "            ,size=(20,1)),
    sg.InputText(default_text="49152" ,            text_color = "#000000",background_color ="#ffffff" ,    size=(40,1),    key="-PORT_NUM-" )]
]
# UDP
L2 = [[sg.Button("OPEN", border_width=4 ,    size =(25,1),    key="-BTN_UDP_OPEN-")]]

# TCP
L3 = [[sg.Button("OPEN", border_width=4 ,     size =(25,1),    key="-BTN_TCP_OPEN-")]]

# 通信ステータス
L4 = [[sg.Multiline(default_text="", border_width=1,    size=(62,10),    key="-COM_ST-")]]

L = [[sg.Frame("Socket config",L1)],
    [sg.Frame("UDP",L2),sg.Frame("TCP",L3)],
    [sg.Frame("Connection status",L4)]]

# ウィンドウ作成
window = sg.Window ("TCP/UDP sever tool", L)
values = ""

def main():
    global values
    threads = []
    # イベントループ
    while True:
        # イベントの読み取り（イベント待ち）
        event , values = window.read()
        # 確認表示
        # print(" イベント:",event ,", 値:",values)
        # 終了条件（ None: クローズボタン）
        if event == "-BTN_UDP_OPEN-":
            t1 = threading.Thread(target=udp_recv, args=(values['-IP_ADDR'] , int(values['-PORT_NUM-']),))
            threads.append(t1)
            t1.setDaemon(True)
            t1.start()
            window["-COM_ST-"].Update("----------UDP open----------")

        # TCP接続
        elif event == "-BTN_TCP_OPEN-":
            t2 = threading.Thread(target=tcp_recv, args=(values['-IP_ADDR'] , int(values['-PORT_NUM-']),))
            threads.append(t2)
            t2.setDaemon(True)
            t2.start()
            window["-COM_ST-"].Update("----------TCP open----------")
        elif event == None:
            sys.exit()


def main_window_update_open():
    global values
    window_txt = "----------TCP connect----------\n"
    window["-COM_ST-"].Update(window_txt)
    print(window_txt)
    return


def main_window_update(protocol,data):
    global values
    window_txt = ""
    window_txt += "----------{} data recieve----------\n".format(protocol) \
                + "Recv data:" + data + "\n"
    window["-COM_ST-"].Update(window_txt)
    print(window_txt)
    return


def main_window_update_close():
    global values
    window_txt = "----------TCP disconnect----------\n"
    window["-COM_ST-"].Update(window_txt)
    print(window_txt)
    return


def udp_recv( ip_addr , port ):
    protocol = "UDP"
    # 受信側アドレスをtupleに格納
    SrcAddr = ( ip_addr , port)
    # ソケット作成
    udpServSock = socket(AF_INET, SOCK_DGRAM)
    # 受信側アドレスでソケットを設定
    udpServSock.bind(SrcAddr)
    time.sleep(1)
    # While文を使用して常に受信待ちのループを実行
    while True:
        time.sleep(1)
        # ソケットにデータを受信した場合の処理
        # 受信データを変数に設定
        data, addr = udpServSock.recvfrom(BUFSIZE)
        # 受信データを確認
        main_window_update(protocol,data.hex())


def recv_client(connection, client):
    protocol = "TCP"
    while True:
        try:
            data = connection.recv(BUFSIZE)
            if 0 != len(data):
                main_window_update(protocol,data.hex())
            else:
                break
        except ConnectionResetError:
            break
    connection.close()
    main_window_update_close()


def tcp_recv( ip_addr , port ):
    tcp_server = socket(AF_INET, SOCK_STREAM)
    tcp_server.bind(( ip_addr , port))
    tcp_server.listen()
    time.sleep(1)
    while True:
        (connection, client) = tcp_server.accept()
        main_window_update_open()
        thread = threading.Thread(target=recv_client, args=(connection, client))
        # スレッド処理開始
        thread.start()


if __name__ == '__main__':
    main()


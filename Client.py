# coding: utf -8
import PySimpleGUI as sg # ライブラリの読み込み
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
# バッファサイズ指定
BUFSIZE = 14600
# テーマの設定
sg.theme("SystemDefault ")

# 事前設定
L1 = [
    # 診断機設定
    [sg.Text("・src IP address ",size=(15,1)),
    sg.InputText(default_text="127.0.0.1" , text_color = "#000000",background_color ="#ffffff",        size=(15,1),    key="-SRC_IP_ADDR-" ),
    sg.Text("     ")],
    [sg.Text("・src port num  ",size=(15,1)),
    sg.InputText(default_text="49152" ,    text_color = "#000000",background_color ="#ffffff" ,        size=(8,1),        key="-SRC_PORT_NUM-" )],
    [sg.Text("・dest IP address ",size=(15,1)),
    sg.InputText(default_text="127.0.0.2" , text_color = "#000000",background_color ="#ffffff" ,    size=(15,1),    key="-DEST_IP_ADDR-" ),
    sg.Text("     ")],
    [sg.Text("・dest port num  ",size=(15,1)),
    sg.InputText(default_text="49152" ,    text_color = "#000000",background_color ="#ffffff" ,        size=(8,1),        key="-DEST_PORT_NUM-" )],
 ]

# UDP
L2 = [[sg.Button("send", border_width=4 ,    size =(10,1),    key="-BTN_SEND_UDP-")]
]

# TCP
L3 = [[sg.Button("connect", border_width=4 , size =(10,1),    key="-BTN_CONECT_TCP-"),
    sg.Button("send", border_width=4 ,         size =(10,1),    key="-BTN_SEND_TCP-"),
    sg.Button("disconnect", border_width=4 , size =(10,1),    key="-BTN_DISSCONECT_TCP-")]
]

# Send data
L4 = [
    [sg.Multiline(default_text="" , border_width=2,        size=(55,22),    key="-PAYLOAD-")]
]

L5 = [
    [sg.Multiline(default_text="", border_width=1,    size=(58,26),autoscroll=True,    key="-COM_ST-")]]

L =[
    [
    sg.Frame("Settings",
        [
            [sg.Frame("Socket config ",L1,size=(420,130))],
            [sg.Frame("Send data",L4)]
        ]
    ),
    sg.Frame("communication",
        [
            [sg.Frame("UDP",L2),sg.Frame("TCP",L3)],
            [sg.Frame("Connection status",L5)]
        ]
    ),
    ]
]

L_NEW = []

# ウィンドウ作成
window = sg.Window ("TCP/UDP cliant tool", L)
values = ""

def main():
    global values
    # イベントループ
    while True:
        # イベントの読み取り（イベント待ち）
        event , values = window.read()
        window_txt = ""
        # 確認表示
        # print(" イベント:",event ,", 値:",values)
        # 終了条件（ None: クローズボタン）
        if event == "-BTN_SEND_UDP-":
            window_txt += "----------UDP send----------"
            window_txt += main_udp_send(values)
        elif event == "-BTN_CONECT_TCP-":
            tcp_connect( values['-SRC_IP_ADDR-'] , values['-DEST_IP_ADDR-'] , int(values['-SRC_PORT_NUM-']) , int(values['-DEST_PORT_NUM-']) )
            window_txt +=  "----------TCP connect----------\n"
        elif event == "-BTN_SEND_TCP-":
            window_txt += "----------TCP send----------\n"
            window_txt += main_tcp_send(values)
        elif event == "-BTN_DISSCONECT_TCP-":
            tcp_close()
            window_txt +=  "----------TCP disconnect----------\n"
            window["-SRC_PORT_NUM-"].Update( int(values["-SRC_PORT_NUM-"]) + 1)
        elif event == None:
            print(" 終了します． ")
            break
        print(window_txt.replace("\n\n\n","\n\n"))
        if "" == values['-COM_ST-']:
            window["-COM_ST-"].Update(window_txt.replace("\n\n\n","\n\n"))
        else:
            window["-COM_ST-"].Update(values['-COM_ST-']+ "\n\n" + window_txt.replace("\n\n\n","\n\n"))
    # 終了処理
    window.close()


def main_udp_send(values):
    rtn = ""
    if None != values["-PAYLOAD-"]:
        rtn =  "\nsend data:" + values["-PAYLOAD-"].upper()+ "\n\n"
        udp_send( values['-SRC_IP_ADDR-'] , values['-DEST_IP_ADDR-'] , int(values['-SRC_PORT_NUM-']) , int(values['-DEST_PORT_NUM-']) , bytes.fromhex(values["-PAYLOAD-"]) )
    return rtn


def udp_send( src_ip , dst_ip , src_port , dst_port , data ):
    # 送信側アドレスをtupleに格納
    SrcAddr = ( src_ip , src_port )
    # 受信側アドレスをtupleに格納
    DstAddr = ( dst_ip , dst_port )
    # ソケット作成
    udpClntSock = socket(AF_INET, SOCK_DGRAM)
    # 送信側アドレスでソケットを設定
    udpClntSock.bind(SrcAddr)
    # 受信側アドレスにペイロード長単位で送信
    chunk_size = 1468
    # ペイロード長単位で送信
    for i in range(0, len(data), chunk_size ):
        chunk = data[i:i+chunk_size]
        udpClntSock.sendto(chunk,DstAddr)
    return


def tcp_connect( src_ip , dst_ip , src_port , dst_port ):
    global tcpClntSock
    # ソケット作成
    tcpClntSock = socket(AF_INET, SOCK_STREAM)
    tcpClntSock.settimeout(0.5)
    # 送信側アドレスをtupleに格納
    SrcAddr = ( src_ip , src_port )
    # 送信側アドレスでソケットを設定
    tcpClntSock.bind(SrcAddr)
    # サーバーに接続
    tcpClntSock.connect((dst_ip, dst_port))


def tcp_close():
    global tcpClntSock
    # ソケットクローズ
    tcpClntSock.close()


def main_tcp_send(values):
    rtn = ""
    if None != values["-PAYLOAD-"]:
        rtn = "send data:" + values["-PAYLOAD-"].upper()+ "\n\n"
        tcp_send( bytes.fromhex(values["-PAYLOAD-"]) )
    return rtn


def tcp_send( data ):
    global tcpClntSock
    chunk_size = 1456
    # ペイロード長単位で送信
    for i in range(0, len(data), chunk_size ):
        chunk = data[i:i+chunk_size]
        tcpClntSock.send(chunk)
    return


if __name__ == '__main__':
    main()
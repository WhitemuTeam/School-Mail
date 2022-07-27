import PySimpleGUI as sg
import online
import os,threading,time
from datetime import datetime

sg.theme('Reddit')

def Log_in_gui():
    '''
    登录界面
    '''
    # 读取key文件
    Username,ClassID = online.read_key()
    if Username==False:
        Username=''
        ClassID=''
    layout=[
        [sg.Text('用户名')],
        [sg.Input(Username)],
        [sg.Text('班级ID')],
        [sg.Input(ClassID)],
        [sg.Button('进入'),sg.Push(),sg.Button('注册班级')]
    ]
    lg=sg.Window('开始界面',layout,font=('微软雅黑'))
    while True:
        event,value=lg.Read()
        if event==sg.WIN_CLOSED:
            os._exit(0)
        if event=='注册班级':
            lg.Close()
            online.Reg_Class_GUI()
            return Log_in_gui()
        Username=value[0]
        ClassID=value[1]
        if Username=='' or ClassID=='':
            sg.Popup('用户名或班级ID不能为空!')
            continue
        else:
            lg.Close()
            online.save_key(Username,ClassID)
            return Username,ClassID

def Time_Get(datetimes=False):
    '''
    返回时间字符串
    '''
    if not datetimes:
        datetimes=datetime.now()
    time_str = datetime.strftime(datetimes,'%m-%d %H:%M:%S')
    return time_str

def Format_Message(CreateAt,Username,Message):
    '''
    格式化信息
    '''
    return CreateAt+' '+Username+' 说: '+Message

def Get_New_Five_Message(ClassID):
    '''
    从云端获取信息后格式化
    :Return: 格式化后的5条新信息和一条最新信息
    '''
    Messages_list,Usernames_list,CreatAt_list = online.get_message(ClassID)
    NewMessage_str = ''
    for num in range(len(Messages_list)):
        NewMessage_str += Format_Message(Time_Get(CreatAt_list[num]),Usernames_list[num],Messages_list[num]) + '\n'
    if len(Messages_list) >= 1:
        LastestMessage_str = Format_Message(Time_Get(CreatAt_list[-1]),Usernames_list[-1],Messages_list[-1])
    else:
        LastestMessage_str = ''
    return NewMessage_str,LastestMessage_str

def main():
    Username,ClassID = Log_in_gui()
    NewMessage_str,Old_Message = Get_New_Five_Message(ClassID)
    layout =[
        [sg.Text('消息框')],
        [sg.Multiline(size=(80,20),key='_OUTPUT_',default_text=NewMessage_str,disabled=True,autoscroll=True,text_color='blue')],
        [sg.Text('发送新消息:')],
        [sg.Input(size=(75,5),key='_INPUT_'),sg.Button('发送')],
    ]
    window = sg.Window('消息框',layout,font=('微软雅黑 10'),size=(700,500),return_keyboard_events=True)
    # def Update_Message():
    #     while True:
    #         print('Updating Message...')
    #         window.Element('_OUTPUT_').Update(online.get_realtime_message(ClassID,Old_Message),text_color_for_value='red',append=True)
    #         time.sleep(3)
    # threading.Thread(target=Update_Message).start()
    while True:
        event,value = window.Read(timeout=1500)
        if event == sg.WIN_CLOSED:
            window.Close()
            return None
        elif event in ('\r','发送'):
            Message = value['_INPUT_']
            Message_Time = online.send_message(Message)
            Old_Message = Format_Message(Message_Time,Username,Message)
            window.Element('_OUTPUT_').Update(Old_Message+'\n',text_color_for_value='black',append=True)
            window.Element('_INPUT_').Update('')
        elif event == '__TIMEOUT__':
            print('Updating Message...')
            Realtime_message = online.get_realtime_message(ClassID,Old_Message)
            if Realtime_message != '':
                Old_Message = Realtime_message
                window.Element('_OUTPUT_').Update(Realtime_message+'\n',text_color_for_value='red',append=True)
if __name__ == "__main__":
    main()
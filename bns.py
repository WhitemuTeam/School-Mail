from windows_toasts import WindowsToaster, ToastImageAndText4
from online import get_realtime_message
from datetime import datetime
import PySimpleGUI as sg
import leancloud,time,platform
import pytz

def notice(Username,Message):
    #判断Windows版本是否高于Windows 8
    if int(platform.release()) >= 8:
        newToast = ToastImageAndText4()
        newToast.SetHeadline("School Mail有新消息啦~")
        newToast.SetBody("{} 说:\n{}".format(Username,Message))
        newToast.SetImage('LOGO.ico')
        # newToast.on_activated = lambda _: print('Toast clicked!')
        WindowsToaster('School Mail').show_toast(newToast)
    else:
        sg.set_options(font=('微软雅黑 10'))
        sg.popup_notify("{} 说:\n{}".format(Username,Message),title='School Mail有新消息啦~',display_duration_in_ms=10000)
    return None

def read_key():
    import json,os
    if os.path.isfile('data/key.json'):
        with open('data/key.json','r') as f:
            key=json.loads(f.read())
        ClassID=key['ClassID']
        return ClassID
    else:
        return False

def Format_Message(CreateAt,Username,Message):
    '''
    格式化信息
    '''
    CreateAt = datetime.strftime(CreateAt,'%m-%d %H:%M:%S')
    return CreateAt+' '+Username+' 说: '+Message

def get_realtime_message(Old_Message_CreatedAt) -> str:
    '''
    获取到最新的一条信息
    :return 返回最新的一条信息,顺序为Message,Username,createdAt
    '''
    if read_key():
        ClassID = read_key()
    # 绑定到MailBox类
    class_obj = leancloud.Object.extend('MailBox')
    # 查询服务
    class_obj_query = class_obj.query
    # 查询该班级ID的信息
    class_obj_query.equal_to('Class_ID',ClassID)
    # 获取信息
    class_obj_query_result = class_obj_query.find()
    if class_obj_query_result == []:
        return False
    else:
        Lastest_Message_CreatedAt = class_obj_query_result[-1].get('createdAt').replace(tzinfo=pytz.UTC)
        if Lastest_Message_CreatedAt > Old_Message_CreatedAt:
            return Lastest_Message_CreatedAt,class_obj_query_result[-1].get('Username'),class_obj_query_result[-1].get('Message')
        else:
            return False

def main():
    Old_Message_CreatedAt = datetime.now().replace(tzinfo=pytz.UTC)
    while True:
        print('Checking....')
        Message_Data = get_realtime_message(Old_Message_CreatedAt)
        if Message_Data:
            print('New Message!')
            notice(Message_Data[1],Message_Data[2])
            Old_Message_CreatedAt = Message_Data[0]
        time.sleep(5)

if __name__ == "__main__":
    main()
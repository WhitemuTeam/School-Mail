import leancloud,os,json
import PySimpleGUI as sg
from datetime import datetime

# 注意配置LeanCloud的AppID和AppKey
if os.path.isfile('data/leancloud.json'):
    with open('data/leancloud.json','r') as f:
        data = json.loads(f.read())
        leancloud.init(data['AppID'],data['AppKey'])
else:
    sg.Popup('请先配置LeanCloud的AppID和AppKey')
    os._exit(0)

sg.theme('Reddit')

def Format_Message(CreateAt,Username,Message):
    '''
    格式化信息
    '''
    CreateAt = datetime.strftime(CreateAt,'%m-%d %H:%M:%S')
    return CreateAt+' '+Username+' 说: '+Message

def save_key(Username=None,ClassID=None):
    import json
    key={
        'Username':Username,
        'ClassID':ClassID,
    }
    with open('data/key.json','w') as f:
        f.write(json.dumps(key))

def read_key():
    import json,os
    if os.path.isfile('data/key.json'):
        with open('data/key.json','r') as f:
            key=json.loads(f.read())
        Username=key['Username']
        ClassID=key['ClassID']
        return Username,ClassID
    else:
        return False,False

def Get_Class_ID() -> str:
    '''
    获取到可用的班级ID
    '''
    import random
    Class_ID=random.randint(1000,9999)
    print('Class_ID -> ',Class_ID)
    Class_ID='C'+str(Class_ID)
    Class_list_services = leancloud.Object.extend('MailClassList') #定位到MailClassList类
    Class_list_service = Class_list_services.query #查询服务
    Class_ID_Status = Class_list_service.equal_to('Class_ID',Class_ID).find() #查询该班级ID是否被占用
    if Class_ID_Status == []:
        return Class_ID
    else:
        Get_Class_ID()

def Reg_Class_GUI():
    layout=[
        [sg.Text('填写简单的信息以新建班级')],
        [sg.Text('班级名:')],
        [sg.Input()],
        [sg.Button('创建')]
    ]
    window = sg.Window('创建班级',layout,font=('微软雅黑 10'))
    event,value = window.Read()
    if event == sg.WIN_CLOSED:
        window.Close()
        return None
    ClassName=value[0]
    if ClassName=='':
        sg.Popup('班级名不能为空!')
        return None
    # 通过leancloud注册班级
    class_obj = leancloud.Object.extend('MailClassList')
    class_obj = class_obj()
    class_obj.set('ClassName',ClassName)
    Class_ID = Get_Class_ID()
    class_obj.set('Class_ID',Class_ID)
    class_obj.save()
    # 保存班级ID
    window.Close()
    save_key(Username='',ClassID=Class_ID)

# 获取云端信息
def get_message(ClassID) -> list:
    '''
    获取到最新的前五条信息
    :param ClassID: 班级ID
    :return 返回最新的前五条信息,顺序为Message,Username,CreatedAt
    '''
    # 绑定到MailBox类
    class_obj = leancloud.Object.extend('MailBox')
    # 查询服务
    class_obj_query = class_obj.query
    # 查询该班级ID的信息
    class_obj_query.equal_to('Class_ID',ClassID)
    # 获取信息
    class_obj_query_result = class_obj_query.find()
    # 返回信息
    # 检查是否有信息
    if class_obj_query_result == []:
        return [],[],[]
    else:
        Messages_list,Usernames_list,CreatAt_list = [],[],[]
        for i in class_obj_query_result:
            Messages_list.append(i.get('Message'))
            Usernames_list.append(i.get('Username'))
            CreatAt_list.append(i.get('createdAt'))
        return Messages_list,Usernames_list,CreatAt_list

#发送信息至云端
def send_message(message):
    '''
    返回一个时间字符串以校准时间
    '''
    Username,ClassID = read_key()
    # 绑定到MailBox类
    class_obj = leancloud.Object.extend('MailBox')
    class_obj = class_obj()
    # 发送信息,包括班级ID和用户名
    class_obj.set('Message',message)
    class_obj.set('Class_ID',ClassID)
    class_obj.set('Username',Username)
    class_obj.save()
    return datetime.strftime(class_obj.get('createdAt'),'%m-%d %H:%M:%S')

# 实时获取云端信息
def get_realtime_message(ClassID,OldMessage) -> str:
    '''
    获取到最新的一条信息
    :param ClassID: 班级ID
    :return 返回最新的一条信息,顺序为Message,Username,createdAt
    '''
    # 绑定到MailBox类
    class_obj = leancloud.Object.extend('MailBox')
    # 查询服务
    class_obj_query = class_obj.query
    # 查询该班级ID的信息
    class_obj_query.equal_to('Class_ID',ClassID)
    # 获取信息
    class_obj_query_result = class_obj_query.find()
    if class_obj_query_result == []:
        return ''
    else:
        Formated_Message = Format_Message(class_obj_query_result[-1].get('createdAt'),class_obj_query_result[-1].get('Username'),class_obj_query_result[-1].get('Message'))
        if Formated_Message != OldMessage:
            return Formated_Message
        else:
            return ''
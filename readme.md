# School Mail

为比赛而生。

## 简介

即时通讯软件，为班级而作，为比赛而生。

## 特性

1. 支持创建/加入聊天室
2. 不需要服务器（因为用到的是LeanCloud的服务器）
3. 支持后台同步信息~~（还没做呢，不要急，还没到比赛时间）~~

## 部署

### Leancloud部署

> 懒得打字，直接照抄Waline的算了

1. [登录](https://console.leancloud.app/login) 或 [注册](https://console.leancloud.app/register) `LeanCloud 国际版` 并进入 [控制台](https://console.leancloud.app/apps)

2. 点击左上角 [创建应用](https://console.leancloud.app/apps) 并起一个你喜欢的名字 (请选择免费的开发版):

   ![创建应用](https://waline.js.org/assets/leancloud-1.f7a36b20.png)

3. 进入应用，选择左下角的 `设置` > `应用 Key`。你可以看到你的 `APP ID`,`APP Key` 和 `Master Key`。请记录它们，以便后续使用。

   ![ID 和 Key](https://waline.js.org/assets/leancloud-2.4cc69975.png)

#### 国内版注意事项

> 备用，哪时用不了看这里

如果你正在使用 Leancloud 国内版 ([leancloud.cn](https://leancloud.cn/))，我们推荐你切换到国际版 ([leancloud.app](https://leancloud.app/))。否则，你需要为应用额外绑定**已备案**的域名，同时购买独立 IP 并完成备案接入:

- 登录国内版并进入需要使用的应用
- 选择 `设置` > `域名绑定` > `API 访问域名` > `绑定新域名` > 输入域名 > `确定`。
- 按照页面上的提示按要求在 DNS 上完成 CNAME 解析。
- 购买独立 IP 并提交工单完成备案接入。(独立 IP 目前价格为 ￥ 50/个/月)

![域名设置](https://waline.js.org/assets/leancloud-3.3ae5fb8d.png)

### 客户端部署

从[Release](https://github.com/WhitemuTeam/School-Mail/release)中下载最新版本后解压

在程序目录下新建`data`文件夹，在`data`文件夹下新建`leancloud.json`文件并打开，输入:

```Json
{
    "AppID":"输入你得到的AppID",
    "AppKey":"输入你得到的AppKey"
}
```

保存后退出，运行School-Mail.exe运行即可正常使用

### 从源码运行

你需要Python 3.x环境

Clone此仓库并在仓库文件夹打开终端，输入以下指令以安装依赖:

```
pip install -r requirements.txt
```

其他与上节一致

## 注意事项

没有，注意不要大势传播，不然有损名气。
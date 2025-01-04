# 星渊电报助手 (TG Aide)

[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)
[![PagerMaid](https://img.shields.io/badge/PagerMaid--Pyro-Plugin-blueviolet.svg)](https://github.com/TeamPGM/PagerMaid-Pyro)

一个功能丰富的 PagerMaid-Pyro 插件，为您的 Telegram 体验带来更多便利。

## 功能特点

### 🌍 翻译功能
- 支持全局翻译开关
- 独立群组/个人翻译设置
- 自定义源语言和目标语言
- 基于 DeepLX API 的高质量翻译

### 👥 群组管理
- 一键通知所有管理员
- 批量删除自身消息
- 群成员管理(清理群成员)
  - 清理长期未上线成员
  - 清理长期未发言成员
  - 清理发言数过少成员
  - 清理已注销账号
  - 清理全部成员

### 💳 支付功能
- USDT 收款地址设置
- 便携式收款二维码生成
- 订单号自动生成与加密

### 🔍 查询功能
- 群组/用户详细信息查询
- 数据中心(DC)分布查询
- 聊天记录关键词搜索
- 程序变量调试查看

### ⚙️ 系统功能
- 自动更新检测
- Web API 服务
- 动态时间显示
- 消息复读功能

### 🤖 其他功能
- 索敌功能
- 自定义文本发送
- 持续在线功能

## 安装要求

- Python 3.7+
- PagerMaid-Pyro 框架
- 必要的 Python 依赖包：
  - emoji
  - qrcode
  - aiohttp
  - PIL (Pillow)

## 安装方法

1. 确保已安装 PagerMaid-Pyro 框架
2. 下载 `tgaide.py` 文件
3. 将文件放入 PagerMaid-Pyro 的 plugins 目录
4. 重启 PagerMaid-Pyro 或使用 `,reload` 命令加载插件

## 使用方法

### 基础命令
- `,aide` - 显示主菜单
- `,aide 翻译` - 显示翻译菜单
- `,aide 索敌` - 显示索敌菜单
- `,aide 助手` - 显示个人助手菜单
- `,aide 时间` - 显示动态时间菜单
- `,aide api` - 显示 API 功能菜单
- `,aide 系统` - 显示系统命令菜单

### 翻译命令
- `,fyall` - 开启/关闭全局翻译
- `,fyit` - 设置独立群组/个人翻译状态
- `,fyset <源语言> <目标语言>` - 设置翻译语言
- `,fy <文本>` - 翻译指定文本

### 群组管理命令
- `,admins <留言>` - 通知群组管理员
- `,dmy <条数>` - 删除自身消息
- `,mg` - 群成员管理

### 查询命令
- `,info <模式>` - 查询详细信息
- `,dcx` - 查看数据中心分布
- `,query <关键词> [搜索条数]` - 搜索聊天记录

### 系统命令
- `,aideup` - 手动更新版本
- `,http <模式> [参数]` - 操作 API 服务

## Web API 使用说明

API 服务提供了消息发送功能，可通过以下 URL 调用：

```
http://<IP地址>:<端口号>/?key=<秘钥>&mode=1&id=<目标ID>&msg=<发送的消息>
```

### API 参数说明
- `key`: 访问秘钥
- `mode`: 操作模式(1: 发送消息)
- `id`: 目标用户/群组 ID
- `msg`: 要发送的消息内容

## 配置文件

插件使用 `tgaide.json` 作为配置文件，包含以下设置：

```json
{
    "version": "1.2.2.0000",
    "online": 1,
    "nametime": 0,
    "webport": 6868,
    "webkey": "admin",
    "usdtaddress": "YOUR_USDT_ADDRESS",
    "global_translate_enabled": false,
    "from_lang": "zh",
    "to_lang": "en",
    "translate_id": []
}
```

## 注意事项

1. 部分功能需要管理员权限
2. API 服务的秘钥请妥善保管
3. 使用翻译功能时请注意 API 调用频率
4. 群成员管理功能请谨慎使用

## 开源协议

本项目采用 GPL-3.0 协议开源。

## 鸣谢

- PagerMaid-Pyro 开发团队
- DeepLX API 服务
- 所有贡献者和用户

## 联系方式

- 作者：@drstth
- 群组：@tgaide
- 频道：@tgaide_channel

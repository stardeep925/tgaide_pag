# 🌟 星渊电报助手 (TG Aide)

[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)
[![PagerMaid](https://img.shields.io/badge/PagerMaid--Pyro-Plugin-blueviolet.svg)](https://github.com/TeamPGM/PagerMaid-Pyro)
[![Version](https://img.shields.io/badge/version-1.2.2-green.svg)](https://github.com/TeamPGM/PagerMaid-Pyro)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)

> 🚀 一个功能丰富的 PagerMaid-Pyro 插件，为您的 Telegram 体验带来更多便利。

---

## ✨ 功能特点

### 🌍 翻译功能
- 🔄 支持全局翻译开关
- 🎯 独立群组/个人翻译设置
- 🔤 自定义源语言和目标语言
- 🎨 基于 DeepLX API 的高质量翻译
- 📝 支持多种语言互译
- 🔁 自动识别语言类型

### 👥 群组管理
- 📢 一键通知所有管理员
- 🗑️ 批量删除自身消息
- 👮 群成员管理(清理群成员)
  - 💤 清理长期未上线成员
  - 🤐 清理长期未发言成员
  - 📉 清理发言数过少成员
  - 👻 清理已注销账号
  - 🧹 清理全部成员
- 📊 成员数据统计分析

### 💳 支付功能
- 💰 USDT 收款地址设置
- 📱 便携式收款二维码生成
- 🔐 订单号自动生成与加密
- 🎨 美观的收款界面设计
- 📋 交易记录自动保存

### 🔍 查询功能
- ℹ️ 群组/用户详细信息查询
- 🌐 数据中心(DC)分布查询
- 🔎 聊天记录关键词搜索
- 🐛 程序变量调试查看
- 📈 使用数据统计

### ⚙️ 系统功能
- 🔄 自动更新检测
- 🌐 Web API 服务
- 🕒 动态时间显示
- 🔁 消息复读功能
- 📡 在线状态维护

### 🤖 其他功能
- 🎯 索敌功能
- 📝 自定义文本发送
- 🟢 持续在线功能
- 🔔 消息通知管理
- 🎮 交互式命令界面

**警告，后续功能不会在md文件更新了，具体功能列表请安装最新插件使用，aide查看菜单**
## 🛠️ 安装要求

### 系统环境
- 💻 Python 3.7+
- 🔧 PagerMaid-Pyro 框架
- 🌐 稳定的网络连接

### 📦 必要的 Python 依赖包
```bash
pip install -r requirements.txt
```
- 🎨 emoji~=2.2.0
- 📱 qrcode~=7.3.1
- 🌐 aiohttp~=3.8.4
- 🖼️ Pillow~=9.5.0
- 🔄 pyrogram~=2.0.106

## 📥 安装方法
   **以下内容请忽略，新版本已做到全自动安装**
1. 📥 克隆仓库或下载插件
```bash
git clone https://github.com/your-username/tgaide.git
```

2. 📁 安装依赖
```bash
cd tgaide
pip install -r requirements.txt
```

3. 🔧 配置插件
```bash
cp config.example.json config.json
nano config.json  # 编辑配置文件
```

4. 🚀 启动使用
```bash
# 将插件放入 PagerMaid-Pyro 的 plugins 目录
cp tgaide.py ~/pagermaid/plugins/
# 重载插件
,reload tgaide

   **以上内容请忽略，新版本已做到全自动安装**
```

## 📚 使用方法

### 🎮 基础命令
| 命令 | 描述 | 参数说明 |
|------|------|----------|
| `,aide` | 📋 显示主菜单 | - |
| `,aide 翻译` | 🌍 显示翻译菜单 | - |
| `,aide 索敌` | 🎯 显示索敌菜单 | - |
| `,aide 助手` | 🤖 显示个人助手菜单 | - |
| `,aide 时间` | ⏰ 显示动态时间菜单 | - |
| `,aide api` | 🔌 显示 API 功能菜单 | - |
| `,aide 系统` | ⚙️ 显示系统命令菜单 | - |

### 🌍 翻译功能详解
| 命令 | 描述 | 参数说明 | 示例 |
|------|------|----------|------|
| `,fyall` | 🔄 开启/关闭全局翻译 | 无需参数 | `,fyall` |
| `,fyit` | 🎯 设置独立翻译状态 | 无需参数，在目标群组/私聊中使用 | `,fyit` |
| `,fyset` | 🔤 设置翻译语言 | `<源语言> <目标语言>` | `,fyset zh en` |
| `,fy` | 📝 翻译指定文本 | `<文本>` | `,fy 你好世界` |

**支持的语言代码：**
- 🇨🇳 中文: `zh`
- 🇺🇸 英语: `en`
- 🇯🇵 日语: `ja`
- 🇰🇷 韩语: `ko`
- 🇷🇺 俄语: `ru`
- 🇫🇷 法语: `fr`
- 🇩🇪 德语: `de`
- 更多语言请参考 DeepL API 文档

### 👥 群组管理详解
| 命令 | 描述 | 参数说明 | 示例 |
|------|------|----------|------|
| `,admins` | 📢 通知管理员 | `[留言]` | `,admins 请查看置顶消息` |
| `,dmy` | 🗑️ 删除自身消息 | `<数量>` | `,dmy 10` |
| `,mg` | 👮 群成员管理 | 交互式操作 | `,mg` |
| `,info` | ℹ️ 查询信息 | `<all/me/u>` | `,info all` |
| `,dcx` | 🌐 查询DC | `[force]` | `,dcx` |
| `,query` | 🔍 搜索消息 | `<关键词> [数量]` | `,query 公告 50` |

### ⚡ 索敌功能详解
| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `,sd on` | 🎯 开启索敌 | 需回复目标消息 | `,sd on` |
| `,sd off` | 🛑 关闭索敌 | 无需参数 | `,sd off` |

### 💳 支付功能详解
| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `,usdtset` | 💰 设置USDT地址 | `<地址>` | `,usdtset TRxxxxx` |
| `,jy` | 📲 发起交易 | `<金额>` | `,jy 100` |

### ⏰ 动态时间功能
| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `,aidetime name` | 🕒 开关动态时间 | - | `,aidetime name` |
| `,aidetime set` | 🔄 设置在线状态 | - | `,aidetime set` |
| `,aidetime mode` | 🔀 切换显示模式 | - | `,aidetime mode` |
| `,timetxt` | 📝 设置随机文本 | `[文本]` | `,timetxt 在线中-摸鱼中` |

### 🔌 API功能详解
| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `,http start` | 🚀 启动API服务 | - | `,http start` |
| `,http stop` | 🛑 停止API服务 | - | `,http stop` |
| `,http port` | 🔌 设置端口 | `<端口>` | `,http port 8080` |
| `,http key` | 🔑 设置密钥 | `<密钥>` | `,http key abc123` |

### 🛠️ 系统功能详解
| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `,aideup` | 🔄 更新插件 | - | `,aideup` |
| `,sent` | 📤 发送文本 | `<文本>` | `,sent Hello` |
| `,rex` | 🔁 复读消息 | `[次数]` | `,rex 3` |
| `,debug` | 🐛 调试信息 | - | `,debug` |

## 📊 功能场景示例

### 🌍 翻译场景
```plaintext
# 设置中译英
,fyset zh en

# 翻译单条消息
,fy 你好世界

# 开启全局翻译
,fyall

# 设置特定群组翻译
,fyit
```

### 👥 群管场景
```plaintext
# 清理群成员
1. 输入 ,mg
2. 选择清理模式(1-5)
3. 设置条件(天数/发言数)
4. 选择操作(查找/清理)

# 批量删除消息
,dmy 50  # 删除最近50条自己的消息

# 通知所有管理员
,admins 请查看最新公告
```

### 💳 收款场景
```plaintext
# 设置USDT地址
,usdtset TRWxxxxxxxxxxxxxxxxxxxxxxxxSTAR

# 发起收款
1. 回复用户消息
2. 输入 ,jy 100
3. 生成带有二维码的收款信息
```

### ⏰ 动态时间场景
```plaintext
# 设置动态时间显示
1. ,aidetime name  # 开启功能
2. ,timetxt 在线中-工作中-摸鱼中  # 设置显示文本
3. ,aidetime mode  # 切换显示模式
```

## 🔧 高级功能

### 🤖 自动化功能
- 自动更新检测
- 自动维护在线状态
- 自动保存交易记录
- 自动清理失效消息

### 🎨 界面定制
- 支持自定义收款界面
- 可配置动态时间显示
- 可自定义翻译显示格式
- 支持多种提示样式

### 🔐 安全特性
- API访问鉴权
- 管理员权限验证
- 操作日志记录
- 敏感信息加密

### 📊 数据统计
- 群组活跃度分析
- 成员互动统计
- 命令使用频率
- 系统资源监控

## 🌐 Web API 使用说明

### 📡 API 接口
```http
GET http://<IP地址>:<端口号>/?key=<秘钥>&mode=1&id=<目标ID>&msg=<发送的消息>
```

### 📝 请求参数
| 参数 | 类型 | 描述 |
|------|------|------|
| `key` | string | 🔑 访问秘钥 |
| `mode` | int | 📊 操作模式 |
| `id` | string | 👤 目标ID |
| `msg` | string | 📨 消息内容 |

### 📤 响应示例
```json
{
    "status": "success",
    "msg": "Message sent successfully"
}
```

## ⚙️ 配置文件

### 📁 配置示例 (tgaide.json)
```json
{
    "version": "1.2.2.0000",
    "online": 1,
    "nametime": 0,
    "webport": 6868,
    "webkey": "your_secure_key_here",
    "usdtaddress": "YOUR_USDT_ADDRESS",
    "global_translate_enabled": false,
    "from_lang": "zh",
    "to_lang": "en",
    "translate_id": []
}
```

## ⚠️ 注意事项

1. 🔒 **安全性**
   - 妥善保管 API 密钥
   - 定期更换访问密码
   - 注意权限管理

2. 💻 **性能**
   - 合理设置清理间隔
   - 避免频繁 API 调用
   - 注意内存使用

3. 🔧 **维护**
   - 定期检查更新
   - 备份重要数据
   - 监控运行状态

4. 📝 **使用建议**
   - 遵守 Telegram 政策
   - 合理使用群管功能
   - 注意用户隐私

## 📄 开源协议

本项目采用 [GPL-3.0](LICENSE) 协议开源。

## 🙏 鸣谢

- 🏆 [PagerMaid-Pyro](https://github.com/TeamPGM/PagerMaid-Pyro) 开发团队
- 🌐 [DeepLX API](https://www.deepl.com/) 服务
- 👥 所有贡献者和用户

## 📞 联系方式

- 👨‍💻 作者：[@drstth](https://t.me/drstth)
- 👥 群组：[@tgaide](https://t.me/tgaide)
- 📢 频道：[@tgaide_channel](https://t.me/tgaide_channel)

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. 🔀 Fork 本仓库
2. 🔨 创建特性分支
3. ✏️ 提交更改
4. 🔄 推送到分支
5. 📬 提交 Pull Request

## 📈 更新日志

懒得写了：D
---

> 📌 **提示：** 使用过程中如有问题，欢迎在 Telegram 群组中交流讨论！

## 📱 功能特性详解

### 🔄 自动化处理
- **消息自动翻译**
  ```plaintext
  # 全局翻译模式下：
  1. 自动翻译所有发出的消息
  2. 自动识别源语言
  3. 支持多语言互译
  ```
- **在线状态维护**
  ```plaintext
  # 自动保持在线
  1. 每55秒自动更新状态
  2. 支持自定义在线/离线状态
  3. 断线自动重连
  ```
- **自动更新系统**
  ```plaintext
  # 版本检查流程
  1. 定期检查新版本
  2. 自动下载更新文件
  3. 智能安装部署
  ```

### 🎨 UI/UX 设计
- **收款界面美化**
  ```plaintext
  特性：
  - 渐变背景设计
  - 自适应布局
  - 高清二维码生成
  - 自定义LOGO支持
  ```
- **动态时间显示**
  ```plaintext
  样式：
  - emoji时钟显示
  - 自定义状态文本
  - 多种显示模式
  ```
- **消息样式**
  ```plaintext
  格式：
  - HTML格式支持
  - Markdown格式支持
  - 自定义表情包
  ```

### 🔍 搜索与查询
- **高级搜索功能**
  ```plaintext
  支持：
  - 模糊搜索
  - 正则匹配
  - 多条件筛选
  - 结果分页
  ```
- **用户信息查询**
  ```plaintext
  可查询：
  - 基础信息
  - DC信息
  - 共同群组
  - 在线状态
  ```
- **群组数据分析**
  ```plaintext
  统计：
  - 成员活跃度
  - 消息频率
  - DC分布
  - 管理员列表
  ```

### 🛡️ 安全防护
- **API 安全**
  ```plaintext
  措施：
  - 密钥验证
  - 请求限流
  - IP白名单
  - 日志记录
  ```
- **权限管理**
  ```plaintext
  级别：
  - 超级管理员
  - 普通管理员
  - 受信任用户
  - 普通用户
  ```
- **数据保护**
  ```plaintext
  方式：
  - 配置文件加密
  - 敏感信息脱敏
  - 定期数据备份
  ```

## 🔧 进阶配置

### 📊 性能优化
```json
{
    "performance": {
        "max_concurrent_tasks": 10,
        "message_cache_size": 1000,
        "auto_clean_interval": 3600,
        "api_timeout": 30
    }
}
```

### 🌐 网络设置
```json
{
    "network": {
        "proxy_enabled": false,
        "proxy_type": "socks5",
        "proxy_address": "127.0.0.1",
        "proxy_port": 1080,
        "api_retry_count": 3
    }
}
```

### 🔐 安全配置
```json
{
    "security": {
        "api_rate_limit": 100,
        "allowed_ips": ["127.0.0.1"],
        "admin_users": ["user_id_1", "user_id_2"],
        "log_level": "INFO"
    }
}
```

## 📈 性能指标

### 🚀 响应速度
- 消息处理: < 100ms
- API 响应: < 200ms
- 搜索查询: < 500ms
- 文件处理: < 1s

### 💾 资源占用
- CPU: 5-10%
- 内存: 50-100MB
- 存储: 10-50MB
- 网络: 1-5MB/s

### 🌐 并发处理
- 最大并发请求: 100/s
- 消息队列容量: 1000
- 最大连接数: 500
- 缓存容量: 10000条

## 🔨 故障排除

### 🚫 常见问题
1. **API 连接失败**
   ```plaintext
   解决方案：
   1. 检查网络连接
   2. 验证API密钥
   3. 确认服务器状态
   ```

2. **翻译功能异常**
   ```plaintext
   解决方案：
   1. 检查语言代码
   2. 验证API额度
   3. 重置翻译设置
   ```

3. **内存占用过高**
   ```plaintext
   解决方案：
   1. 清理消息缓存
   2. 减少并发任务
   3. 优化查询操作
   ```

### 🔍 诊断命令
```plaintext
,debug         # 查看系统状态
,aideup        # 检查更新
,http status   # 检查API状态
```

## 📚 开发文档

### 🔌 API 开发
```python
# API 调用示例
import requests

def send_message(api_key, chat_id, message):
    url = f"http://your-server:port/"
    params = {
        "key": api_key,
        "mode": 1,
        "id": chat_id,
        "msg": message
    }
    response = requests.get(url, params=params)
    return response.json()
```

### 🛠️ 插件开发
```python
# 插件模板
@listener(command="custom_command")
async def custom_function(message: Message):
    """
    自定义功能实现
    """
    try:
        # 实现逻辑
        pass
    except Exception as e:
        await message.edit(f"错误：{str(e)}")
```

### 📦 模块扩展
```python
# 扩展模块示例
class CustomModule:
    def __init__(self):
        self.config = {}
    
    async def initialize(self):
        # 初始化逻辑
        pass
    
    async def process(self, data):
        # 处理逻辑
        pass
```

## 🎯 最佳实践

### 💡 使用建议
1. **配置优化**
   - 根据服务器配置调整并发数
   - 定期清理缓存数据
   - 使用CDN加速API访问

2. **安全防护**
   - 定期更换API密钥
   - 启用IP白名单
   - 监控异常访问

3. **性能调优**
   - 使用连接池
   - 实现请求缓存
   - 优化查询语句

### 🚀 部署建议
1. **环境配置**
   ```bash
   # 推荐配置
   Python 3.8+
   RAM 2GB+
   Storage 20GB+
   Network 10Mbps+
   ```

2. **依赖管理**
   ```bash
   # 创建虚拟环境
   python -m venv venv
   source venv/bin/activate
   
   # 安装依赖
   pip install -r requirements.txt
   **以上内容请忽略，新版本已做到全自动安装**
   ```

3. **监控配置**
   ```bash
   # 推荐监控指标
   - CPU使用率
   - 内存占用
   - API响应时间
   - 错误日志
   ```

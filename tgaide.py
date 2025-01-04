try:
    # 尝试导入1.5.0新版本的模块
    from pagermaid.listener import listener, _lock
    from pagermaid.utils import client, edit_delete, Message, lang, pip_install
    from pagermaid.enums import Client, Message
    from pagermaid import log, read_context, logs, scheduler, bot
    from pyrogram import filters
    from pyrogram.errors import (
        ChatAdminRequired,
        UserAdminInvalid,
        PeerIdInvalid,
        BadRequest,
        FloodWait
    )
    from pyrogram.enums import ChatMemberStatus, ChatType
    from random import uniform
    from asyncio import sleep
    from pyrogram.enums import ChatMemberStatus
except ImportError:
    # 如果导入失败则回退到旧版本的导入路径
    from pagermaid.listener import listener, _lock
    from pagermaid.utils.bot_utils import edit_delete, logs, log
    from pagermaid.enums import Client, Message
    from pagermaid.services import client, scheduler, bot
    from pagermaid.utils import lang, pip_install
    from pyrogram import filters
    from pyrogram.errors import (
        ChatAdminRequired,
        UserAdminInvalid,
        PeerIdInvalid,
        BadRequest,
        FloodWait
    )
from pyrogram.enums import ChatMemberStatus
from pagermaid.static import read_context
from pyrogram.enums import ChatMembersFilter
import contextlib
from contextlib import suppress
import base64
import sys
import os
from urllib.parse import urlparse, parse_qs
import json
from asyncio import sleep
import subprocess
import asyncio
from io import StringIO
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import urllib.request
from pyrogram.raw.functions.account import UpdateStatus
import random
import traceback
from random import uniform
from datetime import datetime, timedelta, timezone

try:
    from emoji import emojize
    import qrcode
    import aiohttp
    from PIL import Image, ImageDraw, ImageFont
except Exception as e:
    print(f"捕获到异常: {e}")

"""
星渊电报助手
V1.2.2.0000版本
作者：@drstth
群组：@tgaide
频道：@tgaide_channel
本插件目前为止全部免费全部开源！禁止倒卖等收费！如果您是买的那么证明您被骗了！
可以基于自己的喜爱进行二次创作，但是请不要拿着我的代码二改然后卖钱！
声明：
admins函数代码基于官方插件库中“atadmins”插件修改
dmy函数基于官方自带的dme函数修改
持续在线模块基于官方插件库中keep_online插件修改
dcx函数参考了dc插件进行编写
mg函数基于clean_member插件进行修改
"""
#依赖安装器
def install_if_missing(package_name):
    try:
        __import__(package_name)
        print(f"{package_name} 已经安装。")
    except ImportError:
        print(f"未找到 {package_name}，正在安装...")
        try:
            # 检测是否在虚拟环境中
            if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
                print("当前环境为enev环境")
                subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
            else:
                # 检测是否在容器中
                if os.path.exists('/.dockerenv'):
                    print("当前环境为容器环境")
                    subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
                else:
                    # 正常环境
                    try:
                        print("当前环境为正常环境")
                        subprocess.run([sys.executable, "-m", "pip3", "install", package_name], check=True)
                    except subprocess.CalledProcessError:
                        subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
            print(f"{package_name} 已安装。")
        except subprocess.CalledProcessError as e:
            print(f"安装 {package_name} 失败：{e}")
        except Exception as e:
            print(f"未知错误：{e}")

####################################################################
#初始化
from_lang = "zh"
to_lang = "en"
global_translate_enabled = False
version = "1.2.2.0000"
listened_user_id = None

print("当前运行目录:", os.getcwd())

install_if_missing("emoji")#用于动态名称显示的时间emoji
install_if_missing("qrcode")#便携收款二维码画布生成二维码的依赖库
install_if_missing("aiohttp")#用于翻译api对接
files = {
    "usdtico.png": "https://tgaide.a1aa.cn/usdtico.png",#便携收款二维码画布使用的usdt图标文件
    "ys.ttf": "https://tgaide.a1aa.cn/ys.ttf"#便携收款二维码画布使用的字体文件，可修改你喜欢的字体
}

#资源文件下载函数
def download_file(url, filename):
    with urllib.request.urlopen(url) as response:
        with open(filename, 'wb') as f:
            f.write(response.read())

def check_and_download_files():
    for filename, url in files.items():
        if not os.path.exists(filename):
            print(f"{filename} 不存在，正在下载...")
            download_file(url, filename)
            print(f"{filename} 下载完成。")
        else:
            print(f"{filename} 已经存在。")
            
check_and_download_files()

default_settings = {
    "version": version,
    "online": 1,
    "nametime": 0,
    "webport": 6868,
    "webkey": "admin",
    "usdtaddress": "TRWD5R64VxFC2z2WXtR6CTbqt26688STAR",
    "global_translate_enabled": False,
    "from_lang": from_lang,
    "to_lang": to_lang,
    "translate_id":[]
}


if not os.path.exists("tgaide.json"):
    with open("tgaide.json", "w") as file:
        json.dump(default_settings, file, indent=4)
    print("文件不存在，已创建新文件并设置了默认值。")
else:
    try:
        with open("tgaide.json", "r") as file:
            settings = json.load(file)
    except (IOError, ValueError) as e:
        print(f"加载json设置失败: {e}")
        settings = {}


    for key, value in default_settings.items():
        settings.setdefault(key, value)

    try:
        with open("tgaide.json", "w") as file:
            json.dump(settings, file, indent=4)
    except (IOError, ValueError) as e:
        print(f"更新设置失败: {e}")


file_path = os.path.join(os.getcwd(), 'tgaide.json')

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if 'global_translate_enabled' in data:
            global_translate_enabled = data['global_translate_enabled']
except FileNotFoundError:
    print(f"文件 {file_path} 未找到。")
except json.JSONDecodeError:
    print(f"文件 {file_path} 不是有效的 JSON 文件。")


print(f"global_translate_enabled 已更新为: {global_translate_enabled}")

#初始化
####################################################################


#更新系列函数

# 版本号检测
def compare_versions(version1, version2):
    v1 = [int(v) for v in version1.split(".")]
    v2 = [int(v) for v in version2.split(".")]
    for i in range(max(len(v1), len(v2))):
        v1_val = v1[i] if i < len(v1) else 0
        v2_val = v2[i] if i < len(v2) else 0
        if v1_val > v2_val:
            return 1
        if v1_val < v2_val:
            return -1
    return 0


# 更新检测
def update_aide_one(version):
    try:
        response = urllib.request.urlopen("https://tgaide.a1aa.cn/version.txt")
        remote_version = response.read().decode('utf-8').strip()

        if compare_versions(remote_version, version) > 0:
            print(f"发现新版本：{remote_version}，当前版本：{version}。开始更新...")

            update_script_url = "https://tgaide.a1aa.cn/update.sh"
            script_response = urllib.request.urlopen(update_script_url)
            update_script_path = "aide_update.sh"
            with open(update_script_path, "wb") as file:
                file.write(script_response.read())

            subprocess.run(["chmod", "777", update_script_path])
            subprocess.run(["bash", update_script_path])
        else:
            print("当前已是最新版本。")

    except Exception as e:
        print(f"更新检查失败：{e}")


update_aide_one(version)


# 自动更新
async def fetch(url):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, urllib.request.urlopen, url)
    response = await future
    return response.read().decode('utf-8')


async def update_aide(message, version):
    try:
        remote_version = (await fetch("https://tgaide.a1aa.cn/version.txt")).strip()

        if compare_versions(remote_version, version) > 0:
            await message.edit(f"发现新版本：{remote_version}，当前版本：{version}。开始更新...")

            update_script = await fetch("https://tgaide.a1aa.cn/update.sh")
            update_script_path = "aide_update.sh"
            with open(update_script_path, "wb") as file:
                file.write(update_script.encode())

            subprocess.run(["chmod", "777", update_script_path])
            subprocess.run(["bash", update_script_path])

            await message.edit("更新成功!请重载插件完成更新<code>,reload</code>")
        else:
            await message.edit("当前已是最新版本。")

    except Exception as e:
        await edit_delete(message, f"更新检查失败：{e}")


# 手动更新
@listener(command="aideup", description="更新助手")
async def aideup(message):
    global version
    await update_aide(message, version)

#更新系列函数
####################################################################

# 菜单
@listener(command="aide", description="显示主菜单或二级菜单", parameters="[二级菜单名称]")
async def aide(message: Message):
    submenu_name = message.arguments.strip()
    main_menu_text = f'''
    👮 **星渊电报助手主菜单** 👮
    ——————————————
    🗺️ **翻译菜单** 【<code>,aide 翻译</code>】
    🖕 **索敌菜单** 【<code>,aide 索敌</code>】
    🛠 **个人助手** 【<code>,aide 助手</code>】
    🕘 **动态时间** 【<code>,aide 时间</code>】
    📡 **API功能** 【<code>,aide api</code>】
    ⚙ **系统命令** 【<code>,aide 系统</code>】
    ——————————————
    © 当前版本：{version}
    🧑‍💻 **[作者](tg://user?id=5405984571)** | 👪 **[群组](https://t.me/tgaide)** | 🗣 **[频道](https://t.me/tgaide_channel)**
    '''

    submenu_texts = {
        "翻译": '''
    🗺️ **翻译主菜单** 🗺️
    ——————————————
    【<code>,fyall</code>】 开启/关闭全局翻译
    【<code>,fyit</code>】 设置独立群组/个人翻译状态
    【<code>,fyset <源语言> <目标语言></code>】 设置翻译语言
    【<code>,fy <源语言></code>】 翻译文本
    ——————————————
    **使用说明：**
    - **,fyall** ：开启或关闭全局翻译功能。
    - **,fyit** ：设置某群组或个人的翻译状态，仅在全局翻译关闭时有效。
    - **,fyset** ：指定源语言和目标语言。
    - **,fy** ：对指定文本进行翻译。
    ''',

        "索敌": '''
    🖕 **索敌主菜单** 🖕
    ——————————————
    【<code>,sd <on/off></code>】 启用/关闭索敌功能（需回复消息）
    ——————————————
    **使用说明：**
    - **,sd on** ：开启索敌功能。
    - **,sd off** ：关闭索敌功能。
    ''',

        "系统": '''
    ⚙ **系统主菜单** ⚙
    ——————————————
    【<code>,aideup</code>】 手动更新版本
    【<code>,sent</code>】 发送文本（支持Markdown/HTML格式）
    ——————————————
    **使用说明：**
    - **,aideup** ：手动触发版本更新。
    - **,sent** ：发送文本消息，支持Markdown和HTML格式。
    ''',

        "助手": '''
    🛠 **助手主菜单** 🛠
    ——————————————
    【<code>,admins <留言></code>】 通知群组管理员（匿名）
    【<code>,dmy <条数></code>】 删除自身消息
    【<code>,info <模式></code>】 查询详细信息
    【<code>,usdtset <地址></code>】 设置USDT地址
    【<code>,jy <金额></code>】 发起便捷交易（需回复用户）
    【<code>,query <关键词> [搜索条数]</code>】 通过关键词查找聊天记录
    【<code>,dcx</code>】 查看本群数据中心分布，回复用户则显示该用户dc
    【<code>,rex</code>】 与re命令一致，但不是转发消息，而是重新发送
    【<code>,mg</code>】 群成员管理(清理群成员)
    【<code>,debug</code>】 查看所有变量及其值（用于调试）
    ——————————————
    **使用说明：**
    - **,admins <留言>** ：通知群组所有管理员，可选留言内容。
    - **,dmy <条数>** ：删除自己的历史消息，指定删除条数。
    - **,info <模式>** ：查询详细信息：
      - **all** ：查询全部信息。
      - **me** ：查询自己的信息。
      - **u** ：查询回复对象的信息。
    - **,jy <金额>** ：发起交易，需回复目标用户。
    - **,query <关键词> [搜索条数]** ：通过关键词查找聊天记录，默认为30条。
    ''',

        "时间": '''
    🕘 **动态时间主菜单** 🕘
    ——————————————
    【<code>,aidetime <参数></code>】 设置动态时间功能
    【<code>,timetxt <文本></code>】 配置随机文本模式
    ——————————————
    **使用说明：**
    - **,aidetime <参数>** ：
      - **name** ：开启或关闭动态时间功能。
      - **set** ：设置为在线或离线状态。
      - **mode** ：切换为随机文本或状态模式。
    - **,timetxt <文本>** ：查看或设置随机文本内容，以“-”分隔不同文本。
    ''',

        "api": '''
    📡 **API服务主菜单** 📡
    ——————————————
    【<code>,http <模式> [参数]</code>】 操作API服务
    ——————————————
    **API使用教程：**
    1. 使用 **<code>,http start</code>** 开启API服务。
    2. 访问以下URL调用API：
       ```
       http://<你的IP地址>:<端口号>/?key=<秘钥>&mode=1&id=<目标ID>&msg=<发送的消息>
       ```
    **参数说明：**
    - **模式** ：
      - **start/stop** ：开启或关闭API服务。
      - **port <端口号>** ：设置服务端口。
      - **key <秘钥>** ：设置访问秘钥。
    '''
    }
    if submenu_name:
        if submenu_name in submenu_texts:
            await message.edit(submenu_texts[submenu_name])
        else:
            await message.edit(f"<b>未找到名为“{submenu_name}”的菜单！</b>")
    else:
        await message.edit(main_menu_text)

    #await asyncio.sleep(60)
    #await message.delete() 菜单自动删除代码，有需要自行解除注释

#索敌开关
@listener(is_plugin=True, outgoing=True, command="sd",
          description="开启或关闭索敌用户",
          parameters="<on/off>")
async def manage_listening(message: Message):
    global listened_user_id

    command_arg = message.arguments.strip().lower()
    
    if command_arg == "on":
        if not message.reply_to_message:
            return await message.edit("请通过回复用户的消息来使用此命令！")

        listened_user_id = message.reply_to_message.from_user.id
        await message.edit(f"{listened_user_id} 开始索敌")

    elif command_arg == "off":
        if listened_user_id is None:
            return await message.edit("当前没有索敌的用户！")

        listened_user_id = None
        await message.edit("已停止索敌")

    else:
        await message.edit("无效的参数！请使用 'sd on' 或 'sd off'。")

    await asyncio.sleep(10)
    await message.delete()


# 索敌监听
@listener(incoming=True)
async def reply_to_listened_user(message: Message):
    global listened_user_id
    if message.from_user is None or listened_user_id is None or message.from_user.id != listened_user_id:
        return
    
    username = message.from_user.username

    async def fetch(url):
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, urllib.request.urlopen, url)
        response = await future
        return response.read().decode('utf-8')

    try:
        sd_content = await fetch("https://yyapi.a1aa.cn/api.php?level=max")
        if username:
            await message.reply(f"@{username} <b>{sd_content}</b>")
        else:
            await message.reply(f"<b>{sd_content}</b>")
    except Exception as e:
        print(f"错误: {e}")



# 发送
@listener(command="sent", description="将传入的文本以原始信息发送出来", parameters="<字符>")
async def sent(message: Message):
    text_sent = message.arguments
    if not text_sent:
        await edit_delete(message, "请提供要发送的字符！")
        return
    await bot.send_message(chat_id=message.chat.id, text=text_sent)
    await message.delete()


# 设置翻译
@listener(command="fyset", description="设置翻译语言", parameters="<源语言> <目标语言>")
async def set_translation_languages(message):
    global from_lang, to_lang
    args = message.arguments.split()
    if len(args) != 2:
        await edit_delete(message, "请提供源语言和目标语言！")
        return

    new_from_lang, new_to_lang = args
    try:
        with open("tgaide.json", "r") as file:
            settings = json.load(file)
    except (IOError, ValueError):
        settings = {}
    settings["from_lang"] = new_from_lang
    settings["to_lang"] = new_to_lang
    try:
        with open("tgaide.json", "w") as file:
            json.dump(settings, file)
        await message.edit(f"翻译语言设置为：从{new_from_lang}到{new_to_lang}")
        from_lang = new_from_lang
        to_lang = new_to_lang
    except IOError as e:
        await edit_delete(message, f"保存设置时发生错误：{e}")


# 翻译
@listener(command="fy", description="将您设置的语言翻译至另外一种语言", parameters="<文本>")
async def fy(message: Message):
    text_to_translate = message.arguments
    if not text_to_translate:
        await edit_delete(message, "请提供要翻译的文本！")
        return
    translated_text = await translate_deeplx(text_to_translate)
    await message.edit(f"{translated_text}")


# 全局翻译开关
@listener(command="fyall", description="开启或关闭全局翻译功能")
async def fyall(message):
    global global_translate_enabled
    global_translate_enabled = not global_translate_enabled
    try:
        with open("tgaide.json", "r") as file:
            settings = json.load(file)
    except (IOError, ValueError):
        settings = {}
    settings["global_translate_enabled"] = global_translate_enabled
    try:
        with open("tgaide.json", "w") as file:
            json.dump(settings, file)
        status = "已开启" if global_translate_enabled else "已关闭"
        await message.edit(f"全局翻译功能{status}。")
    except IOError as e:
        await edit_delete(message, f"保存设置时发生错误：{e}")
    
    await asyncio.sleep(10)
    await message.delete()


@listener(command="fyit",
          description="控制独立翻译开关")
async def handle_fyit_command(message: Message):
    chat_id = message.chat.id
    file_path = 'tgaide.json'
    if not os.path.exists(file_path):
        data = {"translate_id": []}
    else:
        with open(file_path, 'r') as file:
            data = json.load(file)

    translate_ids = data.get("translate_id", [])

    if chat_id in translate_ids:
        translate_ids.remove(chat_id)
        action = "关闭"
    else:
        translate_ids.append(chat_id)
        action = "开启"

    data["translate_id"] = translate_ids

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    await message.edit(f"{action} 此ID为 <code>{chat_id}</code> 的群/人独立翻译成功。")
    await asyncio.sleep(10)
    await message.delete()

def get_translate_ids():
    try:
        with open(os.path.join(os.getcwd(), "tgaide.json"), "r") as file:
            data = json.load(file)
            return data.get("translate_id", [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# 全局翻译监听器
@listener(is_group=True, outgoing=True, ignore_edited=True)
async def global_translate(message: Message):

    if not message.text:
        return

    if not global_translate_enabled:
        translate_ids = get_translate_ids()
        if message.chat.id not in translate_ids:
            return

    prefixes = ["，", ",", "/", "-"]

    if any(message.text.startswith(prefix) for prefix in prefixes):
        return

    translated_text = await translate_deeplx(message.text)
    new_text = f"<b>{message.text}</b>\n<blockquote><i>{translated_text}</i></blockquote>"
    await message.edit(new_text)


# deeplx翻译API函数
async def translate_deeplx(text):
    global from_lang
    global to_lang
    url = "https://api.deeplx.org/EaEyeqJu9r6Or7Mpz4ufO2pPYc3MEkqtNN5G2LG1A8k/translate"
    payload = {
        "text": text,
        "source_lang": from_lang,
        "target_lang": to_lang
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status != 200:
                print(f"翻译失败：{response.status}")
                return None

            result = await response.json()
            if result['code'] != 200:
                print(f"翻译失败：{result}")
                return None

            return result['data']


# 代码基于官方插件库atadmins插件效果
@listener(
    command="admins",
    description="一键 AT 本群管理员（仅在群组中有效）",
    groups_only=True,
    parameters="[要说的话]",
)
async def at_admins(client: Client, message: Message):
    admins = []
    async for m in client.get_chat_members(
            message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        if not m.user.is_bot and not m.user.is_deleted:
            admins.append(f"[​​](tg://user?id={m.user.id})")

    if not admins:
        return await message.edit("❌ 没有管理员")

    say = message.arguments or "🔰召唤本群所有管理员"
    send_list = " ".join(admins)

    await client.send_message(
        message.chat.id,
        f"<blockquote>{say}</blockquote>{send_list}",
        reply_to_message_id=message.reply_to_message_id,
        message_thread_id=message.message_thread_id,
    )

    await message.safe_delete()


# 此函数基于官方dme函数修改
@listener(
    is_plugin=False,
    outgoing=True,
    command="dmy",
    need_admin=True,
    description=lang("sp_des_aide"),
    parameters=lang("sp_parameters_aide"),
)
async def self_prune(bot: Client, message: Message):
    msgs = []
    count_buffer = 0
    offset = 0
    if len(message.parameter) != 1:
        if not message.reply_to_message:
            return await message.edit(lang("arg_error"))
        offset = message.reply_to_message.id
    try:
        count = int(message.parameter[0])
        await message.delete()
    except ValueError:
        await message.edit(lang("arg_error"))
        return

    async for msg in bot.get_chat_history(message.chat.id, limit=100):
        if count_buffer == count:
            break
        if msg.from_user and msg.from_user.is_self:
            await attempt_edit_message(bot, msg)
            msgs.append(msg.id)
            count_buffer += 1
            if len(msgs) == 100:
                await bot.delete_messages(message.chat.id, msgs)
                msgs = []

    async for msg in bot.search_messages(
            message.chat.id, from_user="me", offset=offset
    ):
        if count_buffer == count:
            break
        await attempt_edit_message(bot, msg)
        msgs.append(msg.id)
        count_buffer += 1
        if len(msgs) == 100:
            await bot.delete_messages(message.chat.id, msgs)
            msgs = []

    if msgs:
        await bot.delete_messages(message.chat.id, msgs)

    await log(
        f"{lang('prune_hint1')}{lang('sp_hint')} {str(count_buffer)} / {count} {lang('prune_hint2')}"
    )

    with suppress(ValueError):
        notification = await send_prune_notify(bot, message, count_buffer, count)
        await sleep(1)
        await notification.delete()


async def attempt_edit_message(bot: Client, msg: Message):
    try:
        await msg.edit("<code>***此条信息已删除</code>")
    except Exception as e:
        await log(f"Error editing message {msg.id}: {e}")


async def send_prune_notify(bot: Client, message: Message, count_buffer: int, count: int):
    return await bot.send_message(
        message.chat.id,
        f"{lang('spn_deleted')} {str(count_buffer)} / {str(count)} {lang('prune_hint2')}",
        message_thread_id=message.message_thread_id,
    )


auto_change_name_init = False
dizzy = emojize(":dizzy:", language="alias")
cake = emojize(":cake:", language="alias")
all_time_emoji_name = [
    "clock12",
    "clock1230",
    "clock1",
    "clock130",
    "clock2",
    "clock230",
    "clock3",
    "clock330",
    "clock4",
    "clock430",
    "clock5",
    "clock530",
    "clock6",
    "clock630",
    "clock7",
    "clock730",
    "clock8",
    "clock830",
    "clock9",
    "clock930",
    "clock10",
    "clock1030",
    "clock11",
    "clock1130",
]
time_emoji_symb = [emojize(f":{s}:", language="alias") for s in all_time_emoji_name]


# 动态名称函数
@scheduler.scheduled_job("cron", second=0, id="autochangename")
async def change_name_auto():
    try:
        with open('tgaide.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            nametime_status = data.get('nametime', 0)
            if nametime_status != 1:
                return

        random_line = ""
        if os.path.exists('time.txt'):
            with open('time.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                random_line = random.choice(lines).strip()
        else:
            with open('tgaide.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                online_status = data.get('online', 0)
                random_line = "在线中" if online_status == 1 else "已离线"

        time_cur = (
            datetime.utcnow()
            .replace(tzinfo=timezone.utc)
            .astimezone(timezone(timedelta(hours=8)))
            .strftime("%H:%M:%S:%p:%a")
        )
        hour, minu, seco, p, abbwn = time_cur.split(":")
        shift = 1 if int(minu) > 30 else 0
        hsym = time_emoji_symb[(int(hour) % 12) * 2 + shift]

        _last_name = f"{random_line} {hour}:{minu} {hsym}"
        await bot.update_profile(last_name=_last_name)
        me = await bot.get_me()
        if me.last_name != _last_name:
            raise Exception("修改 last_name 失败")
    except Exception as e:
        trac = "\n".join(traceback.format_exception(e))
        await logs.info(f"更新失败! \n{trac}")


@listener(command="aidetime", description="动态名称操作命令", parameters="<set|mode|name>")
async def handle_time_command(message: Message):
    args = message.arguments.split()
    if not args:
        await edit_delete(message, "请提供参数！参数可以是 set, mode 或 name。")
        return
    
    command = args[0]

    if command == "set":
        await toggle_online_status(message)
    elif command == "mode":
        await toggle_time_mode(message)
    elif command == "name":
        await toggle_name_status(message)
    else:
        await edit_delete(message, "未知参数，请提供 set, mode 或 name 作为参数。")

async def toggle_online_status(message: Message):
    try:
        with open("tgaide.json", "r") as file:
            settings = json.load(file)

        online_status = settings.get("online", 1)
        new_status = 0 if online_status == 1 else 1
        settings["online"] = new_status

        with open("tgaide.json", "w") as file:
            json.dump(settings, file, indent=4)

        status_text = "在线" if new_status == 1 else "离线"
        await message.edit(f"已切换为“{status_text}”状态")
    except (IOError, ValueError) as e:
        await edit_delete(message, f"切换状态时发生错误：{e}")

async def toggle_name_status(message: Message):
    try:
        with open("tgaide.json", "r") as file:
            settings = json.load(file)

        name_status = settings.get("nametime", 1)
        new_status = 0 if name_status == 1 else 1
        settings["nametime"] = new_status

        with open("tgaide.json", "w") as file:
            json.dump(settings, file, indent=4)

        status_text = "开启" if new_status == 1 else "关闭"
        await message.edit(f"已将动态名称设置为“{status_text}”状态")
    except (IOError, ValueError) as e:
        await edit_delete(message, f"开关时发生错误：{e}")

async def toggle_time_mode(message: Message):
    try:
        time_file = "time.txt"
        time1_file = "time1.txt"

        if os.path.exists(time_file):
            os.rename(time_file, time1_file)
            status_text = "已切换到当前状态模式"
        elif os.path.exists(time1_file):
            os.rename(time1_file, time_file)
            status_text = "已切换到随机文本模式"
        else:
            status_text = "未找到time.txt或time1.txt文件，请先使用timetxt设置文本"

        await message.edit(f"{status_text}")
    except (IOError, OSError) as e:
        await edit_delete(message, f"切换时发生错误：{e}")


# 设置随机列表
@listener(command="timetxt", description="显示或设置随机文本内容", parameters="<文本>")
async def timetxt(message: Message):
    input_text = message.arguments
    time_file = "time.txt"
    time1_file = "time1.txt"
    target_file = time_file if os.path.exists(time_file) else time1_file

    try:
        if input_text:
            lines = input_text.split("-")
            with open(target_file, "w") as file:
                for line in lines:
                    file.write(line + "\n")
            await message.edit(f"已更新随机文本内容为:\n" + "\n".join([f"<code>{line}</code>" for line in lines]))
        else:
            if os.path.exists(time_file) or os.path.exists(time1_file):
                if os.path.exists(time_file):
                    target_file = time_file
                else:
                    target_file = time1_file

                with open(target_file, "r") as file:
                    file_content = file.readlines()

                formatted_content = "\n".join([f"<code>{line.strip()}</code>" for line in file_content])
                await message.edit(f"<b>当前随机文本列表</b>\n{formatted_content}")
            else:
                with open(time_file, "w") as file:
                    file.write("")
                await message.edit(f"文件 {time_file} 和 {time1_file} 不存在，已创建 {time_file} 文件。")
    except (IOError, OSError) as e:
        await edit_delete(message, f"读取或写入文件时发生错误：{e}")


# 持续在线模块
@scheduler.scheduled_job("interval", seconds=55, id="keep_online")
async def keep_online():
    try:
        with open("tgaide.json", "r") as file:
            data = json.load(file)
            online_status = data.get("online", 0)

        if online_status == 1:
            await bot.invoke(UpdateStatus(offline=False))
    except Exception as e:
        with contextlib.suppress(Exception):
            await log(f"Keep online failed: {e}")


# 信息查询
@listener(
    command="info",
    description="获取当前群组、发送者和被回复用户的详细信息",
    groups_only=True,
    parameters="[all|me|u]"
)
async def get_info(client: Client, message: Message):
    chat = await client.get_chat(message.chat.id)
    sender = message.from_user
    reply_to_message = message.reply_to_message
    reply_user = reply_to_message.from_user if reply_to_message else None

    def get_chat_info(chat):
        return (
            f"**群组信息**\n"
            f"ID: {chat.id}\n"
            f"标题: {chat.title}\n"
            f"类型: {chat.type}\n"
            f"成员数: {chat.members_count}\n"
            f"描述: {chat.description}\n"
            f"邀请链接: {chat.invite_link}\n"
        )

    def get_user_info(user, prefix="用户"):
        dc_id = "未知"
        try:
            dc_id = f"DC{user.dc_id}"
        except:
            pass
        return (
            f"\n**{prefix}信息**\n"
            f"ID: {user.id}\n"
            f"用户名: {user.username}\n"
            f"全名: {user.first_name} {user.last_name}\n"
            # f"语言代码: {user.language_code}\n"  # 貌似无作用，这里注释了
            f"是否为机器人: {'是' if user.is_bot else '否'}\n"
            f"是否为 Premium 用户: {'是' if user.is_premium else '否'}\n"
            f"DC位置: {dc_id}\n"
        )

    async def get_common_chats_info(user):
        common_chats = await client.get_common_chats(user.id)
        common_chats_info = (
                f"\n**共同群组信息**\n"
                f"共同群组数量: {len(common_chats)}\n" +
                "\n".join([f"- {chat.title} (ID: {chat.id})" for chat in common_chats])
        )
        return common_chats_info

    arg = message.arguments.strip().lower() if message.arguments else None

    info_message = ""
    if arg == "all":
        info_message += get_chat_info(chat)
        info_message += get_user_info(sender, "发送者")
        if reply_user:
            info_message += get_user_info(reply_user, "被回复用户")
            info_message += await get_common_chats_info(reply_user)
    elif arg == "me":
        info_message += get_user_info(sender, "发送者")
    elif arg == "u" and reply_user:
        info_message += get_user_info(reply_user, "被回复用户")
        info_message += await get_common_chats_info(reply_user)
    else:
        info_message += get_chat_info(chat)

    await client.send_message(
        message.chat.id,
        info_message,
        reply_to_message_id=message.reply_to_message_id,
        message_thread_id=message.message_thread_id,
    )
    await message.safe_delete()


server_instance = None
stop_event = threading.Event()


# web相关

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open('tgaide.json', 'r') as f:
                config = json.load(f)
                webkey = config.get('webkey')
        except (FileNotFoundError, json.JSONDecodeError):
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "error", "msg": "Server configuration error"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return

        query_components = parse_qs(urlparse(self.path).query)
        key = query_components.get('key', [None])[0]
        mode = query_components.get('mode', [None])[0]

        if key != webkey:
            self.send_response(403)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "error", "msg": "Key error"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            if mode is None:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response = {"status": "error", "msg": "The mode value is not passed in"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            elif mode == '1':
                id = query_components.get('id', [None])[0]
                msg = query_components.get('msg', [None])[0]
                if not id or not msg:
                    self.send_response(400)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {"status": "error", "msg": "The id and msg values must be passed in and not be empty"}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                else:
                    response = send_message_to_id(id, msg)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response = {"status": "success", "msg": "ok"}
                self.wfile.write(json.dumps(response).encode('utf-8'))


def send_message_to_id(user_id, message_text):
    try:
        bot.send_message(user_id, message_text)
        return {"status": "success", "msg": "Message sent successfully"}
    except Exception as e:
        return {"status": "error", "msg": str(e)}


def run_server(port, stop_event):
    global server_instance
    server_instance = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server_instance.serve_forever()


@listener(command="http", description="开放助手的web服务或设置参数", parameters="<模式> [参数]")
async def http(message: Message):
    global server_instance, stop_event

    arguments = message.arguments.split()
    command = arguments[0] if arguments else None
    parameter = arguments[1] if len(arguments) > 1 else None

    config_file = 'tgaide.json'

    if not os.path.isfile(config_file):
        await edit_delete(message, "配置文件tgaide.json不存在！")
        return

    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
        port = config.get('webport', 6868)

    if command == "stop":
        if server_instance:
            stop_event.set()
            server_instance.shutdown()
            server_instance = None
            await message.edit("HTTP 服务已关闭")
        else:
            await message.edit("HTTP 服务未运行")
        return

    if command == "start":
        if server_instance:
            await message.edit("HTTP 服务已经运行")
        else:
            stop_event.clear()
            server_thread = threading.Thread(target=run_server, args=(port, stop_event))
            server_thread.daemon = True
            server_thread.start()
            await message.edit(f"HTTP 服务运行在端口 {port}")
        return

    if command == "port":
        if not parameter or not parameter.isdigit():
            await edit_delete(message, "请提供一个有效的端口号！")
            return

        port = int(parameter)
        if port < 0 or port > 65535:
            await edit_delete(message, "端口号必须在0到65535之间！")
            return

        config['webport'] = port

        try:
            with open(config_file, 'w', encoding='utf-8') as file:
                json.dump(config, file, ensure_ascii=False, indent=4)

            await message.edit(f"webport已修改为 {port}")

        except Exception as e:
            await edit_delete(message, f"修改配置文件时出错: {str(e)}")
        return

    if command == "key":
        if not parameter:
            await edit_delete(message, "请输入秘钥！")
            return

        config['webkey'] = parameter

        try:
            with open(config_file, 'w', encoding='utf-8') as file:
                json.dump(config, file, ensure_ascii=False, indent=4)

            await message.edit(f"秘钥已成功修改，此秘钥为高危信息，在使用此功能时请确保不在公开群使用！")

        except Exception as e:
            await edit_delete(message, f"修改配置文件时出错: {str(e)}")
        return


    await message.edit("无效的参数，请使用 'start' 或 'stop' 或 'port <端口号>' 或 'key <秘钥>'")




@listener(command="usdtset", description="设置USDT地址", parameters="<USDT地址>")
async def set_usdt_address(message: Message):
    usdt_address = message.arguments
    if not usdt_address or len(usdt_address) != 34:
        await edit_delete(message, "请提供一个有效的34个字符的USDT地址！")
        return

    config_file = 'tgaide.json'

    if not os.path.isfile(config_file):
        await edit_delete(message, "配置文件tgaide.json不存在！")
        return

    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)

        config['usdtaddress'] = usdt_address

        with open(config_file, 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=False, indent=4)

        await message.edit(f"USDT地址已修改为 <code>{usdt_address}</code>")

    except Exception as e:
        await edit_delete(message, f"修改配置文件时出错: {str(e)}")


@listener(command="jy", description="便携usdt收款", parameters="<金额>")
async def handle_jyusdt(message: Message, bot: Client):
    arguments = message.arguments

    if not arguments or not arguments.isdigit():
        await edit_delete(message, "请提供金额参数！")
        return

    json_file_path = os.path.join(os.getcwd(), "tgaide.json")
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    usdt_address = data.get("usdtaddress")

    replied_message = message.reply_to_message
    if replied_message:
        replied_user_id = replied_message.from_user.id
        replied_username = replied_message.from_user.username
        replied_name = replied_message.from_user.first_name
    else:
        replied_user_id = None
        replied_username = None
        replied_name = None

    info = {
        #这里给大家自由发挥哈
        "参数": arguments,
        "USDT地址": usdt_address,
        "回复者ID": replied_user_id,
        "回复者用户名": replied_username,
        "回复者名称": replied_name
    }
    current_timestamp = str(int(datetime.timestamp(datetime.now()))) #时间戳
    current_datetime = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S") #日期-文本
    encrypted_timestamp = simple_xor_encrypt(current_timestamp, arguments) #订单号
    generate_qr_with_text(usdt_address,encrypted_timestamp)
    await message.delete()

    usdt_image_path = os.path.join(os.getcwd(), "usdt.png")

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=usdt_image_path,
        caption=(
            f"""
🔰<b>新交易</b>🔰

<b>🔒订单号</b>：
<i><code>{encrypted_timestamp}</code></i>
<b>🧑需方：[{replied_name}](tg://user?id={replied_user_id})</b>
<b>💰交易金额：<code>{arguments}</code> USDT</b>
<b>📦收款地址👇</b>
<blockquote><code>{usdt_address}</code></blockquote>

<i>🕗当前时间：<i>{current_datetime}</i>
                """
        )
    )


def simple_xor_encrypt(data: str, key: str) -> str:
    encrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
    encoded = base64.urlsafe_b64encode(encrypted.encode()).decode()
    encoded = encoded.rstrip("=")
    return encoded


def generate_gradient_background(width, height, start_color, end_color):
    base = Image.new('RGB', (width, height), start_color)
    top = Image.new('RGB', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (1 - y / height * 0.4))] * width)
    mask.putdata(mask_data)
    gradient = Image.composite(base, top, mask)
    return gradient

def generate_qr_with_text(input_text: str, order: str, output_filename: str = "usdt.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    qr.add_data(input_text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#3490de", back_color="#eaeaea")
    qr_img = qr_img.convert('RGB')  # 添加这行确保图像模式一致
    
    qr_width, qr_height = qr_img.size
    text_height = 150
    border_thickness = 20
    canvas_width = qr_width + 2 * border_thickness
    canvas_height = qr_height + text_height + 2 * border_thickness - 50
    background = generate_gradient_background(canvas_width, canvas_height, '#eaeaea', '#393e46')
    canvas = Image.new('RGB', (canvas_width, canvas_height))
    canvas.paste(background, (0, 0))
    
    # 修改粘贴操作，使用完整的box参数
    qr_x = border_thickness
    qr_y = text_height // 2 + border_thickness
    canvas.paste(qr_img, (qr_x, qr_y, qr_x + qr_width, qr_y + qr_height))

    try:
        icon = Image.open("usdtico.png")
        icon_size = (50, 50)
        icon = icon.resize(icon_size, Image.LANCZOS)
        canvas.paste(icon, (10, 10), icon)
    except IOError:
        print("Icon file not found.")

    try:
        icon = Image.open("tx.png")
        icon_size = (50, 50)
        icon = icon.resize(icon_size, Image.LANCZOS)
        canvas.paste(icon, (260, 10), icon)
    except IOError:
        print("Icon file not found.")

    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype("ys.ttf", 25)
        small_font = ImageFont.truetype("ys.ttf", 12)
    except IOError:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    header_text = "收款地址"
    header_bbox = draw.textbbox((0, 0), header_text, font=font)
    header_width = header_bbox[2] - header_bbox[0]
    header_x = (canvas_width - header_width) // 2
    header_y = border_thickness
    draw.text((header_x, header_y), header_text, font=font, fill="black")

    param_text_bbox = draw.textbbox((0, 0), input_text, font=small_font)
    param_text_width = param_text_bbox[2] - param_text_bbox[0]
    param_text_x = (canvas_width - param_text_width) // 2
    param_text_y = header_y + 40
    draw.text((param_text_x, param_text_y), input_text, font=small_font, fill="#455d7a")

    order = f"订单号：{order}"
    order_text_bbox = draw.textbbox((0, 0), order, font=small_font)
    order_text_width = order_text_bbox[2] - order_text_bbox[0]
    order_text_x = (canvas_width - order_text_width) // 2
    order_text_y = param_text_y + 330
    draw.text((order_text_x, order_text_y), order, font=small_font, fill="#1f5f8b")

    footer_text = "请确保二维码与地址一致！"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    footer_x = (canvas_width - footer_width) // 2
    footer_y = qr_y + qr_height + text_height // 8
    draw.text((footer_x, footer_y), footer_text, font=font, fill="red")

    canvas.save(output_filename)


@listener(command="debug",description="获取当前程序的全部变量名及其值")
async def debug_variables(message: Message):
    global_vars = globals()
    local_vars = locals()
    all_vars = {**global_vars, **local_vars}
    output = "当前变量名及其值:\n"
    for var_name, var_value in all_vars.items():
        try:
            output += f"{var_name}: {var_value}\n"
        except Exception as e:
            output += f"{var_name}: <无法显示值: {e}>\n"
    await message.edit(output)

@listener(command="query", description="搜索聊天记录", parameters="<关键词> [限制条数]")
async def search_messages(message: Message):
    args = message.arguments.strip().split(maxsplit=1)
    if not args:
        await edit_delete(message, "❗️<b>请提供要搜索的关键词！</b>\n<b>用法：</b><code>,query &lt;关键词&gt; [限制条数]</code>")
        return

    keyword = args[0]
    try:
        limit = int(args[1]) if len(args) > 1 else 30
        if limit <= 0:
            raise ValueError
    except ValueError:
        await edit_delete(message, "❗️<b>限制条数必须是大于0的整数！</b>")
        return

    await message.edit(f"🔍✨ <b>正在搜索包含关键词</b> <code>{keyword}</code> <b>的消息</b>（<i>限制 {limit} 条</i>）...🔎")

    results = []
    try:
        async for msg in bot.get_chat_history(
                chat_id=message.chat.id,
                limit=limit + 1
        ):
            if msg.id == message.id:
                continue
            if msg.text and keyword.lower() in msg.text.lower():
                sender = msg.from_user.first_name if msg.from_user else "未知用户"
                msg_text = msg.text[:150] + "..." if len(msg.text) > 150 else msg.text
                result = (
                    f"👤 <b>用户：</b><i>{sender}</i>\n"
                    f"💬 <b>消息内容：</b>\n"
                    f"<blockquote><a href='https://t.me/c/{str(message.chat.id)[4:]}/{msg.id}'>{msg_text}</a></blockquote>\n"
                )
                results.append(result)
        if results:
            response = f"🔍 <b>找到 {len(results)} 条包含关键词</b> <code>{keyword}</code> <b>的消息：</b>\n\n"
            response += "\n━━━━━━✨━━━━━━\n".join(results)

            if len(response) > 4096:
                chunks = [response[i:i + 4096] for i in range(0, len(response), 4096)]
                for chunk in chunks:
                    await bot.send_message(
                        message.chat.id,
                        chunk
                    )
                await message.delete()
            else:
                await bot.send_message(
                    message.chat.id,
                    response
                )
                await message.delete()
        else:
            await message.edit(f"❌ <b>未找到包含关键词</b> <code>{keyword}</code> <b>的消息。</b>😞")

    except Exception as e:
        await edit_delete(message, f"❗️<b>搜索时发生错误：</b>{str(e)} ⚠️")

@listener(command="dcx", description="查询DC分布情况", parameters="[force]")
async def dcq(message: Message):
    await message.edit("🔍 <b>正在查询数据中心分布情况...</b>")

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if not user:
            return await message.edit("❌ <b>无法获取该用户信息</b>")
        try:
            return await message.edit(
                f"👤 <b>用户：</b><code>{user.first_name}</code>\n"
                f"📍 <b>数据中心：</b><code>DC{user.dc_id}</code>"
            )
        except:
            return await message.edit(
                "⚠️ <b>无法查询该用户DC信息</b>\n\n"
                "<b>可能的原因：</b>\n"
                "• 用户未设置头像\n"
                "• 无法访问用户资料\n" 
                "• 用户隐私设置限制"
            )
    
    if message.chat.id > 0:
        try:
            user = await bot.get_users(message.chat.id)
            return await message.edit(
                f"👤 <b>用户：</b><code>{user.first_name}</code>\n"
                f"📍 <b>数据中心：</b><code>DC{user.dc_id}</code>"
            )
        except:
            return await message.edit(
                "⚠️ <b>无法查询您的DC信息</b>\n\n"
                "<b>可能的原因：</b>\n"
                "• 未设置头像\n"
                "• 无法访问资料\n"
                "• 隐私设置限制"
            )

    count = await bot.get_chat_members_count(message.chat.id)
    if count >= 10000 and message.arguments != "force":
        return await message.edit(
            "⚠️ <b>当前群组成员数量过多</b>\n\n"
            "• 成员数：<code>10000+</code>\n"
            "• 可能导致：<code>查询超时</code>\n\n"
            "🔔 如需继续查询请使用：\n<code>,dcx force</code>"
        )

    users = bots = deleted = 0
    dc_ids = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "unknown": 0}

    async for member in bot.get_chat_members(message.chat.id, limit=9999):
        if not member.user.is_bot and not member.user.is_deleted:
            users += 1
            try:
                dc_ids[str(member.user.dc_id)] += 1
            except:
                dc_ids["unknown"] += 1
        elif member.user.is_bot:
            bots += 1
        else:
            deleted += 1

    stats = []
    for dc_num in range(1, 6):
        dc_count = dc_ids[str(dc_num)]
        if users > 0:
            percentage = round((dc_count/users)*100, 2)
            stats.append(
                f"📍 DC{dc_num}: <code>{dc_count}</code> 位用户 (<code>{percentage}%</code>)"
            )

    response = (
        f"📊 <b>数据中心分布统计</b>\n"
        f"━━━━━━✨━━━━━━\n"
        f"<blockquote>{chr(10).join(stats)}</blockquote>\n\n"
        f"📌 <b>其他统计信息</b>\n"
        f"━━━━━━✨━━━━━━\n"
        f"<blockquote>• 未知位置: <code>{dc_ids['unknown']}</code> 位用户 ❓\n"
        f"• 机器人数: <code>{bots}</code> 个机器人 🤖\n" 
        f"• 已注销数: <code>{deleted}</code> 个账号 ⚰️</blockquote>"
    )

    if count >= 10000:
        response += "\n⚠️ <b>注意：受限于 Telegram API，仅显示前 10000 位成员数据</b>"

    await message.edit(response)

@listener(command="rex", description="复读指定消息", parameters="[次数]")
async def rex(message: Message):
    if not message.reply_to_message:
        await edit_delete(message, "❗️ 请回复需要复读的消息")
        return
    try:
        repeat_count = int(message.arguments) if message.arguments else 1
        if repeat_count < 1:
            raise ValueError
    except ValueError:
        await edit_delete(message, "❗️ 复读次数必须是大于0的整数")
        return
    await message.delete()
    reply_msg = message.reply_to_message
    try:
        for _ in range(repeat_count):
            await reply_msg.copy(message.chat.id)
            await asyncio.sleep(0.01)
    except Exception as e:
        await edit_delete(message, f"❗️ 复读消息时发生错误：{str(e)}")

async def check_self_and_from(message: Message):
    cid = message.chat.id
    data = await bot.get_chat_member(cid, (await bot.get_me()).id)
    if data.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return False
    if not message.from_user:
        return False
    if message.outgoing:
        return True
    data = await bot.get_chat_member(cid, message.from_user.id)
    return data.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


async def kick_chat_member(cid, uid, only_search: bool = False):
    if only_search:
        return
    try:
        with contextlib.suppress(UserAdminInvalid, PeerIdInvalid, BadRequest):
            await bot.ban_chat_member(cid, uid, datetime.now() + timedelta(minutes=5))
    except FloodWait as e:
        await sleep(e.value + uniform(0.5, 1.0))
        await kick_chat_member(cid, uid, only_search)


async def process_clean_member(
    message: Message, mode: str, day: int, only_search: bool = False
):
    member_count = 0
    try:
        async for member in bot.get_chat_members(message.chat.id):
            if (
                mode == "1"
                and member.user.last_online_date
                and member.user.last_online_date < datetime.now() - timedelta(days=day)
            ):
                member_count += 1
                await kick_chat_member(message.chat.id, member.user.id, only_search)
            if mode == "2":
                now = datetime.now() - timedelta(days=day)
                async for message in bot.search_messages(
                    message.chat.id, limit=1, from_user=member.user.id
                ):
                    if message.date < now:
                        member_count += 1
                        await kick_chat_member(
                            message.chat.id, member.user.id, only_search
                        )
            elif mode == "3":
                try:
                    count = await bot.search_messages_count(
                        message.chat.id, from_user=member.user.id
                    )
                except PeerIdInvalid:
                    continue
                if count < day:
                    member_count += 1
                    await kick_chat_member(message.chat.id, member.user.id, only_search)
            if mode == "4" and member.user.is_deleted:
                member_count += 1
                await kick_chat_member(message.chat.id, member.user.id, only_search)
            if mode == "5":
                member_count += 1
                await kick_chat_member(message.chat.id, member.user.id, only_search)
        if not only_search:
            await message.edit(f"✅ 成功清理了 `{member_count}` 位成员")
        else:
            await message.edit(f"🔍 共找到 `{member_count}` 位符合条件的成员")
    except ChatAdminRequired:
        await message.edit("⚠️ 您似乎没有封禁用户的权限")
    except FloodWait:
        return await message.edit("❌ 操作失败！您已被 Telegram 服务器限制")

@listener(command="mg", need_admin=True, groups_only=True, description="群成员管理")
async def manage_members(message: Message):
    if not await check_self_and_from(message):
        return await message.edit("⛔️ 您不是群管理员，无法使用此命令")
    
    uid = message.from_user.id
    mode = "0"
    day = 0
    
    reply = await message.edit(
        "🎮 **群成员管理面板** 🎮\n"
        "━━━━━━✨━━━━━━\n\n"
        "**请选择管理模式：**\n\n"
        "1️⃣ 清理长期未上线成员 💤\n"
        "2️⃣ 清理长期未发言成员 🤐\n" 
        "3️⃣ 清理发言数过少成员 📉\n"
        "4️⃣ 清理已注销账号 👻\n"
        "5️⃣ 清理全部成员 🧹\n"
        "━━━━━━✨━━━━━━"
    )

    try:
        async with bot.conversation(message.chat.id, filters=filters.user(uid)) as conv:
            await asyncio.sleep(1)
            res: Message = await conv.get_response()
            mode = res.text
            await res.safe_delete()

            if mode in ["1", "2"]:
                await reply.edit(
                    "⏰ **时间设置** ⏰\n"
                    "━━━━━━✨━━━━━━\n\n"
                    "**请输入清理天数**\n"
                    "⚠️ 最少需要 7 天\n"
                    "━━━━━━✨━━━━━━"
                )
                await asyncio.sleep(1)
                res = await conv.get_response()
                day = max(int(res.text), 7)
                await res.safe_delete()
            
            elif mode == "3":
                await reply.edit(
                    "💬 **发言设置** 💬\n"
                    "━━━━━━✨━━━━━━\n\n"
                    "**请输入最少发言条数：**\n"
                    "📝 低于此数值的成员将被处理\n"
                    "━━━━━━✨━━━━━━"
                )
                await asyncio.sleep(1)
                res = await conv.get_response()
                day = int(res.text)
                await res.safe_delete()
            
            elif mode == "4":
                pass
            elif mode != "5":
                raise ValueError("❌ 无效的管理模式！请重新选择")

            await reply.edit(
                "🔍 **操作模式选择** 🔍\n"
                "━━━━━━✨━━━━━━\n\n"
                "请选择以下操作之一：\n\n"
                "📊 **查找** - 仅统计符合条件的成员\n"
                "🚫 **清理** - 直接移除符合条件的成员\n"
                "━━━━━━✨━━━━━━"
            )
            await asyncio.sleep(1)
            res = await conv.get_response()
            only_search = res.text == "查找"
            await res.safe_delete()

    except ValueError as e:
        return await reply.edit(f"{e}")

    await reply.edit(
        "⏳ **正在处理成员列表...** ⏳\n"
        "━━━━━━✨━━━━━━\n"
        "🔄 请耐心等待处理完成\n"
        "📝 处理结果将稍后显示\n"
        "━━━━━━✨━━━━━━"
    )
    await process_clean_member(reply, mode, day, only_search)

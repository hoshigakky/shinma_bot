import datetime
import logging
import os
from logging import getLogger, StreamHandler, DEBUG

import discord

import requests
from discord.ext import tasks

from const.constants import PUSH_MESSAGE, INFO_MESSAGE
from utils.notice_message import NoticeMessage
from utils.opencv_util import OpenCVUtil
from utils.sqlite_util import SQLiteUtil

# discord client
client = discord.Client()
# Discord Bot token
DISCORD_TOKEN = ""

# 画像格納ベースパス
PIC_BASE_PATH = "z://"

# コマンド定義
CMD_IN = "/inch "
CMD_TIME = "/time "
CMD_OUT = "/outch "
CMD_INFO = "/info"
CMD_TEMPLATE = "/msg "

# logger
logger = getLogger(__name__)
handler = StreamHandler()
# handler = logging.FileHandler(filename="discordbot.log")
handler.setLevel(DEBUG)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s"))
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


@client.event
async def on_ready():
    """Bot起動時に実行されるイベントハンドラ"""
    logger.info("bot boot and init start")
    OpenCVUtil.init_load()
    logger.info("init end")


@client.event
async def on_message(message):
    # コマンドの場合
    if message.content.startswith("/"):
        await cmd_analyze(message)

    # 画像の場合
    sql_util = SQLiteUtil()
    info = sql_util.select_account_by_id(message.guild.id)
    inch = -1
    if len(info) > 0:
        inch = info["inch"]

    if message.channel.id != inch:
        # 設定したチャンネル以外の場合は終了
        return

    urls = _get_file_url(message.attachments)
    if len(urls) > 0:
        url = urls[0]
        # 画像ダウンロード
        path = download_img(url, message.guild.id, os.path.basename(url))

        # 神魔解析
        try:
            match_types = OpenCVUtil.match_weapon_type(path, message.guild.id)
            error_count = 0
            for match_type in match_types:
                if len(match_type) == 0:
                    error_count += 1
            if error_count == 6:
                raise Exception("match type zero")
        except Exception as e:
            logger.error("match error", e)
            await _send_message(message.guild.id, message.channel.id, "解析に失敗したか神魔画像ではありません。")
            return
        # 画像削除
        os.remove(path)
        # メッセージ作成
        msg = NoticeMessage.create_notice_message(match_types, message.guild.id)
        push_msg = msg.format(match_types)

        # リマインド用メッセージ更新
        sql_util.update_message(message.guild.id, push_msg)

        # 神魔情報投稿チャンネルにメッセージを送信
        info = sql_util.select_account_by_id(message.guild.id)
        msg_push_channel = info["outch"]

        await _send_message(message.guild.id, msg_push_channel, push_msg)


async def cmd_analyze(message):
    """
    コマンドごとの処理
    param message: ハイフンで始まる文字列
    """
    server_id = message.guild.id
    receive_msg = message.content
    sql_util = SQLiteUtil()
    # print("msg = " + message)
    account = sql_util.select_account_by_id(server_id)
    if len(account) == 0:
        sql_util.insert_account(server_id)

    msg = sql_util.select_msg_template(server_id)
    if len(msg) == 0:
        # メッセージ未設定の場合テンプレート使用
        sql_util.insert_msg_template(server_id, PUSH_MESSAGE)
        msg = PUSH_MESSAGE

    if receive_msg.startswith(CMD_IN):
        for guild in client.guilds:
            for channel in guild.channels:
                for text_ch in channel.guild.text_channels:
                    if receive_msg.split(" ")[1] == text_ch.name:
                        logger.info(text_ch.name + " = " + str(text_ch.id))
                        sql_util.update_in_channel(server_id, text_ch.id)
                        break

    elif receive_msg.startswith(CMD_TIME):
        # フォーマットチェック
        try:
            input_time = receive_msg.split(" ")[1]
            datetime.datetime.strptime(input_time, "%H:%M")
            sql_util.update_time(server_id, input_time)
        except ValueError:
            await _send_message(message.guild.id, message.channel.id, "設定値が不正です。(例 12:30)")

    elif receive_msg.startswith(CMD_OUT):
        for guild in client.guilds:
            for channel in guild.channels:
                for text_ch in channel.guild.text_channels:
                    if receive_msg.split(" ")[1] == text_ch.name:
                        print(text_ch.name + str(text_ch.id))
                        sql_util.update_out_channel(server_id, text_ch.id)
                        break
    elif receive_msg.startswith(CMD_INFO):
        await _send_message(server_id,
                            message.channel.id,
                            INFO_MESSAGE.format(
                                message.guild._channels[account["inch"]].name,
                                message.guild._channels[account["outch"]].name,
                                account["time"],
                                msg.replace("`", "` ")))
    elif receive_msg.startswith(CMD_TEMPLATE + "reset"):
        sql_util.insert_msg_template(server_id, PUSH_MESSAGE)
    elif receive_msg.startswith(CMD_TEMPLATE):
        template = receive_msg.replace(CMD_TEMPLATE, "")
        sql_util.insert_msg_template(server_id, template)
    else:
        # 認識できないコマンド
        pass


def download_img(url: str, server_id: str, file_name: str) -> str:
    """
    画像ファイルのダウンロード
    :rtype: object
    :param url: ダウンロード先URL
    :param server_id: 投稿サーバID
    :param file_name: ダウンロードファイル名
    :return: 画像ファイルの保存パス
    """
    writePath = PIC_BASE_PATH + str(server_id) + "/" + file_name
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        if not os.path.exists(PIC_BASE_PATH + str(server_id)):
            os.makedirs(PIC_BASE_PATH + str(server_id))

        # ダウンロードしたデータを書き込み
        with open(writePath, 'wb') as f:
            f.write(r.content)
    return writePath


def _get_file_url(attachments: list) -> list:
    """ attachmentsからURLを取得する """
    # -> List[str]:
    url_list = []
    for attachment in attachments:
        logger.info(attachment.url)
        if len(attachment.url) > 0:
            url_list.append(attachment.url)
    return url_list


def _push_msg_clear():
    sql_util = SQLiteUtil()
    sql_util.all_clear_message()


async def _remind():
    logger.info("remind start")
    now = datetime.datetime.now()
    hour = now.strftime("%H:%M")
    if hour == "00:00":  # メッセージクリア用
        _push_msg_clear()

    sql_util = SQLiteUtil()
    info_list = sql_util.select_time_group(hour)

    for info in info_list:
        logger.info(info)
        await _send_message(info["id"], info["outch"], info["pushmsg"])
        sql_util.update_message(info["id"], "")


@tasks.loop(seconds=30)
async def _loop():
    logger.info("task loop")

    try:
        # 再接続
        if client.is_closed():
            await client.connect(reconnect=True)

        # 5分前神魔リマインド
        if client.is_ready():
            await _remind()
    except Exception as e:
        logger.error("loop error", e)


async def _send_message(server_id: int, channel_id: str, msg: str):
    logger.info("send message = " + msg)
    channel = client.get_channel(channel_id)
    await channel.send(msg)


if __name__ == "__main__":
    _loop.start()
    client.run(DISCORD_TOKEN)

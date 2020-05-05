import datetime
import logging
import os
from logging import getLogger, StreamHandler, DEBUG

import discord

# discord client
import requests
from discord.ext import tasks

from const.constants import constant_time_list, TIME_1, TIME_2, TIME_3, TIME_4, TIME_5, TIME_6, TIME_7, TIME_8, \
    PUSH_MESSAGE, INFO_MESSAGE
from utils.opencv_util import OpenCVUtil
from utils.sqlite_util import SQLiteUtil

client = discord.Client()
# Discord Bot token
DISCORD_TOKEN = ""

# 画像格納ベースパス
PIC_BASE_PATH = "z://"

# コマンド定義
CMD_IN = "/inch"
CMD_TIME = "/time"
CMD_OUT = "/outch"
CMD_INFO = "/info"

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

        # 新魔解析
        try:
            match_types = OpenCVUtil.match_weapon_type(path, message.guild.id)
        except Exception as e:
            logger.error("match error", e)
            await _send_message(message.guild.id, message.channel.id, "解析に失敗しました。")
            return
        # 画像削除
        os.remove(path)
        # メッセージ作成
        push_msg = PUSH_MESSAGE.format(match_types)

        # リマインド用メッセージ更新
        sql_util.update_message(message.guild.id, push_msg)

        # 新魔情報投稿チャンネルにメッセージを送信
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
            if input_time not in constant_time_list():
                raise ValueError("invalid time string")

            sql_util.update_time(server_id, input_time)
        except ValueError:
            await _send_message(message.guild.id, message.channel.id, "設定可能値：" + ",".join(constant_time_list()))

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
                                account["time"]))
        pass
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


async def _remind():
    logger.info("remind start")
    now = datetime.datetime.now()
    hour = now.strftime("%H%M")

    if hour == "0755":  # 08:00
        start_time = TIME_1
    elif hour == "1225":  # 12:30
        start_time = TIME_2
    elif hour == "1755":  # 18:00
        start_time = TIME_3
    elif hour == "1855":  # 19:00
        start_time = TIME_4
    elif hour == "1955":  # 20:00
        start_time = TIME_5
    elif hour == "2055":  # 21:00
        start_time = TIME_6
    elif hour == "2155":  # 22:00
        start_time = TIME_7
    elif hour == "2255":  # 23:00
        start_time = TIME_8
    else:
        return

    sql_util = SQLiteUtil()
    info_list = sql_util.select_time_group(start_time)

    for info in info_list:
        logger.info(info)
        await _send_message(info["id"], info["outch"], info["pushmsg"])
        sql_util.update_message(info["id"], "")


@tasks.loop(seconds=30)
async def _loop():
    logger.info("task loop")

    # 再接続
    if client.is_closed():
        await client.connect(reconnect=True)

    # 5分前神魔リマインド
    if client.is_ready():
        await _remind()


async def _send_message(server_id: int, channel_id: str, msg: str):
    logger.info("send message = " + msg)
    channel = client.get_channel(channel_id)
    await channel.send(msg)


if __name__ == "__main__":
    _loop.start()
    client.run(DISCORD_TOKEN)

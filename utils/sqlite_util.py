import sqlite3
import os

dbname = 'bot.db'

# dbname = '/home/discord/bot/bottest/bot.db'


def _create_db():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("create table account"
              "("
              "id integer primary key, "  # サーバID
              "inch integer, "  # 画像投稿用チャンネル
              "outch integer, "  # 解析結果投稿用チャンネル
              "time text,"  # コロシアム時間帯(例 08:00)
              "pushmsg text)"  # メッセージ
              )
    conn.commit()
    conn.close()


class SQLiteUtil:
    def __init__(self):
        exist = os.path.exists(dbname)
        if not exist:
            # DB初期化処理
            _create_db()

    @staticmethod
    def insert_account(server_id: str):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = "insert into account values(?, ?, ?, ?, ?)"

        c.execute(sql, (server_id, 0, 0, "", ""))
        conn.commit()
        conn.close()

    @staticmethod
    def select_account_by_id(server_id: int) -> dict:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = "select * from account where id = ? "
        c.execute(sql, (server_id,))
        accountData = c.fetchone()

        info = {}
        if accountData is not None and len(accountData) > 0:
            info = {
                "id": accountData[0],
                "inch": accountData[1],
                "outch": accountData[2],
                "time": accountData[3],
                "pushmsg": accountData[4]
            }

        return info

    @staticmethod
    def select_time_group(time: str) -> list:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = "select * from account where time = ?"
        c.execute(sql, (time,))
        accountData = c.fetchall()

        infoList = []
        for data in accountData:
            info = {
                "id": data[0],
                "inch": data[1],
                "outch": data[2],
                "time": data[3],
                "pushmsg": data[4]
            }
            infoList.append(info)

        return infoList

    @staticmethod
    def update_in_channel(server_id: str, inch: int):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = "update account set inch = ? where id = ?"
        c.execute(sql, (inch, server_id))
        conn.commit()
        conn.close()

    @staticmethod
    def update_out_channel(server_id: str, outch: int):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = "update account set outch = ? where id = ?"
        c.execute(sql, (outch, server_id))
        conn.commit()
        conn.close()

    @staticmethod
    def update_time(server_id: str, time: str):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = "update account set time = ? where id = ?"
        c.execute(sql, (time, server_id))
        conn.commit()
        conn.close()

    @staticmethod
    def update_message(server_id: str, msg: str):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = "update account set pushmsg = ? where id = ?"
        c.execute(sql, (msg, server_id))
        conn.commit()
        conn.close()

    @staticmethod
    def all_clear_message():
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = "update account set pushmsg = ''"
        c.execute(sql)
        conn.commit()
        conn.close()

from const.constants import TYPE_1, TYPE_2, TYPE_3, TYPE_4, TYPE_5, TYPE_6, TYPE_7, DISASTER_1, DISASTER_2, DISASTER_3, \
    DISASTER_4, DISASTER_5, DISASTER_6, PUSH_MESSAGE
from utils.sqlite_util import SQLiteUtil


class NoticeMessage:

    @staticmethod
    def create_notice_message(match_types, server_id: str) -> str:
        # 神魔名取得
        first_disaster, match_types[1], match_types[2] = \
            NoticeMessage._get_disaster(match_types[0], match_types[1], match_types[2])
        second_disaster, match_types[4], match_types[5] = \
            NoticeMessage._get_disaster(match_types[3], match_types[4], match_types[5])

        # メッセージ取得
        sql_util = SQLiteUtil()
        msg = sql_util.select_msg_template(server_id)
        if len(msg) == 0:
            # メッセージ未設定の場合テンプレート使用
            sql_util.insert_msg_template(server_id, PUSH_MESSAGE)
            msg = PUSH_MESSAGE

        notice = msg.format(match_types[0],
                            match_types[1],
                            match_types[2],
                            match_types[3],
                            match_types[4],
                            match_types[5],
                            first_disaster,
                            second_disaster)
        return notice

    @staticmethod
    def _get_disaster(rear: str, front_1: str, front_2: str):
        type_1_2 = False
        type_3_4 = False
        if front_1 in (TYPE_1, TYPE_2) or front_2 in (TYPE_1, TYPE_2):  # 打撃、射出
            type_1_2 = True
        elif front_1 in (TYPE_3, TYPE_4) or front_2 in (TYPE_3, TYPE_4):  # 刀剣、長柄
            type_3_4 = True

        # 前衛武器のどちらかが解析に失敗している可能性を考慮し戻り値に武器を含める
        if rear == TYPE_5:  # 祈祷
            if type_1_2:
                # 震波の厄災
                return DISASTER_1, TYPE_1, TYPE_2
            elif type_3_4:
                # 氷雪の厄災
                return DISASTER_2, TYPE_3, TYPE_4
        elif rear == TYPE_6:  # 魔書
            if type_1_2:
                # 旋風の厄災
                return DISASTER_3, TYPE_1, TYPE_2
            elif type_3_4:
                # 日輪の厄災
                return DISASTER_4, TYPE_3, TYPE_4
        elif rear == TYPE_7:  # 楽器
            if type_1_2:
                # 流星の厄災
                return DISASTER_5, TYPE_1, TYPE_2
            elif type_3_4:
                # 雷公の厄災
                return DISASTER_6, TYPE_3, TYPE_4
        else:
            # 神魔名不明
            if type_1_2:
                return "", TYPE_1, TYPE_2
            elif type_3_4:
                return "", TYPE_3, TYPE_4

import platform

TYPE_1 = "打撃"
TYPE_2 = "射出"
TYPE_3 = "刀剣"
TYPE_4 = "長柄"
TYPE_5 = "祈祷"
TYPE_6 = "魔書"
TYPE_7 = "楽器"
TYPE_8 = "魔具"


def constant_list() -> ():
    return TYPE_1, TYPE_2, TYPE_3, TYPE_4, TYPE_5, TYPE_6, TYPE_7, TYPE_8


DISASTER_1 = "震波"   # 震波の厄災 打撃、射出、祈祷
DISASTER_2 = "氷雪"   # 氷雪の厄災 刀剣、長柄、祈祷
DISASTER_3 = "旋風"   # 旋風の厄災 打撃、射出、魔書
DISASTER_4 = "日輪"   # 日輪の厄災 刀剣、長柄、魔書
DISASTER_5 = "流星"   # 流星の厄災 打撃、射出、楽器
DISASTER_6 = "雷公"   # 雷公の厄災 刀剣、長柄、楽器
# DISASTER_7 = "日輪"   # 日輪の厄災(魔具) 刀剣、魔具、魔書

# 装備画像保存パス
os_name = platform.system()
if os_name.lower() == "windows":
    TMP_SCREEN_SHOT_PATH = "C://Users/dev/Documents/GitHub/shinma_bot/data/"
else:
    TMP_SCREEN_SHOT_PATH = "/home/discord/shinma_bot/data/"

# データベース名
DB_NAME = "weaponss.db"
# データベースの絶対パス
if os_name.lower() == "windows":
    DB_PATH = "C://Users/dev/Documents/GitHub/shinma_bot//windows_" + DB_NAME
else:
    DB_PATH = "/home/discord/shinma_bot/" + DB_NAME

# PUSH_MESSAGE = "本日の神魔\n" \
#                "=============================\n" \
#                "第1神魔：{0[0]}、{0[1]}、{0[2]}\n" \
#                "第2神魔：{0[3]}、{0[4]}、{0[5]}\n" \
#                "============================="
PUSH_MESSAGE = "本日の神魔\n" \
               "```\n" \
               "第1神魔({6})：{0}、{1}、{2}\n" \
               "第2神魔({7})：{3}、{4}、{5}\n" \
               "```"
INFO_MESSAGE = "設定情報\n" \
               "```\n" \
               "画像投稿チャンネル:{0}\n" \
               "神魔情報投稿チャンネル:{1}\n" \
               "通知時間:{2}\n" \
               "通知メッセージ:{3}\n" \
               "```"
# 第1神魔 場所算出用
FIRST_LEFT_X = 0.317
FIRST_LEFT_Y = 0.304
FIRST_RIGHT_X = 0.484
FIRST_RIGHT_Y = 0.354
# 第2神魔 場所算出用
SECOND_LEFT_X = 0.317
SECOND_LEFT_Y = 0.743
SECOND_RIGHT_X = 0.484
SECOND_RIGHT_Y = 0.792

TYPE_PATHS = {
    TYPE_1: [TMP_SCREEN_SHOT_PATH + "pattern1/weapon_type_1.png",
             TMP_SCREEN_SHOT_PATH + "pattern2/weapon_type_1.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_1.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_1_1.png"],
    TYPE_2: [TMP_SCREEN_SHOT_PATH + "pattern1/weapon_type_2.png",
             TMP_SCREEN_SHOT_PATH + "pattern2/weapon_type_2.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_2.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_2_1.png"],
    TYPE_3: [TMP_SCREEN_SHOT_PATH + "pattern1/weapon_type_3.png",
             TMP_SCREEN_SHOT_PATH + "pattern2/weapon_type_3.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_3.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_3_1.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_3_2.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_3_3.png"],
    TYPE_4: [TMP_SCREEN_SHOT_PATH + "pattern1/weapon_type_4.png",
             TMP_SCREEN_SHOT_PATH + "pattern2/weapon_type_4.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_4.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_4_1.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_4_2.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_4_3.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_4_4.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_4_5.png"],
    TYPE_5: [TMP_SCREEN_SHOT_PATH + "pattern1/weapon_type_5.png",
             TMP_SCREEN_SHOT_PATH + "pattern2/weapon_type_5.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_5.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_5_1.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_5_2.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_5_3.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_5_4.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_5_5.png"],
    TYPE_6: [TMP_SCREEN_SHOT_PATH + "pattern1/weapon_type_6.png",
             TMP_SCREEN_SHOT_PATH + "pattern2/weapon_type_6.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_6.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_6_1.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_6_2.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_6_3.png"],
    TYPE_7: [TMP_SCREEN_SHOT_PATH + "pattern1/weapon_type_7.png",
             TMP_SCREEN_SHOT_PATH + "pattern2/weapon_type_7.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_7.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_7_1.png",
             TMP_SCREEN_SHOT_PATH + "pattern3/weapon_type_7_2.png"],
    TYPE_8: []
}

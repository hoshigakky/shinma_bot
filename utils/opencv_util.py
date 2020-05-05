import logging
import cv2
import numpy as np

# loggerの子loggerオブジェクトの宣言
from const.constants import constant_list, FIRST_LEFT_Y, FIRST_RIGHT_Y, FIRST_LEFT_X, FIRST_RIGHT_X, SECOND_LEFT_Y, \
    SECOND_RIGHT_Y, SECOND_LEFT_X, SECOND_RIGHT_X, TYPE_PATHS

from const.constants import TMP_SCREEN_SHOT_PATH

logger = logging.getLogger("discord_bot").getChild(__name__)

# 拡大率
RATE = 4


class OpenCVUtil:
    descriptors = {key: [] for key in TYPE_PATHS.keys()}
    key_points = {key: [] for key in TYPE_PATHS.keys()}
    images = {key: [] for key in TYPE_PATHS.keys()}

    @staticmethod
    def init_load():
        akaze = cv2.AKAZE_create()
        for path_key in TYPE_PATHS.keys():
            paths = TYPE_PATHS[path_key]
            for path in paths:
                weapon_type_img = cv2.imread(path)
                height = weapon_type_img.shape[0]
                width = weapon_type_img.shape[1]
                # 特徴量を抽出しやすいように画像を拡大
                weapon_type_img = cv2.resize(weapon_type_img, (int(width * RATE), int(height * RATE)))

                # 特徴量を保持
                kp1, des1 = akaze.detectAndCompute(weapon_type_img, None)
                OpenCVUtil.descriptors[path_key].append(des1)
                OpenCVUtil.key_points[path_key].append(kp1)
                OpenCVUtil.images[path_key].append(weapon_type_img)

    # @staticmethod
    # def init_load():
    #     akaze = cv2.AKAZE_create()
    #     weapon_type_set_path = [TMP_SCREEN_SHOT_PATH + "new_small", TMP_SCREEN_SHOT_PATH + "small"]
    #     for path in weapon_type_set_path:
    #
    #         for i in range(1, len(constant_list()) + 1):
    #             weapon_type_img = cv2.imread(path + "/weapon_type_" + str(i) + ".png")
    #             height = weapon_type_img.shape[0]
    #             width = weapon_type_img.shape[1]
    #             # 特徴量を抽出しやすいように画像を拡大
    #             weapon_type_img = cv2.resize(weapon_type_img, (int(width * RATE), int(height * RATE)))
    #
    #             # 特徴量を保持
    #             kp1, des1 = akaze.detectAndCompute(weapon_type_img, None)
    #             OpenCVUtil.descriptors.append(des1)
    #             OpenCVUtil.key_points.append(kp1)
    #             OpenCVUtil.images.append(weapon_type_img)

    @staticmethod
    def _create_red_mask(image):
        # HSV色空間に変換
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 赤色のHSVの値域1
        hsv_min = np.array([0, 64, 0])
        hsv_max = np.array([30, 255, 255])
        mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

        # 赤色のHSVの値域2
        hsv_min = np.array([150, 64, 0])
        hsv_max = np.array([179, 255, 255])
        mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

        # 赤色領域のマスク（255：赤色、0：赤色以外）
        mask = mask1 + mask2

        return mask

    @staticmethod
    def match_weapon_type(image_path: str, server_id) -> []:
        logger.debug("matching start")
        target_image = cv2.imread(image_path)
        top_match_types = OpenCVUtil._match(target_image, server_id)
        return top_match_types

    @staticmethod
    def _match(target_img, server_id) -> []:
        match_types = []
        rects = OpenCVUtil._find_rectangle(target_img)
        rect_img = target_img[rects[0][1]:rects[1][1], rects[0][0]:rects[1][0]]
        OpenCVUtil._debug_image_writer("z://" + str(server_id) + "/rect.png", rect_img)
        rect_height = rect_img.shape[0]
        rect_width = rect_img.shape[1]
        first_place = rect_img[int(rect_height * FIRST_LEFT_Y):int(rect_height * FIRST_RIGHT_Y),
                      int(rect_width * FIRST_LEFT_X):int(rect_width * FIRST_RIGHT_X)]
        second_place = rect_img[int(rect_height * SECOND_LEFT_Y):int(rect_height * SECOND_RIGHT_Y),
                       int(rect_width * SECOND_LEFT_X):int(rect_width * SECOND_RIGHT_X)]

        # 特徴量を抽出しやすいように画像を拡大
        OpenCVUtil._debug_image_writer("z://" + str(server_id) + "/resize_before_firstbot.png", first_place)
        first_place = cv2.resize(first_place, (int(first_place.shape[1] * RATE), int(first_place.shape[0] * RATE)))
        second_place = cv2.resize(second_place, (int(second_place.shape[1] * RATE), int(second_place.shape[0] * RATE)))
        OpenCVUtil._debug_image_writer("z://" + str(server_id) + "/resize_after_firstbot.png", first_place)

        akaze = cv2.AKAZE_create()
        blocks = []
        for i in range(0, 3):
            concat_height = first_place.shape[0]
            # 神魔武器3つ入っているので3分割する
            concat_block_width = int(first_place.shape[1] / 3)
            # 武器1つ分の範囲で画像を分割
            blocks.append(first_place[0:concat_height, i * concat_block_width: (i + 1) * concat_block_width])
        for i in range(0, 3):
            concat_height = second_place.shape[0]
            concat_block_width = int(second_place.shape[1] / 3)
            blocks.append(second_place[0:concat_height, i * concat_block_width: (i + 1) * concat_block_width])

        # デバッグ用出力
        for i, block in enumerate(blocks):
            OpenCVUtil._debug_image_writer("z://" + str(server_id) + "/block_" + str(i) + ".png", block)
        OpenCVUtil._debug_image_writer("z://" + str(server_id) + "/firstbot.png", first_place)
        OpenCVUtil._debug_image_writer("z://" + str(server_id) + "/secondbot.png", second_place)

        bf = cv2.BFMatcher()
        for pic, block in enumerate(blocks):
            block_kp, block_des = akaze.detectAndCompute(block, None)
            more_score = 0
            more_type = ""
            for i, des_keys in enumerate(OpenCVUtil.descriptors.keys()):
                for des in OpenCVUtil.descriptors.get(des_keys):
                    matches = bf.knnMatch(des, block_des, k=2)

                    good = []
                    for m, n in matches:
                        if m.distance < 0.5 * n.distance:
                            good.append([m])

                    # debug
                    # out1 = cv2.drawKeypoints(OpenCVUtil.images[i], OpenCVUtil.key_points[i], None)
                    # out2 = cv2.drawKeypoints(block, block_kp, None)
                    # img_kaze = cv2.drawMatchesKnn(out1, OpenCVUtil.key_points[i], out2, block_kp, good, None, flags=2)
                    # OpenCVUtil._debug_image_writer("z://type" + str(i) + '.png', out1)
                    # OpenCVUtil._debug_image_writer('z://img_gray_debug_1' + str(pic) + str(i) + '.png', img_kaze)

                    logger.info(str(i) + " type : " + str(len(good)))
                    if len(good) > more_score:
                        if i >= len(constant_list()):
                            logger.info(constant_list()[i - len(constant_list())])
                            more_score = len(good)
                            more_type = constant_list()[i - len(constant_list())]
                        else:
                            logger.info(constant_list()[i])
                            more_score = len(good)
                            more_type = constant_list()[i]

            match_types.append(more_type)

        return match_types

    @staticmethod
    def _find_rectangle(image) -> ():
        logger.debug("find rectangle start")
        image = cv2.GaussianBlur(image, (11, 11), 0)

        # BGRでの色抽出
        bgrLower = np.array([110, 110, 110])  # 抽出する色の下限(BGR)
        bgrUpper = np.array([200, 200, 200])  # 抽出する色の上限(BGR)
        img_mask = cv2.inRange(image, bgrLower, bgrUpper)  # BGRからマスクを作成
        result = cv2.bitwise_and(image, image, mask=img_mask)  # 元画像とマスクを合成
        height = result.shape[0]
        width = result.shape[1]

        OpenCVUtil._debug_image_writer("z://find_rect.png", result)

        black_pixel = 0
        rect_start_pixel_w = -1
        rect_start_pixel_h = -1
        end = False
        # 左上の位置を特定
        for h in range(0, height - 1):
            for w in range(0, width - 1):
                b = result[h, w][0]
                g = result[h, w][1]
                r = result[h, w][2]
                if b != 0 and g != 0 and r != 0:
                    logger.info("[" + str(w) + "," + str(h) + "] " + str(b) + ", " + str(g) + ", " + str(r))
                    if rect_start_pixel_w == -1:
                        rect_start_pixel_w = w
                        rect_start_pixel_h = h

                    # 背景色が黒以外で連続横幅6割続いた場合は神魔の範囲とみなす
                    black_pixel += 1
                    if black_pixel > int(width * 0.6):
                        end = True
                        left = rect_start_pixel_w, rect_start_pixel_h
                        break

            rect_start_pixel_w = -1
            rect_start_pixel_h = -1
            black_pixel = 0
            if end is True:
                break

        # 右下の位置を特定
        rect_start_pixel_w = -1
        rect_start_pixel_h = -1
        end = False
        black_pixel = 0
        for h in range(height - int(height / 10), 0, -1):  # 下部はOKボタンがあるので少し範囲を狭めるため10で割った値を使用
            for w in range(width - 1, 0, -1):
                b = result[h, w][0]
                g = result[h, w][1]
                r = result[h, w][2]
                if b != 0 and g != 0 and r != 0:
                    logger.info("[" + str(w) + "," + str(h) + "] " + str(b) + ", " + str(g) + ", " + str(r))
                    if rect_start_pixel_w == -1:
                        rect_start_pixel_w = w
                        rect_start_pixel_h = h
                    # 背景色が黒以外で連続横幅6割続いた場合は神魔の範囲とみなす
                    black_pixel += 1
                    if black_pixel > int(width * 0.6):
                        end = True
                        right = rect_start_pixel_w, rect_start_pixel_h
                        break
            rect_start_pixel_w = -1
            rect_start_pixel_h = -1
            black_pixel = 0
            if end is True:
                break

        return left, right

    @staticmethod
    def _debug_image_writer(path: str, image):
        cv2.imwrite(path, image)

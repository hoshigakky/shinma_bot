import logging
import cv2
import numpy as np

# loggerの子loggerオブジェクトの宣言
from const.constants import constant_list, FIRST_LEFT_Y, FIRST_RIGHT_Y, FIRST_LEFT_X, FIRST_RIGHT_X, SECOND_LEFT_Y, \
    SECOND_RIGHT_Y, SECOND_LEFT_X, SECOND_RIGHT_X

from const.constants import TMP_SCREEN_SHOT_PATH

logger = logging.getLogger("discord_bot").getChild(__name__)

RATE = 4


class OpenCVUtil:
    descriptors = []
    key_points = []
    images = []

    @staticmethod
    def init_load():
        akaze = cv2.AKAZE_create()
        for i in range(1, len(constant_list()) + 1):
            logger.info(TMP_SCREEN_SHOT_PATH + "weapon_type_" + str(i) + ".png")
            weapon_type_img = cv2.imread(TMP_SCREEN_SHOT_PATH + "new_small/weapon_type_" + str(i) + ".png")
            height = weapon_type_img.shape[0]
            width = weapon_type_img.shape[1]
            # # 特徴量を抽出しやすいように画像を拡大
            weapon_type_img = cv2.resize(weapon_type_img, (int(width * RATE), int(height * RATE)))
            # img_gray = cv2.cvtColor(img2_gray_big, cv2.COLOR_BGR2GRAY)
            # im_blur = cv2.GaussianBlur(img_gray, (11, 11), 0)
            # img_thresh = cv2.adaptiveThreshold(im_blur, 155, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7,
            #                                    3)
            # weapon_type_img = OpenCVUtil._common_image(weapon_type_img)

            # bgrLower = np.array([4, 4, 200])  # 抽出する色の下限(BGR)
            # bgrUpper = np.array([120, 126, 205])  # 抽出する色の上限(BGR)
            # img_mask = cv2.inRange(weapon_type_img, bgrLower, bgrUpper)  # BGRからマスクを作成
            # weapon_type_img = cv2.bitwise_and(weapon_type_img, weapon_type_img, mask=img_mask)  # 元画像とマスクを合成

            # # マスキング処理
            # red_mask = OpenCVUtil._create_red_mask(weapon_type_img)
            # weapon_type_img = cv2.bitwise_and(weapon_type_img, weapon_type_img, mask=red_mask)
            #
            # weapon_type_img = cv2.cvtColor(weapon_type_img, cv2.COLOR_BGR2GRAY)
            # weapon_type_img = cv2.GaussianBlur(weapon_type_img, (11, 11), 0)
            # weapon_type_img = cv2.adaptiveThreshold(weapon_type_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 3)

            kp1, des1 = akaze.detectAndCompute(weapon_type_img, None)
            OpenCVUtil.descriptors.append(des1)
            OpenCVUtil.key_points.append(kp1)
            OpenCVUtil.images.append(weapon_type_img)
        for i in range(1, len(constant_list()) + 1):
            logger.info(TMP_SCREEN_SHOT_PATH + "weapon_type_" + str(i) + ".png")
            weapon_type_img = cv2.imread(TMP_SCREEN_SHOT_PATH + "small/weapon_type_" + str(i) + ".png")
            height = weapon_type_img.shape[0]
            width = weapon_type_img.shape[1]
            # # 特徴量を抽出しやすいように画像を拡大
            weapon_type_img = cv2.resize(weapon_type_img, (int(width * RATE), int(height * RATE)))
            kp1, des1 = akaze.detectAndCompute(weapon_type_img, None)
            OpenCVUtil.descriptors.append(des1)
            OpenCVUtil.key_points.append(kp1)
            OpenCVUtil.images.append(weapon_type_img)

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
    def match_weapon_type(image_path: str) -> []:
        logger.debug("matching start")
        # match_types = []
        akaze = cv2.AKAZE_create()
        target_image = cv2.imread(image_path)
        # height = target_image.shape[0]
        # width = target_image.shape[1]
        # # 特徴量を抽出しやすいように画像を拡大
        # target_image_big = cv2.resize(target_image, (int(width * 5), int(height * 5)))
        # img_gray = cv2.cvtColor(target_image_big, cv2.COLOR_BGR2GRAY)
        # im_blur = img_gray  # cv2.GaussianBlur(img_gray, (11, 11), 0)
        # img_thresh = cv2.adaptiveThreshold(im_blur, 155, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 3)
        # img_thresh = OpenCVUtil._common_image(target_image)

        # それぞれで特徴量を取得
        # target_top_kp, target_top_des = akaze.detectAndCompute(target_image, None)
        # target_bottom_kp, target_bottom_des = akaze.detectAndCompute(bottom_image, None)

        top_match_types = OpenCVUtil._match(target_image)
        # bottom_match_types = OpenCVUtil._match(target_bottom_kp, target_bottom_des, bottom_image)
        # print(top_match_types)
        # print(bottom_match_types)

        # return top_match_types, bottom_match_types
        return top_match_types

    # @staticmethod
    # def _common_image(image):
    #     # 特徴量を抽出しやすいように画像を拡大
    #     height = image.shape[0]
    #     width = image.shape[1]
    #     img2_gray_big = cv2.resize(image, (int(width * 5), int(height * 5)))
    #     img_gray = cv2.cvtColor(img2_gray_big, cv2.COLOR_BGR2GRAY)
    #     im_blur = cv2.GaussianBlur(img_gray, (11, 11), 0)
    #     img_thresh = cv2.adaptiveThreshold(im_blur, 155, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 3)
    #
    #     return img_thresh

    @staticmethod
    def _match(target_img) -> []:
        match_types = []
        rects = OpenCVUtil._find_rectangle(target_img)
        rect_img = target_img[rects[0][1]:rects[1][1], rects[0][0]:rects[1][0]]
        cv2.imwrite("z://rect.png", rect_img)
        rect_height = rect_img.shape[0]
        rect_width = rect_img.shape[1]
        first_place = rect_img[int(rect_height * FIRST_LEFT_Y):int(rect_height * FIRST_RIGHT_Y), int(rect_width * FIRST_LEFT_X):int(rect_width * FIRST_RIGHT_X)]
        second_place = rect_img[int(rect_height * SECOND_LEFT_Y):int(rect_height * SECOND_RIGHT_Y), int(rect_width * SECOND_LEFT_X):int(rect_width * SECOND_RIGHT_X)]

        # 特徴量を抽出しやすいように画像を拡大
        cv2.imwrite("z://resize_before_firstbot.png", first_place)
        first_place = cv2.resize(first_place, (int(first_place.shape[1] * RATE), int(first_place.shape[0] * RATE)))
        second_place = cv2.resize(second_place, (int(second_place.shape[1] * RATE), int(second_place.shape[0] * RATE)))
        cv2.imwrite("z://resize_after_firstbot.png", first_place)

        # マスキング処理
        # first_red_mask = OpenCVUtil._create_red_mask(first_place)
        # second_red_mask = OpenCVUtil._create_red_mask(second_place)
        # first_place = cv2.bitwise_and(first_place, first_place, mask=first_red_mask)
        # second_place = cv2.bitwise_and(second_place, second_place, mask=second_red_mask)
        #
        # first_place = cv2.cvtColor(first_place, cv2.COLOR_BGR2GRAY)
        # second_place = cv2.cvtColor(second_place, cv2.COLOR_BGR2GRAY)
        # first_place = cv2.GaussianBlur(first_place, (11, 11), 0)
        # second_place = cv2.GaussianBlur(second_place, (11, 11), 0)
        #
        # first_place = cv2.adaptiveThreshold(
        #     first_place, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 3)
        # second_place = cv2.adaptiveThreshold(
        #     second_place, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 3)

        # first_place[np.where((first_place == black).all(axis=2))] = white
        # second_place[np.where((second_place == black).all(axis=2))] = white

        akaze = cv2.AKAZE_create()

        # concat_img = cv2.hconcat([first_place, second_place])

        blocks = []
        for i in range(0, 3):
            concat_height = first_place.shape[0]
            concat_block_width = int(first_place.shape[1] / 3)
            blocks.append(first_place[0:concat_height, i * concat_block_width: (i + 1) * concat_block_width])
        for i in range(0, 3):
            concat_height = second_place.shape[0]
            concat_block_width = int(second_place.shape[1] / 3)
            blocks.append(second_place[0:concat_height, i * concat_block_width: (i + 1) * concat_block_width])

        for i, block in enumerate(blocks):
            cv2.imwrite("z://block_" + str(i) + ".png", block)
        first_kp, first_des = akaze.detectAndCompute(first_place, None)
        second_kp, second_des = akaze.detectAndCompute(second_place, None)
        cv2.imwrite("z://firstbot.png", first_place)
        cv2.imwrite("z://secondbot.png", second_place)
        # for j, rect in enumerate(rects):
        #     roi = (rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
        #     clipped = target_img[roi[1]: roi[3], roi[0]: roi[2]]
        #     cv2.imwrite("z://aa/rect" + str(j) + ".png", clipped)
        #     target_kp, target_des = akaze.detectAndCompute(clipped, None)

        bf = cv2.BFMatcher()
        for pic, block in enumerate(blocks):
            block_kp, block_des = akaze.detectAndCompute(block, None)
            more_score = 0
            more_type = ""
            for i, des in enumerate(OpenCVUtil.descriptors):
                matches = bf.knnMatch(des, block_des, k=2)

                good = []
                for m, n in matches:
                    if m.distance < 0.5 * n.distance:
                        good.append([m])

                # debug
                out1 = cv2.drawKeypoints(OpenCVUtil.images[i], OpenCVUtil.key_points[i], None)
                out2 = cv2.drawKeypoints(block, block_kp, None)
                img_kaze = cv2.drawMatchesKnn(out1, OpenCVUtil.key_points[i], out2, block_kp, good, None, flags=2)
                cv2.imwrite("z://type" + str(i) + '.png', out1)
                cv2.imwrite('z://img_gray_debug_1' + str(pic) + str(i) + '.png', img_kaze)

                logger.info(str(i) + " type : " + str(len(good)))
                if len(good) > more_score:
                    if i >= len(constant_list()):
                        logger.info(constant_list()[i - len(constant_list())])
                        # match_types.append(constant_list()[i])
                        more_score = len(good)
                        more_type = constant_list()[i - len(constant_list())]
                    else:
                        logger.info(constant_list()[i])
                        # match_types.append(constant_list()[i])
                        more_score = len(good)
                        more_type = constant_list()[i]

                # cv2.imwrite('target.png', out2)
            match_types.append(more_type)

        return match_types

    @staticmethod
    def _find_rectangle(image) -> ():
        logger.debug("find rectangle start")
        img1 = image  # cv2.imread(image)
        # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img1 = cv2.GaussianBlur(img1, (11, 11), 0)
        # img1 = cv2.adaptiveThreshold(img1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 3)

        # BGRでの色抽出
        bgrLower = np.array([110, 110, 110])    # 抽出する色の下限(BGR)
        bgrUpper = np.array([200, 200, 200])    # 抽出する色の上限(BGR)
        img_mask = cv2.inRange(img1, bgrLower, bgrUpper)  # BGRからマスクを作成
        result = cv2.bitwise_and(img1, img1, mask=img_mask)  # 元画像とマスクを合成
        height = result.shape[0]
        width = result.shape[1]

        # result = cv2.GaussianBlur(result, (11, 11), 0)
        # result = cv2.adaptiveThreshold(result, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 3)
        cv2.imwrite("z://find_rect.png", result)

        black_pixel = 0
        rect_start_pixel_w = -1
        rect_start_pixel_h = -1
        end = False
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

                    # 背景色が黒以外で連続横幅7割続いた場合は神魔の範囲とみなす
                    black_pixel += 1
                    if black_pixel > int(width * 0.8):
                        end = True
                        left = rect_start_pixel_w, rect_start_pixel_h
                        break

            rect_start_pixel_w = -1
            rect_start_pixel_h = -1
            black_pixel = 0
            if end is True:
                break
        rect_start_pixel_w = -1
        rect_start_pixel_h = -1
        end = False
        black_pixel = 0
        for h in range(height - int(height / 10), 0, -1):
            for w in range(width - 1, 0, -1):
                b = result[h, w][0]
                g = result[h, w][1]
                r = result[h, w][2]
                if b != 0 and g != 0 and r != 0:
                    logger.info("[" + str(w) + "," + str(h) + "] " + str(b) + ", " + str(g) + ", " + str(r))
                    if rect_start_pixel_w == -1:
                        rect_start_pixel_w = w
                        rect_start_pixel_h = h
                    # 背景色が黒以外で連続横幅7割続いた場合は神魔の範囲とみなす
                    black_pixel += 1
                    if black_pixel > int(width * 0.8):
                        end = True
                        right = rect_start_pixel_w, rect_start_pixel_h
                        break
            rect_start_pixel_w = -1
            rect_start_pixel_h = -1
            black_pixel = 0
            if end is True:
                break

        return left, right

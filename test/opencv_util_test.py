import cv2
import numpy as np

from utils.opencv_util import OpenCVUtil


# def test_match():
#     OpenCVUtil.init_load()
#
#     img1 = cv2.imread("../data/small/aaweapon_type_1.png", cv2.COLOR_BGR2GRAY)
#     img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#     img2 = cv2.imread("../data/test.png", cv2.COLOR_BGR2GRAY)
#     img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#     akaze = cv2.AKAZE_create()
#
#     kp1, des1 = akaze.detectAndCompute(img1_gray, None)
#     out = cv2.drawKeypoints(img1_gray, kp1, None)
#     cv2.imshow("mutch_image_src", out)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     height = img2_gray.shape[0]
#     width = img2_gray.shape[1]
#     img2_gray_big = cv2.resize(img2_gray, (int(width * 5), int(height * 3)))
#     kp2, des2 = akaze.detectAndCompute(img2_gray_big, None)
#     out2 = cv2.drawKeypoints(img2_gray_big, kp2, None)
#     cv2.imshow("mutch_image_src2", out2)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#     bf = cv2.BFMatcher()
#     matches = bf.knnMatch(des1, des2, k=2)
#     good = []
#     for m, n in matches:
#         if m.distance < 0.4 * n.distance:
#             good.append([m])
#
#     img_kaze = cv2.drawMatchesKnn(out, kp1, out2, kp2, good, None, flags=2)
#
#     # 結果の表示
#     cv2.namedWindow("mutch_image_src", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
#     cv2.imshow("mutch_image_src", img_kaze)
#
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


def test_image_mask():
    img1 = cv2.imread("z://Screenshot_20191222-185148.jpg")
    # BGRでの色抽出
    # black = [0, 0, 0]
    red = [0, 0, 255]
    # white = [255, 255, 255]
    bgrLower = np.array([110, 110, 110])    # 抽出する色の下限(BGR)
    bgrUpper = np.array([200, 200, 200])    # 抽出する色の上限(BGR)
    img_mask = cv2.inRange(img1, bgrLower, bgrUpper)  # BGRからマスクを作成
    # result = img1[np.where((img1 == img_mask).all(axis=2))] = red
    result = cv2.bitwise_and(img1, img1, mask=img_mask)  # 元画像とマスクを合成
    height = result.shape[0]
    width = result.shape[1]

    end = False
    for h in range(0, height - 1):
        for w in range(0, width - 1):
            b = result[h, w][0]
            g = result[h, w][1]
            r = result[h, w][2]
            if b != 0 and g != 0 and r != 0:
                print("-->[" + str(w) + "," + str(h) + "] " + str(b) + ", " + str(g) + ", " + str(r))
                end = True
                left = w, h
                break
        if end is True:
            break
    end = False
    for h in range(height - int(height / 10), 0, -1):
        for w in range(width - 1, 0, -1):
            b = result[h, w][0]
            g = result[h, w][1]
            r = result[h, w][2]
            if b != 0 and g != 0 and r != 0:
                print("->[" + str(w) + "," + str(h) + "] " + str(b) + ", " + str(g) + ", " + str(r))
                end = True
                right = w, h
                break
        if end is True:
            break

    rect_img = img1[left[1]:right[1], left[0]:right[0]]
    rect_img = rect_img[245:285, 177:270]
    cv2.imwrite("z://rect.jpg", rect_img)
    # print(result[0, 0])
    cv2.namedWindow("mutch_image_src", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
    cv2.imshow("mutch_image_src", rect_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

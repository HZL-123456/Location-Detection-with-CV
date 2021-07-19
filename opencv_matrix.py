import cv2
import numpy as np
import math


def getAreaMax_contour(contours, area_min=5):
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = None

    for c in contours:  # 历遍所有轮廓
        contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > area_min:
                area_max_contour = c

    return area_max_contour, contour_area_max  # 返回最大的轮廓


def colors_identify(img):
    color_range = {
        'black': [(125, 125, 125), (255, 255, 255)],
    }

    global color_list, COLOR
    global cylinder_red_finish, cylinder_green_finish, cylinder_blue_finish

    frame_gaussianblur = cv2.GaussianBlur(img, (3, 3), 0)  # 高斯模糊
    frame_lab = cv2.cvtColor(frame_gaussianblur, cv2.COLOR_BGR2LAB)  # 将图片转换到LAB空间
    max_area = 0
    mask = cv2.inRange(frame_lab, color_range['black'][0], color_range['black'][1])  # 对原图像和掩模进行位运算
    opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # 开运算
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # 闭运算
    contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓
    areaMax_contour, area_max = getAreaMax_contour(contours)  # 找出最大轮廓
    if areaMax_contour is not None:
        if area_max > max_area:  # 找最大面积
            max_area = area_max
            areaMax_contour_max = areaMax_contour
    print(max_area)
    if max_area != 0 and max_area >= 100:
        ((black_line_centerx, centerY), rad) = cv2.minEnclosingCircle(areaMax_contour_max)  # 获取最小外接圆
        black_line_centerx, centerY, rad = int(black_line_centerx), int(centerY), int(rad)  # 获取圆心，半径
        cv2.circle(img, (black_line_centerx, centerY), rad, (0, 255, 0), 2)  # 画圆
        cv2.imshow('Result', img)
        print(black_line_centerx // 50, centerY // 50)
        return True
    return False


a = [[1, 1, 0, 0, 1, 0, 0],
     [1, 1, 1, 0, 1, 0, 0],
     [1, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 1, 0],
     [1, 1, 1, 1, 0, 1, 0],
     [0, 0, 0, 1, 0, 1, 0]]

a = np.array(a, dtype=np.uint8)
a[a == 1] = 255
grayImage = cv2.resize(a, (300, 350))
grayImage[grayImage < 150] = 0
# cv2.imshow('GrayImage', grayImage)
IMG_OUT = cv2.cvtColor(grayImage, cv2.COLOR_GRAY2RGB)
colors_identify(IMG_OUT)
cv2.waitKey(0)
cv2.destroyAllWindows()

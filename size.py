# -*- coding: utf-8 -*-

import cv2
import numpy as np

# 导入模板
template_unknow = cv2.imread('image\unknow.png', 0)
template_know = cv2.imread('image\\template\\know.png', 0)
template_1 = cv2.imread('image\\template\\1.png', 0)
template_2 = cv2.imread('image\\template\\2.png', 0)
template_3 = cv2.imread('image\\template\\3.png', 0)
template_4 = cv2.imread('image\\template\\4.png', 0)
template_5 = cv2.imread('image\\template\\5.png', 0)
template_6 = cv2.imread('image\\template\\6.png', 0)
template_7 = cv2.imread('image\\template\\7.png', 0)
list_template = [template_unknow, template_know, template_1, template_2, template_3, template_4, template_5, template_6,
                 template_7]

# 模板对应矩阵中的数字
dict_template = {0: -1, 1: -3, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8}

# 模板匹配阈值
list_threshold = [0.8, 0.9, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.8]

'''
定义矩阵中数字：
unknow -1
blank -3
mine 1
num original_num+1
possiblity 0<=p<1

threshold:
unknow 0.8 yes,it's unknow
know 0.90
1 0.85
2 0.85
3 0.85
4 0.85
5 0.85
6 0.85

'''

large_scale = {'size': 'large', 'x_size': 30, 'y_size': 16, 'mine': 99, 'start_x': 223, 'start_y': 145, 'end_x': 1696,
               'end_y': 931}
for x in range(30):
    for y in range(16):
        large_scale[(x, y)] = [248 + x * 49, 170 + y * 49]

middle_scale = {'size': 'middle', 'x_size': 16, 'y_size': 16, 'mine': 40, 'start_x': 567, 'start_y': 145, 'end_x': 1352,
                'end_y': 930}
for x in range(16):
    for y in range(16):
        middle_scale[(x, y)] = [588 + x * 49, 168 + y * 49]

square = {'length': 49, 'width': 49}


# 获取游戏规模函数，根据模板匹配获得的第一个匹配点的横坐标确定游戏规模，返回dictionary
def get_size(image_gray, template):
    res = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.85
    loc = np.where(res >= threshold)
    match_cord = loc[::-1]
    f_coordinate = [match_cord[0][0], match_cord[1][0]]
    # print(f_coordinate)
    if f_coordinate[0] > large_scale['start_x'] + square['length']:
        return middle_scale
    elif f_coordinate[0] > large_scale['start_x'] - square['length']:
        return large_scale
    else:
        return 0


# 判断指定区域内模板是否匹配
def template_fit(roi_gray, template, threshold):
    res = cv2.matchTemplate(roi_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        return 1
    else:
        return -1


# 更新数字矩阵
def update_matrix(img_gray, matrix, game_scale, square, list_template, list_threshold):
    for i in range(game_scale['y_size']):
        for j in range(game_scale['x_size']):
            if matrix[i][j] == -1 or (matrix[i][j] < 1 and matrix[i][j] > 0):
                roi = img_gray[
                      game_scale['start_y'] + square['length'] * i - 1: game_scale['start_y'] + square['length'] * (
                      i + 1) + 1,
                      game_scale['start_x'] + square['width'] * j - 1: game_scale['start_x'] + square['width'] * (
                      j + 1) + 1]
                for k in range(len(list_template)):
                    if template_fit(roi, list_template[k], list_threshold[k]) == 1:
                        # print i,j,k
                        matrix[i][j] = dict_template[k]
                        break

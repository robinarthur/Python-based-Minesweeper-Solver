# -*- coding: utf-8 -*-

import numpy as np
import sympy
import random

matrix_large = np.ones((16, 30))*-1
matrix_middle = np.ones((16, 16))*-1
UNKNOW = -1.
IS_MINE = 1.


# 返回某坐标周围元素位置,返回list，为周围元素位置
def elem_around(matrix, i, j):
    y_size, x_size = matrix.shape
    list_elem = []
    for k in range(-1, 2):
        for l in range(-1, 2):
            if i+k < 0 or i+k >= x_size or j+l < 0 or j+l >= y_size or (k == 0 and l == 0):
                continue
            list_elem.append([i+k, j+l])
    return list_elem


# 简单排雷方法，根据雷数和周围情况判定是\不是雷,返回新增的确定是雷\不是雷格数
def flag_ez(matrix, list_mine, list_not_mime):
    y_size, x_size = matrix.shape
    for i in range(x_size):
        for j in range(y_size):
            is_mine_num = 0
            sum_unknow_num = 0
            list_unknow = []
            if matrix[j][i] > 1:
                list_elem = elem_around(matrix, i, j)
                elem_num = len(list_elem)
                mine_num = matrix[j][i] - 1  # 真实雷数=数字-1
                for elem in list_elem:
                    x, y = elem
                    assert x < 30 and y < 16, (x, y)
                    if matrix[y][x] == IS_MINE:
                        is_mine_num += 1
                    if matrix[y][x] == UNKNOW or (matrix[y][x] < 1 and matrix[y][x] > 0):
                        sum_unknow_num += 1
                        list_unknow.append([x, y])
                # 若未知格数=剩余雷数=总雷数-已确定雷数 ,则未知格均为雷,参数list_mine返回确定是雷的位置坐标
                if mine_num - is_mine_num == sum_unknow_num:
                    for elem in list_unknow:
                        x, y = elem
                        matrix[y][x] = IS_MINE
                        if list_mine.count([x, y]) == 0:
                            list_mine.append([x, y])
                # 若总雷数=已确定雷数，且未知格数>0，则未知格均不是雷，参数list_not_mine返回确定不是雷的位置坐标
                elif mine_num == is_mine_num and sum_unknow_num > 0:
                    for elem in list_unknow:
                        x, y = elem
                        list_not_mime.append([x, y])


# 中级排雷方法，联立方程求解，约化增广矩阵为阶梯型矩阵,参数list返回排雷后确定是\不是雷的坐标
def flag_middle(matrix, list_mine, list_not_mine):
    y_size, x_size = matrix.shape
    matrix_w = 0
    d = {}
    left_list = [[]]
    right_matrix = []
    matrix_h = 0
    for i in range(x_size):
        for j in range(y_size):
            is_mine_num = 0
            sum_unknow_num = 0
            list_unknow = []
            if matrix[j][i] > 1:
                list_elem = elem_around(matrix, i, j)
                elem_num = len(list_elem)
                mine_num = matrix[j][i] - 1  # 真实雷数=数字-1
                for elem in list_elem:
                    x, y = elem
                    assert x < 30 and y < 16, (x, y)
                    if matrix[y][x] == IS_MINE:
                        is_mine_num += 1
                    if matrix[y][x] == UNKNOW or ( matrix[y][x] < 1 and matrix[y][x] > 0 ):
                        sum_unknow_num += 1
                        list_unknow.append([x, y])
                mine_remainder = mine_num - is_mine_num
                if mine_remainder > 0:
                    right_matrix.append(mine_remainder)
                    for elem in list_unknow:
                        x, y = elem  # 将坐标与变量X 对应，列入方程
                        if d.get((x, y), -1) == -1:   # 若坐标[x,y]未出现过，设为变量X sub matrix_w
                            d[x, y]=[matrix_w]
                            d[matrix_w] = [x, y]
                            matrix_w += 1   # matrix_w指向下一个坐标，即矩阵宽度
                        left_list[matrix_h].append(d[x, y])
                    left_list.append([])
                    matrix_h += 1   # matrix_h指向下一个坐标，即矩阵高度

    left_matrix = np.zeros((matrix_h, matrix_w))
    for i in range(matrix_h):
        for j in left_list[i]:
            left_matrix[i][j] = 1
    ans, index = sympy.Matrix(np.column_stack((left_matrix,right_matrix))).rref()
    ans_array = np.asarray(ans)
    h, w = ans_array.shape
    '''
    print('h:',h)
    print('w:',w)
    print('matrix_h:',matrix_h)
    print('matrix_w:',matrix_w)
    '''
    one = []
    left_reduced = ans_array[0:matrix_h, 0:matrix_w]
    right_reduced = ans_array[0:matrix_h, matrix_w]
    for i in range(matrix_h):
        if right_reduced[i] == 0:   # 若化简后的某一行解为0，且该行的约化矩阵不存在为-1的值，则该行值为1的位置所对应的格点一定不是雷
            minus_one = 0
            for j in range(matrix_w):
                if left_reduced[i][j] == -1:
                    minus_one += 1
                    break
                else:
                    pass
            if minus_one == 0:
                for j in range(matrix_w):
                    if left_reduced[i][j] == 1:
                        one.append(j)
                for elem in one:
                    if list_not_mine.count(d[int(elem)]) == 0:
                        list_not_mine.append(d[int(elem)])

        elif right_reduced[i] == 1:  # 若某一行解为1，且改行的约化矩阵只存在一个1，则那个1一定是雷
            not_zero = 0
            not_zero_loc = None
            for j in range(matrix_w):
                if left_reduced[i][j] != 0:
                    not_zero += 1
                elif left_reduced[i][j] == 1:
                    not_zero_loc = j
            if not_zero == 1 and not_zero_loc != None:
                if list_mine.count(d[not_zero_loc]) == 0:
                    x, y = d[not_zero_loc]
                    matrix[y][x] = IS_MINE
                    list_mine.append([x, y])
                    # print('mine:',(x,y))

    if len(list_mine) == 0 and len(list_not_mine) == 0:  # 若没有可以确定的位置，随机点一个
        random_num = random.randint(0, matrix_w - 1)
        list_not_mine.append(d[random_num])
        # print('Guess:',d[random_num])

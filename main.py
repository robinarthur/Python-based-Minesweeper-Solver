# -*- coding: utf-8 -*-
import cv2
import numpy as np
import size as sz
import win32 as winf
import time
import cnt as cnt
import PIL2CV as pv
import win32gui

#打开Minesweeper.exe,默认路径 C:\Program Files\Microsoft Games\Minesweeper\Minesweeper.exe
winf.openMW()

winf.switch()
time.sleep(1)

#模拟按键截图，将图像从PIL类对象转为OpenCv类对象
im_pil = winf.ptr()
im_cv = pv.pil2cv(im_pil)
img_gray = cv2.cvtColor(im_cv, cv2.COLOR_BGR2GRAY)

#获取游戏规模
game_scale = sz.get_size(img_gray,sz.template_unknow)

#初始化游戏数据矩阵
matrix = np.ones((game_scale['y_size'],game_scale['x_size'])) * -1

#开局，随机点击一个格子
winf.random_click(game_scale,sz.square)
time.sleep(0.4)

#数据初始化
list_mine=[]
list_not_mine=[]
left_click = 0
right_click = 0
mine_num = 0

#判断游戏是否结束
while win32gui.FindWindow(0,u'游戏失败') == 0 and win32gui.FindWindow(0,u'游戏胜利') == 0:

    time.sleep(0.02)

    winf.switch()
    #重新截图，更新矩阵
    im_pil = winf.ptr()
    time.sleep(0.02)
    im_cv = pv.pil2cv(im_pil)
    img_gray = cv2.cvtColor(im_cv, cv2.COLOR_BGR2GRAY)
    sz.update_matrix(img_gray,matrix,game_scale,sz.square,sz.list_template,sz.list_threshold)

    #简单策略
    cnt.flag_ez(matrix,list_mine,list_not_mine)

    #低级策略无法判断，使用中级策略
    if len(list_mine) == 0 and len(list_not_mine) == 0:
        cnt.flag_middle(matrix,list_mine,list_not_mine)

    #鼠标点击
    for i in range(len(list_mine)):
        x,y = list_mine.pop()

    for i in range(len(list_not_mine)):
        x,y = list_not_mine.pop()
        x,y = game_scale[(x,y)]
        winf.mouse_click(x,y,'left')
        left_click += 1
        time.sleep(0.02)




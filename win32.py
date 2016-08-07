# -*- coding: utf-8 -*-

import win32api
import win32gui
import win32con
import time
import random
from PIL import ImageGrab

# make sure Pillow 2.7.0 is installed !!!
# 2.7.0 !!!
# 因为高版本Pillow的ImageGrab对剪贴板的BMP图像格式的支持有问题

#打开MinesWeeper.exe
def openMW(str = 'C:\Program Files\Microsoft Games\Minesweeper\Minesweeper.exe'):
    win32api.ShellExecute(0, 'open', str, '', '', 0)
    time.sleep(1)

#模拟鼠标操作,接受参数为某位置在屏幕的坐标，点击左键\右键
def mouse_click(x,y,str):

    # win10对1080P屏幕默认进行比例为150%的DPI缩放，需要对坐标进行修正，即修正坐标=原坐标/1.5
    dpi_fix_x = int(x/1.5) - 3
    dpi_fix_y = int(y/1.5) - 3

    win32api.SetCursorPos((dpi_fix_x,dpi_fix_y))
    #win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,x,y)
    if str == 'left':
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        return 1
    elif str == 'right':
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0,0,0)
        return 1
    else :
        return 1

#开局随意点击一位置
def random_click(game_scale,square):
    ran_x = random.randint(game_scale['start_x'] + 10,game_scale['end_x'] - 10)
    ran_y = random.randint(game_scale['start_y'] + 10,game_scale['end_y'] - 10)
    #print ran_x,ran_y
    #x = int(game_scale['start_x'] + ran_x * square['width'] - 10)
    #y = int(game_scale['start_y'] + ran_y * square['length'] - 10)
    mouse_click(ran_x,ran_y,'left')

#窗口操作
def switch():
    wdname1 = u"扫雷"
    w1hd = win32gui.FindWindow(0, wdname1)
    win32gui.SetForegroundWindow(w1hd)

#模拟键盘操作截图,从剪贴板获取图像并返回
def ptr():
    Ptr_num=44
    win32api.keybd_event(Ptr_num,0,0,0)
    time.sleep(0.04)
    win32api.keybd_event(Ptr_num,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(0.04)
    im = ImageGrab.grabclipboard()
    return im


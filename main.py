import tkinter as tk
import mysql.connector
import re
import cv2
import pyautogui
import time
import datetime
from datetime import datetime, timedelta
from pynput.keyboard import Key, Controller, Listener
from pynput import keyboard
import keyboard
import requests
import ctypes
from datetime import datetime
import sys
from pynput import keyboard
import numpy as np
import webbrowser
import threading

# 连接到 MySQL 数据库
mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

keyboard = Controller()

keyf = "f"
qwjn = 0
duihua = 1
from PIL import ImageGrab




stop_event = threading.Event()  # 终止功能的变量
current_version = "1.0.1"  # 当前版本号
mycursor = mydb.cursor()
query = "SELECT banben FROM banben "  # 替换为您的表名和条件
mycursor.execute(query)
version = mycursor.fetchone()
if version:
    banben_value = version[0]
query2 = "SELECT banben2 FROM banben "  # 替换为您的另一个表名和条件
mycursor.execute(query2)
version2 = mycursor.fetchone()  # fetchone()返回查询结果的第二行
if version2:
    banben_value2 = version2[0]
version=banben_value
version2=banben_value2
mycursor.close()
#mydb.close()

MIN_USERNAME_LENGTH = 3  # 限制用户名最短为3
MAX_USERNAME_LENGTH = 20  # 限制用户名最长为20
MIN_PASSWORD_LENGTH = 6  # 限制用户密码最短为6

import tkinter as tk
from tkinter import messagebox
import hashlib


# 登录函数
def login():
    # 创建数据库游标对象
    cursor = mydb.cursor()
    # 获取用户名输入框的值
    username = login_username_entry.get()
    # 获取密码输入框的值
    password = login_password_entry.get()

    # 执行SQL查询语句，查询数据库中用户名对应的密码和日期
    cursor.execute('SELECT password, date FROM User WHERE username=%s', (username,))
    # 获取查询结果
    result = cursor.fetchone()
    # 关闭数据库游标
    cursor.close()

    # 如果查询结果不为空
    if result:
        # 从数据库中获取日期
        db_date = result[1]
        # 获取当前时间
        current_date = datetime.now()
        # 获取当前时间的整数部分（忽略毫秒）
        rounded_time = current_date - timedelta(microseconds=current_date.microsecond)
        # 对输入的密码进行SHA-256散列
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # 如果散列后的密码与数据库中存储的密码匹配，并且数据库中的日期大于当前时间（未过期）
        if hashed_password == result[0] and db_date > rounded_time:
            # 打印登录成功的信息，并显示欢迎信息和过期时间
            print("登录成功！欢迎，" + username)
            show_message("登录成功", ("欢迎，" + username, "过期时间", (str(db_date))))
            # 销毁主窗口，并显示下一个界面
            root.destroy()
            nsh_tk()
            return True  # 返回True表示登录成功
        # 如果数据库中的日期小于当前时间（已过期）
        elif db_date < rounded_time:
            # 打印账户过期的信息，并显示过期时间，然后结束函数执行
            print("账户过期")
            show_message("登录失败", ("您的账户过期于", (str(db_date)), "请续费"))
            return
        else:  # 如果以上条件都不满足，说明出现了其他错误
            print("未知错误！")  # 打印未知错误的提示信息，并结束函数执行
            show_message("登录失败", "未知错误")
            return False  # 返回False表示登录失败
    else:  # 如果查询结果为空，说明用户名或密码错误
        print("用户名或密码错误！")  # 打印用户名或密码错误的提示信息，并结束函数执行
        show_message("登录失败", "用户名或密码错误")
        return False  # 返回False表示登录失败


# 登录成功和失败弹窗
def show_message(title, message):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo(title, message)  # 显示消息框
    root.destroy()  # 销毁窗口


def show_gongneng(title, message):
    window = tk.Tk()
    window.withdraw()  # 隐藏主窗口
    messagebox.showinfo(title, message)  # 显示消息框
    window.destroy()  # 销毁窗口


# 创建注册界面函数
def ZC_tk():
    def register_user():
        # 获取注册窗口的输入
        reg_email = zc_email_entry.get()  # 获取邮箱输入框的值
        reg_activation_code = zc_cdk_entry.get()  # 获取激活码输入框的值
        reg_username = zc_username_entry.get()  # 获取用户名输入框的值
        reg_password = zc_password_entry.get()  # 获取密码输入框的值
        reg_confirm_password = zc_password_qr_entry.get()  # 获取确认密码输入框的值

        # 从 MySQL 数据库获取验证的代码
        cursor = mydb.cursor()  # 创建数据库游标对象
        cursor.execute("SELECT CDK FROM CDK WHERE CDK = %s", (reg_activation_code,))  # 执行SQL查询语句，查询数据库中激活码对应的CDK
        result = cursor.fetchone()  # 获取查询结果
        # 简单的验证
        if not all(
                [reg_email, reg_activation_code, reg_username, reg_password, reg_confirm_password]):  # 检查所有字段是否都已填写
            messagebox.showerror("错误", "所有字段都必须填写！")  # 如果未填写，显示错误信息并返回
            return
            # 检查用户名长度
        if not (MIN_USERNAME_LENGTH <= len(reg_username) <= MAX_USERNAME_LENGTH):  # 检查用户名长度是否在规定范围内
            messagebox.showerror("错误",
                                 f"用户名长度必须在{MIN_USERNAME_LENGTH}到{MAX_USERNAME_LENGTH}个字符之间！")  # 显示错误信息并返回
            return
        if len(reg_password) < MIN_PASSWORD_LENGTH:  # 检查密码长度是否达到最小要求
            messagebox.showerror("错误", f"密码长度必须至少为{MIN_PASSWORD_LENGTH}个字符！")  # 显示错误信息并返回
            return
        if reg_password != reg_confirm_password:  # 检查两次输入的密码是否一致
            messagebox.showerror("错误", "密码不匹配！")  # 如果不一致，显示错误信息并返回
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", reg_email):  # 使用正则表达式验证邮箱格式是否正确
            messagebox.showerror("错误", "请输入有效的邮箱地址！")  # 如果邮箱格式不正确，显示错误信息并返回
            return
        hashed_password = hashlib.sha256(reg_password.encode()).hexdigest()  # 对密码进行SHA-256散列加密
        if result:  # 如果查询结果不为空，表示激活码存在
            cursor.execute("SELECT COUNT(*) FROM CDK WHERE CDK = %s AND SY = 1",
                           (reg_activation_code,))  # 执行SQL查询语句，统计激活码是否已被使用
            count = cursor.fetchone()[0]  # 获取查询结果中的计数
            if count > 0:  # 如果计数大于0，表示激活码已被使用
                messagebox.showerror("错误", "该激活码已使用！")  # 显示错误信息并返回
                return  # 结束函数执行
            else:  # 激活码未使用，注册成功，并将激活码改为已使用状态
                # 检查用户名是否已存在
                cursor.execute("SELECT COUNT(*) FROM User WHERE username = %s", (reg_username,))
                username_count = cursor.fetchone()[0]
                if username_count > 0:  # 如果用户名已存在，不消耗激活码并提示用户
                    messagebox.showerror("错误", "用户名已存在！不消耗激活码。")
                    return
                else:  # 用户名不存在，执行激活码更新和用户添加操作
                    # 将指定激活码设为已使用
                    cursor.execute("UPDATE CDK SET SY = 1 WHERE CDK = %s", (reg_activation_code,))
                    mydb.commit()

                    # 获取用户输入的激活码时长
                    cursor.execute("SELECT date FROM CDK WHERE CDK = %s", (reg_activation_code,))
                    row = cursor.fetchone()
                    if row:
                        # 获取date数据
                        date_from_db = row[0]
                        print(date_from_db)

                        # 计算新的日期
                        current_date = datetime.now()
                        new_date = current_date + timedelta(days=date_from_db)
                        print(new_date)

                        # 添加用户信息到数据库
                        add_user_query = "INSERT INTO User (username, password, email, date) VALUES (%s, %s, %s, %s)"
                        cursor.execute(add_user_query, (reg_username, hashed_password, reg_email, new_date))
                        mydb.commit()
                    cursor.close()
                    messagebox.showinfo("成功", "注册成功！")
                    zc_tk.destroy()  # 关闭注册窗口
        else:  # 如果没有这个激活码，提示激活码错误
            messagebox.showerror("错误", "激活码错误！")
        cursor = mydb.cursor()
        cursor.execute("SELECT CDK FROM CDK WHERE CDK = %s", (reg_activation_code,))
        result = cursor.fetchone()

    zc_tk = tk.Toplevel()
    zc_tk.title("注册窗口")  # 窗口名字
    zc_tk.geometry("350x350")  # 窗口大小
    zc_tk.iconbitmap("tb.ico")  # 窗口图标
    zc_frame = tk.Frame(zc_tk)
    zc_frame.pack()
    zc_biaoqian = tk.Label(zc_tk, text="注册界面")
    zc_biaoqian.pack()
    zc_email = tk.Label(zc_tk, text="邮箱:")
    zc_email.pack()
    zc_email_entry = tk.Entry(zc_tk)
    zc_email_entry.pack()
    zc_cdk = tk.Label(zc_tk, text="激活码:")
    zc_cdk.pack()
    zc_cdk_entry = tk.Entry(zc_tk)
    zc_cdk_entry.pack()
    zc_username = tk.Label(zc_tk, text="账号:")
    zc_username.pack()
    zc_username_entry = tk.Entry(zc_tk)
    zc_username_entry.pack()
    zc_password = tk.Label(zc_tk, text="密码:")
    zc_password.pack()
    zc_password_entry = tk.Entry(zc_tk)
    zc_password_entry.pack()
    zc_password_qr = tk.Label(zc_tk, text="确认密码:")
    zc_password_qr.pack()
    zc_password_qr_entry = tk.Entry(zc_tk)
    zc_password_qr_entry.pack()
    zc_button = tk.Button(zc_tk, text="注册", command=register_user)
    zc_button.pack()


def xf_tk():
    def xf_user():
        reg_xf_activation_code = xf_cdk_entry.get()
        reg_xf_username = xf_username_entry.get()
        reg_xfqr_username = xf_username_qr_entry.get()
        cursor = mydb.cursor()
        cursor.execute("SELECT CDK FROM CDK WHERE CDK = %s", (reg_xf_activation_code,))
        result = cursor.fetchone()

        # 简单的验证
        if not all([reg_xf_activation_code, reg_xf_username, reg_xfqr_username]):
            messagebox.showerror("错误", "所有字段都必须填写！")
            return
        if not (MIN_USERNAME_LENGTH <= len(reg_xf_username) <= MAX_USERNAME_LENGTH):
            messagebox.showerror("错误", f"用户名长度必须在{MIN_USERNAME_LENGTH}到{MAX_USERNAME_LENGTH}个字符之间！")
            return
        if reg_xf_username != reg_xfqr_username:
            messagebox.showerror("错误", "两次账号输入不同")
            return
        if result:  # 如果查询结果不为空，则表示激活码存在
            cursor.execute("SELECT COUNT(*) FROM CDK WHERE CDK = %s AND SY = 1", (reg_xf_activation_code,))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror("错误", "该激活码已使用！")
                return
            else:  # 激活码未使用，进行用户是否存在的判断
                # 检查用户名是否已存在
                cursor.execute("SELECT COUNT(*) FROM User WHERE username = %s", (reg_xf_username,))
                username_count = cursor.fetchone()[0]
                if username_count > 0:  # 如果用户名已存在则续费成功
                    #获取激活码的时长
                    cursor.execute("SELECT date FROM CDK WHERE CDK = %s", (reg_xf_activation_code,))
                    row = cursor.fetchone()
                    #获取用户剩余时长
                    cursor.execute("SELECT date FROM User WHERE username = %s", (reg_xf_username,))
                    row2 = cursor.fetchone()
                    #转化数据
                    date_time_obj = row2[0].strftime("%Y-%m-%d %H:%M:%S")
                    formatted_date_time = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S")
                    print(row)
                    print(formatted_date_time)
                    current_date = datetime.now()  # 查询当前时间
                    seconds = current_date.second
                    microseconds = current_date.microsecond
                    # 获取整秒部分
                    rounded_time = current_date - timedelta(microseconds=microseconds)
                    print(rounded_time)
                    if formatted_date_time > rounded_time:
                        date_from_row = row[0]
                        days_to_add = date_from_row
                        date = formatted_date_time + timedelta(days=days_to_add)
                        print(date)
                        query = f"UPDATE User SET date = %s WHERE username = %s"
                        cursor.execute(query, (date, reg_xf_username,))
                        cursor.execute("UPDATE CDK SET SY = 1 WHERE CDK = %s", (reg_xf_activation_code,))
                        mydb.commit()
                        cursor.close()
                        messagebox.showinfo("续费成功", "下次到期时间为" + str(date))
                        xf_tk.destroy()
                    else:
                        if row:
                            # 获取date数据
                            date_from_db = row[0]
                            print(date_from_db)
                            # 计算当前日期加上date数据的结果
                            current_date = datetime.now()
                            date = current_date + timedelta(days=date_from_db)
                            query = f"UPDATE User SET date = %s WHERE username = %s"
                            cursor.execute(query, (date, reg_xf_username,))
                            cursor.execute("UPDATE CDK SET SY = 1 WHERE CDK = %s", (reg_xf_activation_code,))
                            mydb.commit()
                            cursor.close()
                            messagebox.showinfo("续费成功", "下次到期时间为1" + str(date))
                            xf_tk.destroy()
                else:
                    messagebox.showerror("续费失败", "用户名不存在")
                    return
        else:  # 如果没有这个激活码，提示激活码错误
            messagebox.showerror("错误", "激活码错误！")

    xf_tk = tk.Toplevel()
    xf_tk.title("续费窗口")  # 窗口名字
    xf_tk.geometry("350x350")  # 窗口大小
    xf_tk.iconbitmap("tb.ico")
    xf_username = tk.Label(xf_tk, text="账号:")
    xf_username.pack()
    xf_username_entry = tk.Entry(xf_tk)
    xf_username_entry.pack()
    xf_username_qr = tk.Label(xf_tk, text="确认账号:")
    xf_username_qr.pack()
    xf_username_qr_entry = tk.Entry(xf_tk)
    xf_username_qr_entry.pack()
    xf_cdk = tk.Label(xf_tk, text="激活码:")
    xf_cdk.pack()
    xf_cdk_entry = tk.Entry(xf_tk)
    xf_cdk_entry.pack()
    xf_button = tk.Button(xf_tk, text="注册", command=xf_user)
    xf_button.pack()


# 检测和鼠标宏功能
def say_hello():
    # 欢迎使用
    print("欢迎使用")
    num = 0
    # 获取屏幕分辨率
    screen_width, screen_height = pyautogui.size()
    # 读取要匹配的图像
    image_path = '2.png'
    image = cv2.imread(image_path)
    # 将图像转换为灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 定义要截取的区域
    region = (1332, 675, 410, 69)
    # 创建SIFT特征检测器
    sift = cv2.SIFT_create()
    # 创建FLANN匹配器
    flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict())
    global should_continue
    # 计算要匹配图像的关键点和描述符
    kp1, des1 = sift.detectAndCompute(gray, None) # 创建BFMatcher对象

    while not stop_event.is_set():
        # 截取指定区域的屏幕截图
        screenshot = pyautogui.screenshot(region=region)
        # 将PIL图像转换为NumPy数组
        screenshot_np = np.array(screenshot)
        # 转换颜色空间为BGR
        screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        # 转换为灰度图像
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        # 计算截图区域的关键点和描述符
        kp2, des2 = sift.detectAndCompute(screenshot_gray, None)
        # 如果没有检测到特征点,则继续下一次循环
        if des2 is None:
            continue

        # 使用FLANN匹配器进行特征匹配
        matches = flann.knnMatch(des1, des2, k=2)
        good_matches = []
        # 根据距离比率筛选好的匹配
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)
        # 如果匹配数量大于等于30,则认为找到了目标图像
        if len(good_matches) >= 10:
            print("运行成功")
            # 移动鼠标并点击
            pyautogui.moveTo(1446, 709)
            pyautogui.click()
            should_continue = False
            return
        else:
            num += 1
            time.sleep(0.02)
            img_matches = cv2.drawMatches(gray, kp1, screenshot_gray, kp2, good_matches, None)
            cv2.imshow('Matches', img_matches)
            cv2.waitKey(1)

            print("在桌面上找不到图像,已运行:", num, "次")


def tz_gn():
    stop_event.set()
    show_gongneng("手动停止", "功能已经手动停止")
    print("此功能已停止")


def qd_gn():
    thread = threading.Thread(target=say_hello)
    thread.start()
    global stop_event
    if stop_event.is_set():
        print("函数已停止，准备重新启动...")
        stop_event.clear()  # 重置事件，以便重新启动函数
        thread = threading.Thread(target=say_hello, args=(stop_event,))
        thread.start()
    else:
        print("函数正在运行，无法重新启动...")





# 使用的界面
def on_home_key():
    """
    处理Home键按下事件
    """
    if version == version2 == current_version:
        status_label.config(text="欢迎使用")
        show_gongneng("启动成功", "点击确定后切换到游戏界面")
        qd_gn()
    elif version <= version2 != current_version:
        status_label.config(text="废弃版本请加群更新")
        show_gongneng("版本已废弃", "请加群更新软件")
    else:
        show_gongneng("版本已过期", "请加群更新软件")
        status_label.config(text="请加群更新软件")

def on_press(key):
    global key_pressed_state
    try:
        if key.char == 'Home':
            print('你按下了 Home 键!')
            on_home_key()
    except AttributeError:
        pass

def nsh_tk():
    listener = keyboard.Listener(on_press=on_press)
    listener_thread = threading.Thread(target=listener.start)
    listener_thread.start()

    window = tk.Tk()
    window.title("小福助手")
    window.geometry("300x200")
    window.iconbitmap("tb.ico")

    tk.Label(window, text="欢迎使用小福助手").grid(row=0, column=1)
    tk.Label(window, text="按下Home键启动程序").grid(row=2, column=1)
    tk.Button(window, text="点击我也可以", command=on_home_key).grid(row=3, column=1)
    tk.Button(window, text="停止", command=tz_gn).grid(row=3, column=2)
    tk.Label(window, text="交流群：413987981").grid(row=4, column=1)
    tk.Label(window, text="提示：每次运行结束都\n需要切换到小福助手再按下快捷键才可以使用").grid(row=5, column=1)
    tk.Label(window, text=f"最新版本号： {version2}\n当前版本号为：{current_version}").grid(row=6, column=1)

    global status_label
    status_label = tk.Label(window, text="")
    status_label.grid(row=7, column=1)

    window.mainloop()







# 创建主窗口
root = tk.Tk()
root.title("小福助手登录窗口")


# 暂无作用
def yc():
    root.withdraw()


# 打开购买激活码网站
def open_url():
    url = "http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=ztB0Po-rygNZuIhjKpO7_-VQXZFad6_O&authKey=r0%2BT9xRl8K7BCANdS2Za7ZKMhWix0zkcrDxi4GkClRXYC96PZFCqm5OEAiiyuiGT&noverify=0&group_code=413987981"  # 替换为你想要打开的网址
    webbrowser.open(url)


# 窗口名字
root.geometry("400x140")  # 窗口大小
root.iconbitmap("tb.ico")  # 窗口图标
login_frame = tk.Frame(root)
login_frame.pack()
login_label = tk.Label(login_frame, text="登录")
login_label.pack()
login_username_label = tk.Label(login_frame, text="用户名:")
login_username_label.pack(side=tk.LEFT)
login_username_entry = tk.Entry(login_frame)
login_username_entry.pack(side=tk.LEFT)
login_password_label = tk.Label(login_frame, text="密码:")
login_password_label.pack(side=tk.LEFT)
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.pack(side=tk.LEFT)
login_button = tk.Button(login_frame, text="登录", command=login)
login_button.pack()

root_ZC = tk.Button(text="注册", command=ZC_tk)
root_ZC.pack()
open_xf_button = tk.Button(text="续费", command=xf_tk)
open_xf_button.pack()
open_button = tk.Button(text="加群", command=open_url)
open_button.pack()

root.mainloop()

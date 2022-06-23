import tkinter as tk
import random

window_size = {1: '243x243', 2: '430x430', 3: '970x565'}
chlick_times = 0
lei_num = {1: 8, 2: 36, 3: 93}
block_size = {1: (9, 9), 2: (16, 16), 3: (21, 36)}
Not_Lei = set()
signed = list()


class Application(tk.Frame):
    # 父控件为root
    def __init__(self, master) -> None:
        super().__init__(master)
        self.photo = {'None': tk.PhotoImage(file='未踩格.jpg'),
            'Null': tk.PhotoImage(file='标记格.jpg'),
            'NaN': tk.PhotoImage(file='踩雷.jpg'),
            '0': tk.PhotoImage(file='0.jpg'),
            '1': tk.PhotoImage(file='1.jpg'),
            '2': tk.PhotoImage(file='2.jpg'),
            '3': tk.PhotoImage(file='3.jpg'),
            '4': tk.PhotoImage(file='4.jpg'),
            '5': tk.PhotoImage(file='5.jpg'),
            '6': tk.PhotoImage(file='6.jpg'),
            '7': tk.PhotoImage(file='7.jpg'),
            '8': tk.PhotoImage(file='8.jpg')}
        self.pack()
        self.master = master
        self.Label_1()
        self.Button_1 = tk.Button(
            self, text='开始游戏', command=self.Button_action_1)
        self.Button_1.pack()

    def Label_1(self):
        self.Label__1 = tk.Label(self, text='hello World!')
        self.Label__1.pack()

    def Button_action_1(self):
        self.Label__1.destroy()
        self.Button_1.destroy()
        self.choose()
        self.Button_1 = tk.Button(
            self, text='确认', command=self.Button_action_2)
        self.Button_1.pack()

    def choose(self):
        """
        显示单选框并设置按下按钮时回传数值
        """
        self.value = tk.IntVar()
        self.value.set(1)
        self.Rb1 = tk.Radiobutton(
            self, text='简单', variable=self.value, value=1)
        self.Rb1.pack()
        self.Rb2 = tk.Radiobutton(
            self, text='普通', variable=self.value, value=2)
        self.Rb2.pack()
        self.Rb3 = tk.Radiobutton(
            self, text='困难', variable=self.value, value=3)
        self.Rb3.pack()

    def Button_action_2(self):
        """
        toplevel的按钮,按下后传回当前单选框选中数值
        """
        self.Button_1.destroy()
        self.Rb1.destroy()
        self.Rb2.destroy()
        self.Rb3.destroy()
        global game_mode
        game_mode = self.value.get()
        self.master.geometry(window_size[game_mode])
        w, h = window_size[game_mode].split('x')
        self.config(width=w, height=h)
        self.pack()
        for r in range(block_size[game_mode][0]):
            for c in range(block_size[game_mode][1]):
                globals()['Block_'+str(r)+'_'+str(c)] = block(self, r, c)


class block(tk.Label):
    """
    雷格小方块
    """
    state = 'None'       # state 状态，state = 'None' 未被插旗，state = 'Null' 被插旗，state = 'NaN' 踩雷, state = [0,8]区间 分别为[0,8].jpg
    number = 0      # number 周围雷数，值从0-8
    Lei = False

    def __init__(self, master, row, column):
        self.row, self.column, self.master = row, column, master
        super().__init__(
            master, image=self.master.photo[self.state], relief='groove', border=1)
        self.image = self.master.photo[self.state]
        self.grid(row=row, column=column)
        self.bind("<ButtonPress-1>", self.image_Change_1)
        self.bind('<ButtonPress-3>', self.image_Change_2)

    def image_Change_1(self, envent):
        """检查是否位于插旗状况，若不是，则显示雷状态，并递归检测周围8格情况做出相应反应"""
        StateDetection(
            self.row, self.column)            # 检测是否是第一次点击，若是，则初始化棋盘，不是则跳过
        if self.state == 'Null':
            self.state = 'None'
            self.config(image=self.master.photo[self.state])
            self.image = self.master.photo[self.state]
            signed.remove((self.row, self.column))
        else:
            if self.Lei:            # 本身是雷时，踩雷，将雷全部暴露，游戏结束
                Show_All_End(self)      # 游戏终止程序
            else:  # 本身不是雷，将可显示区域全部显示
                if self.state == 'None':
                    ShowDetection(self.row, self.column)
                    Show(self.row, self.column, self)
                else:
                    # 统计是否周围被标记的方块是否与self.number相同
                    if self.number == signed_number(self.row, self.column):
                        ShowDetection(self.row, self.column)
                        Show(self.row, self.column, self)
                    else:
                        pass

    def image_Change_2(self, envet):       # 插旗与解除
        nm = 0
        if self.state == 'Null':        # 解除
            self.state = 'None'
            self.config(image=self.master.photo[self.state])
            self.image = self.master.photo[self.state]
            signed.remove((self.row, self.column))
        elif self.state == 'None':      # 插旗
            self.state = 'Null'
            self.config(image=self.master.photo[self.state])
            self.image = self.master.photo[self.state]
            signed.append((self.row, self.column))
        # 胜利检测
        for i in signed:
            if i in LEI_x_y:        # nm+1
                nm += 1
        if nm == lei_num[game_mode]:
            end(self)


def StateDetection(row, column):           # 状态检测算法，采用遍历.第一次按下棋盘时开始计算并返回周围的雷数写入实例里的
    global chlick_times
    if chlick_times == 0:
        block_x = list(range(block_size[game_mode][0]))
        block_y = list(range(block_size[game_mode][1]))
        lei = set()
        chlick_times += 1
        e = True
        while e:         # 随机产生雷
            x = random.choice(block_x)
            y = random.choice(block_y)
            if (x, y) != (row, column):
                lei.add((x, y))
            if len(lei) == lei_num[game_mode]:
                e = False
        global LEI_x_y
        LEI_x_y = list(lei)
        for i, j in LEI_x_y:
            globals()['Block_'+str(i)+'_'+str(j)].Lei = True
        for i in block_x:
            for j in block_y:
                if not globals()['Block_'+str(i)+'_'+str(j)].Lei:       # 非雷情况
                    x = range(i-1, i+2)
                    y = range(j-1, j+2)
                    for a in x:
                        for b in y:
                            try:
                                if globals()['Block_'+str(a)+'_'+str(b)].Lei:
                                    globals()['Block_'+str(i) +
                                              '_'+str(j)].number += 1
                            except:
                                pass


def ShowDetection(row, column):            # 显示检测算法，采用递归，将计算当前按下处的所有可显示位置
    global Not_Lei
    for i in range(row-1, row+2):
        for j in range(column-1, column+2):
            try:
                if globals()['Block_'+str(i)+'_'+str(j)].state != 'Null':
                    if globals()['Block_'+str(i)+'_'+str(j)].number != 0:
                        Not_Lei.add((i, j))

                    else:
                        if (i, j) not in Not_Lei:
                            Not_Lei.add((i, j))
                            ShowDetection(i, j)
            except:
                pass


def Show(row, column, block):
    global Not_Lei
    Not_Lei_1 = list(Not_Lei)
    for x in Not_Lei_1:
        if globals()['Block_'+str(x[0])+'_'+str(x[1])].Lei == False:
            globals()['Block_'+str(x[0])+'_'+str(x[1])].state = str(globals()
                                                                    ['Block_'+str(x[0])+'_'+str(x[1])].number)
            globals()['Block_'+str(x[0])+'_'+str(x[1])].config(image=globals()['Block_'+str(
                x[0])+'_'+str(x[1])].master.photo[globals()['Block_'+str(x[0])+'_'+str(x[1])].state])
            globals()['Block_'+str(x[0])+'_'+str(x[1])].image = globals()['Block_'+str(
                x[0])+'_'+str(x[1])].master.photo[globals()['Block_'+str(x[0])+'_'+str(x[1])].state]
        else:
            if globals()['Block_'+str(x[0])+'_'+str(x[1])].number != 0:
                if globals()['Block_'+str(x[0])+'_'+str(x[1])].number == signed_number(row, column):
                    Show_All_End(block)

    Not_Lei = set()


def signed_number(row, column):
    nuber = 0
    for x in range(row-1, row+2):
        for y in range(column-1, column+2):
            try:
                if globals()['Block_'+str(x)+'_'+str(y)].state == 'Null':
                    nuber += 1
            except:
                pass
    return nuber


def Show_All_End(block):
    for i, j in LEI_x_y:
        globals()['Block_'+str(i)+'_'+str(j)].config(image=globals()
                                                     ['Block_'+str(i)+'_'+str(j)].master.photo['NaN'])
        globals()['Block_'+str(i)+'_'+str(j)
                  ].image = globals()['Block_'+str(i)+'_'+str(j)].master.photo['NaN']
    end(block)


def end(block):
    end = tk.Toplevel(block.master)
    tk.Label(end, text="游戏结束!").pack()
    tk.Button(end, text='确认', command=end.master.master.destroy).pack()

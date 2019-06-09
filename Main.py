# coding=UTF-8
# (1)个人财务管理内容包括日期、收入、餐饮消费、服装消费、学习支出、娱乐支出
# (2)查看某个时间段的消费情况
# (3)分类统计各类消费占收入的比例，给出相应的消费预警
# (4)修改消费记录
# (5)全部信息以文件的形式保存，用菜单组织代码。
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, Canvas
import configparser
import time

fo = configparser.ConfigParser()
fo.read('Data.ini')
Money_category = ('+', '-')
category = ('工资', '餐饮', '服装', '学习', '娱乐')
Title = ('时间', '金额', '缘由', '备注')
Popup = False


class SetWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        height = self.winfo_screenheight()
        width = self.winfo_screenwidth()
        x = (width - 350) / 2
        y = (height - 180) / 2
        self.geometry("%dx%d+%d+%d" % (350, 180, x, y))
        self.title('插入信息')
        self.resizable(width=False, height=False)
        # 1
        row1 = tk.Frame(self)
        row1.grid(row=0)
        tk.Label(row1, text='时间：', width=10).grid(row=0, column=1)
        self.year = tk.StringVar()
        tk.Entry(row1, textvariable=self.year, width=5).grid(row=0, column=2)
        tk.Label(row1, text='年').grid(row=0, column=3)
        self.month = tk.StringVar()
        tk.Entry(row1, textvariable=self.month, width=2).grid(row=0, column=4)
        tk.Label(row1, text='月').grid(row=0, column=5)
        self.day = tk.StringVar()
        tk.Entry(row1, textvariable=self.day, width=2).grid(row=0, column=6)
        tk.Label(row1, text='日').grid(row=0, column=7)
        # 2
        row2 = tk.Frame(self)
        row2.grid(row=1)
        tk.Label(row2, text='缘由：', width=10).grid(row=0, column=1)
        self.reason = tk.StringVar()
        reason_combobox = ttk.Combobox(row2, width=18, textvariable=self.reason)
        reason_combobox.grid(row=0, column=2)
        reason_combobox['value'] = category
        reason_combobox.current(0)
        reason_combobox.bind("<<ComboboxSelected>>")
        # 3
        row3 = tk.Frame(self)
        row3.grid(row=2)
        tk.Label(row3, text='金额：', width=10).grid(row=0, column=1)
        self.add = tk.StringVar()
        add_combobox = ttk.Combobox(row3, width=2, textvariable=self.add)
        add_combobox.grid(row=0, column=2)
        add_combobox['value'] = Money_category
        add_combobox.current(0)
        add_combobox.bind("<<ComboboxSelected>>")
        self.money = tk.StringVar()
        tk.Entry(row3, textvariable=self.money, width=12).grid(row=0, column=3)
        tk.Label(row3, text='元').grid(row=0, column=4)
        # 4
        row4 = tk.Frame(self)
        row4.grid(row=3)
        tk.Label(row4, text='备注：', width=10).grid(row=0, column=1)
        self.extra = tk.StringVar()
        tk.Entry(row4, textvariable=self.extra, width=20).grid(row=0, column=2)
        # 5
        row5 = tk.Frame(self)
        row5.grid(row=4)
        Button(row5, text="确认", width=6, height=1, command=self.ok).grid(row=0, column=1)
        Button(row5, text="取消", width=6, height=1, command=self.cancel).grid(row=0, column=2)

    def ok(self):
        var = sorted(fo.sections())
        if len(var) == 0:
            id = str(1)
        else:
            id = str(int(var[len(var) - 1]) + 1)
        fo.add_section(id)
        fo.set(id, '日期',
               self.year.get().lstrip() + '年' + self.month.get().lstrip() + '月' + self.day.get().lstrip() + '日')
        fo.set(id, '金额', self.add.get() + self.money.get().lstrip())
        fo.set(id, '缘由', self.reason.get().lstrip())
        fo.set(id, '备注', self.extra.get().lstrip())
        fo.set(id, 'id', id)
        fo.write(open('Data.ini', "w"))
        self.destroy()  # 销毁窗口

    def cancel(self):
        self.destroy()


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        height = self.winfo_screenheight()
        width = self.winfo_screenwidth()
        x = (width - 1000) / 2
        y = (height - 380) / 2
        self.geometry("%dx%d+%d+%d" % (1000, 380, x, y))
        self.title('个人财务管理系统')
        self.resizable(width=False, height=False)

        label1 = tk.Label(self, width=75)
        label2 = tk.Label(self, height=40)
        label3 = tk.Label(self, height=5)
        label1.pack(fill=tk.Y, side=tk.LEFT)
        label2.pack(fill=tk.X, side=tk.TOP)
        label3.pack(fill=tk.X, side=tk.BOTTOM)

        tree = ttk.Treeview(label1, columns=Title, show='headings', selectmode="extended")
        for Attribute in Title:
            tree.column(Attribute, anchor='center')
            tree.heading(Attribute, text=Attribute)
        tree.column('时间', width=120)
        tree.column('金额', width=100)
        tree.column('缘由', width=100)
        tree.column('备注', width=430)

        tree.pack(expand=tk.YES, fill=tk.BOTH)
        canvas = Canvas(label2, height=330, width=250)
        canvas.pack()
        update(tree)
        draw(canvas)

        def Insert():
            setwindow = SetWindow()
            self.wait_window(setwindow)
            warning()
            update(tree)
            draw(canvas)

        def refresh():
            update(tree)
            draw(canvas)

        def Delete():
            if len(tree.selection()) == 0:
                return
            elif messagebox.askyesno('警告', '确认删除所选项吗？'):
                for i in tree.selection():
                    fo.remove_section(tree.item(i, 'values')[4])
                    fo.write(open('Data.ini', 'w'))
                update(tree)
                draw(canvas)

        def Change():
            if len(tree.selection()) == 0:
                return
            else:
                id = tree.item(tree.selection()[0], 'values')[4]
                Changewindow = tk.Toplevel()
                h = Changewindow.winfo_screenheight()
                w = Changewindow.winfo_screenwidth()
                x = (w - 350) / 2
                y = (h - 180) / 2
                Changewindow.geometry("%dx%d+%d+%d" % (350, 180, x, y))
                Changewindow.title('修改信息')
                Changewindow.resizable(width=False, height=False)
                # 1
                year = fo.get(id, "日期").split('年')[0]
                month = fo.get(id, "日期").split('年')[1].split('月')[0]
                day = fo.get(id, "日期").split('年')[1].split('月')[1].split('日')[0]
                row1 = tk.Frame(Changewindow)
                row1.grid(row=0)
                tk.Label(row1, text='时间：', width=10).grid(row=0, column=1)
                Changewindow.year = tk.StringVar()
                Changewindow.year.set(year)
                tk.Entry(row1, textvariable=Changewindow.year, width=5).grid(row=0, column=2)
                tk.Label(row1, text='年').grid(row=0, column=3)
                Changewindow.month = tk.StringVar()
                Changewindow.month.set(month)
                tk.Entry(row1, textvariable=Changewindow.month, width=2).grid(row=0, column=4)
                tk.Label(row1, text='月').grid(row=0, column=5)
                Changewindow.day = tk.StringVar()
                Changewindow.day.set(day)
                tk.Entry(row1, textvariable=Changewindow.day, width=2).grid(row=0, column=6)
                tk.Label(row1, text='日').grid(row=0, column=7)
                # 2
                row2 = tk.Frame(Changewindow)
                row2.grid(row=1)
                tk.Label(row2, text='缘由：', width=10).grid(row=0, column=1)
                Changewindow.reason = tk.StringVar()
                reason_combobox = ttk.Combobox(row2, width=18, textvariable=Changewindow.reason)
                reason_combobox.grid(row=0, column=2)
                reason_combobox['value'] = category
                reason_combobox.current(category.index(fo.get(id, '缘由')))
                reason_combobox.bind("<<ComboboxSelected>>")
                # 3
                row3 = tk.Frame(Changewindow)
                row3.grid(row=2)
                tk.Label(row3, text='金额：', width=10).grid(row=0, column=1)
                Changewindow.add = tk.StringVar()
                add_combobox = ttk.Combobox(row3, width=2, textvariable=Changewindow.add)
                add_combobox.grid(row=0, column=2)
                add_combobox['value'] = Money_category
                Money = fo.get(id, '金额')
                add_combobox.current(Money_category.index(Money[0]))
                add_combobox.bind("<<ComboboxSelected>>")
                Changewindow.money = tk.StringVar()
                Changewindow.money.set(Money.replace(Money[0], ''))
                tk.Entry(row3, textvariable=Changewindow.money, width=12).grid(row=0, column=3)
                tk.Label(row3, text='元').grid(row=0, column=4)
                # 4
                row4 = tk.Frame(Changewindow)
                row4.grid(row=3)
                tk.Label(row4, text='备注：', width=10).grid(row=0, column=1)
                Changewindow.extra = tk.StringVar()
                Changewindow.extra.set(fo.get(id, '备注'))
                tk.Entry(row4, textvariable=Changewindow.extra, width=20).grid(row=0, column=2)
                # 5
                row5 = tk.Frame(Changewindow)
                row5.grid(row=4)

                def ok():
                    fo.remove_section(id)
                    fo.add_section(id)
                    fo.set(id, '日期', Changewindow.year.get().lstrip() + '年' + Changewindow.month.get().lstrip()
                           + '月' + Changewindow.day.get().lstrip() + '日')
                    fo.set(id, '金额', Changewindow.add.get() + Changewindow.money.get().lstrip())
                    fo.set(id, '缘由', Changewindow.reason.get().lstrip())
                    fo.set(id, '备注', Changewindow.extra.get().lstrip())
                    fo.set(id, 'id', id)
                    fo.write(open('Data.ini', "w"))
                    update(tree)
                    draw(canvas)
                    Changewindow.destroy()
                    warning()

                def cancel():
                    Changewindow.destroy()

                Button(row5, text="确认", width=6, height=1, command=ok).grid(row=0, column=1)
                Button(row5, text="取消", width=6, height=1, command=cancel).grid(row=0, column=2)

        def Search():
            Searchwindow = tk.Toplevel()
            h = Searchwindow.winfo_screenheight()
            w = Searchwindow.winfo_screenwidth()
            x = (w - 350) / 2
            y = (h - 180) / 2
            Searchwindow.geometry("%dx%d+%d+%d" % (350, 180, x, y))
            Searchwindow.title('搜索信息')
            Searchwindow.resizable(width=False, height=False)
            # 1
            row1 = tk.Frame(Searchwindow)
            row1.grid(row=0)
            tk.Label(row1, text='开始时间：', width=12).grid(row=0, column=1)
            Searchwindow.year1 = tk.StringVar()
            Searchwindow.year1.set(2019)
            tk.Entry(row1, textvariable=Searchwindow.year1, width=5).grid(row=0, column=2)
            tk.Label(row1, text='年').grid(row=0, column=3)
            Searchwindow.month1 = tk.StringVar()
            Searchwindow.month1.set(6)
            tk.Entry(row1, textvariable=Searchwindow.month1, width=2).grid(row=0, column=4)
            tk.Label(row1, text='月').grid(row=0, column=5)
            Searchwindow.day1 = tk.StringVar()
            Searchwindow.day1.set(9)
            tk.Entry(row1, textvariable=Searchwindow.day1, width=2).grid(row=0, column=6)
            tk.Label(row1, text='日').grid(row=0, column=7)
            # 2
            row2 = tk.Frame(Searchwindow)
            row2.grid(row=1)
            tk.Label(row2, text='结束时间：', width=12).grid(row=1, column=1)
            Searchwindow.year2 = tk.StringVar()
            Searchwindow.year2.set(2019)
            tk.Entry(row2, textvariable=Searchwindow.year2, width=5).grid(row=1, column=2)
            tk.Label(row2, text='年').grid(row=1, column=3)
            Searchwindow.month2 = tk.StringVar()
            Searchwindow.month2.set(6)
            tk.Entry(row2, textvariable=Searchwindow.month2, width=2).grid(row=1, column=4)
            tk.Label(row2, text='月').grid(row=1, column=5)
            Searchwindow.day2 = tk.StringVar()
            Searchwindow.day2.set(9)
            tk.Entry(row2, textvariable=Searchwindow.day2, width=2).grid(row=1, column=6)
            tk.Label(row2, text='日').grid(row=1, column=7)
            # 3
            row3 = tk.Frame(Searchwindow, height=5)
            row3.grid(row=2)

            def ok():
                year1 = Searchwindow.year1.get()
                month1 = Searchwindow.month1.get()
                day1 = Searchwindow.day1.get()
                year2 = Searchwindow.year2.get()
                month2 = Searchwindow.month2.get()
                day2 = Searchwindow.day2.get()
                time1 = time.strptime(year1 + '-' + month1 + '-' + day1, '%Y-%m-%d')
                time2 = time.strptime(year2 + '-' + month2 + '-' + day2, '%Y-%m-%d')
                if time1 <= time2:
                    x = tree.get_children()
                    var = []
                    for item in x:
                        tree.delete(item)
                    for id in fo.sections():
                        year = fo.get(id, "日期").split('年')[0]
                        month = fo.get(id, "日期").split('年')[1].split('月')[0]
                        day = fo.get(id, "日期").split('年')[1].split('月')[1].split('日')[0]
                        item_time = time.strptime(year + '-' + month + '-' + day, '%Y-%m-%d')
                        if (item_time >= time1) & (item_time <= time2):
                            var.append(id)
                    var = sorted(var)
                    for i in range(0, len(var)):
                        valuevar = []
                        for options in fo.options(var[i]):
                            valuevar.append(fo.get(var[i], options))
                        tree.insert('', i, value=valuevar)
                    Searchwindow.destroy()
                else:
                    messagebox.showerror('错误', '时间输入错误')

            def cancel():
                Searchwindow.destroy()

            Button(row3, text="确认", width=6, height=1, command=ok).grid(row=0, column=1)
            Button(row3, text="取消", width=6, height=1, command=cancel).grid(row=0, column=2)

        tk.Button(label3, text="插入", width=5, command=Insert).grid(row=0, column=0)
        tk.Button(label3, text="删除", width=5, command=Delete).grid(row=0, column=1)
        tk.Button(label3, text="修改", width=5, command=Change).grid(row=0, column=2)
        tk.Button(label3, text="搜索", width=5, command=Search).grid(row=0, column=3)
        tk.Button(label3, text="全部", width=5, command=refresh).grid(row=0, column=4)


def update(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)
    var = sorted(fo.sections())
    for i in range(0, len(var)):
        valuevar = []
        for options in fo.options(var[i]):
            valuevar.append(fo.get(var[i], options))
        tree.insert('', i, value=valuevar)


def draw(canvas):
    cost = [0, 0, 0, 0]
    angle = [0, 0, 0, 0]
    all = 0
    for item in fo.sections():
        if category.index(fo.get(item, "缘由")) != 0:
            cost[category.index(fo.get(item, "缘由")) - 1] -= int(fo.get(item, "金额"))
    for co in cost:
        all += co
    for an in range(0, 4):
        if all == 0:
            angle[an] = 90
        else:
            angle[an] = cost[an] / all * 360
    canvas.create_rectangle(0, 0, 400, 400, fill="white")

    canvas.create_arc(200, 200, 50, 50, start=0, extent=angle[0] - 1, fill="red")
    canvas.create_arc(200, 200, 50, 50, start=angle[0], extent=angle[1] - 1, fill="green")
    canvas.create_arc(200, 200, 50, 50, start=angle[0] + angle[1], extent=angle[2] - 1, fill="yellow")
    canvas.create_arc(200, 200, 50, 50, start=360 - angle[3], extent=angle[3] - 1, fill="blue")

    canvas.create_text(40, 250, text="餐饮:" + str(int(round(angle[0] / 360 * 100, 0))) + '%', font=("", 14))
    canvas.create_rectangle(80, 240, 110, 260, fill="red")
    canvas.create_text(150, 250, text="服装:" + str(int(round(angle[1] / 360 * 100, 0))) + '%', font=("", 14))
    canvas.create_rectangle(190, 240, 220, 260, fill="green")
    canvas.create_text(40, 300, text="学习:" + str(int(round(angle[2] / 360 * 100, 0))) + '%', font=("", 14))
    canvas.create_rectangle(80, 290, 110, 310, fill="yellow")
    canvas.create_text(150, 300, text="娱乐:" + str(int(round(angle[3] / 360 * 100, 0))) + '%', font=("", 14))
    canvas.create_rectangle(190, 290, 220, 310, fill="blue")


def warning():
    cost = [0, 0, 0, 0]
    all = 0
    for item in fo.sections():
        if category.index(fo.get(item, "缘由")) != 0:
            cost[category.index(fo.get(item, "缘由")) - 1] -= int(fo.get(item, "金额"))
    for co in cost:
        all += co
    for i in range(0, 4):
        if cost[i] >= 500:
            messagebox.showwarning("警告", category[i+1]+"支出已超过500元")
    if all > 5000:
        messagebox.showwarning("警告", "总支出已超过5000元")


if __name__ == '__main__':
    app = MyApp()
    app.mainloop()

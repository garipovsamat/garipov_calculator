# imports
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import os


class Expression:
    def __init__(self):
        self._expression = "" # выражение, которое будет считаться питоном
        self._info = "" # выражение, которое будет видеть пользователь

    def add_number(self, number):
        self._expression += str(number)
        self._info += str(number)
        update_info(self._info)

    def fpercent(self):
        self._expression += '%'
        self._info += '% '
        update_info(self._info)

    def fce(self):
        for ichar in range(len(self._expression) - 1, -1, -1):
            if self._expression[ichar] not in '.0123456789':
                self._expression = self._expression[:ichar + 1]
                self._info = self._info[:ichar + 1]
                break
        update_info(self._info)

    def fc(self):
        self._expression = ' '
        self._info = ' '
        update_info(self._info)

    def fback(self):
        self._expression = self._expression[:-1]
        self._info = self._info[:-1]
        update_info(self._info)

    def frow(self):
        self._expression += '**2'
        self._info += "^2 "
        update_info(self._info)

    def frow3(self):
        self._expression += '**3'
        self._info += "^3 "
        update_info(self._info)

    def fsqrt(self):
        self._expression += '**(1/2)'
        self._info = self._info.split()
        self._info.insert(-1, "√")
        self._info = "".join(self._info)
        update_info(self._info)

    def fdiv(self):
        self._expression += '/'
        self._info += '/'
        update_info(self._info)

    def fmul(self):
        self._expression += '*'
        self._info += "*"
        update_info(self._info)

    def fsub(self):
        self._expression += '-'
        self._info += "-"
        update_info(self._info)

    def fadd(self):
        self._expression += '+'
        self._info += "+"
        update_info(self._info)

    def fpoint(self):
        self._expression += '.'
        self._info += "."
        update_info(self._info)

    def fsin(self):
        self._expression += "self.sin("
        self._info += "sin("
        update_info(self._info)
    @classmethod
    def sin(cls, x):
        x = math.radians(x)
        return math.sin(x)

    def fcos(self):
        self._expression += "self.cos("
        self._info += "cos("
        update_info(self._info)

    @classmethod
    def cos(cls, x):
        x = math.radians(x)
        return math.cos(x)

    def ftg(self):
        self._expression += "self.tan("
        self._info += "tan("
        update_info(self._info)

    @classmethod
    def tan(cls, x):
        x = math.radians(x)
        return math.tan(x)

    def fctg(self):
        self._expression += "self.ctan("
        self._info += "ctan("
        update_info(self._info)

    @classmethod
    def ctan(cls, x):
        x = math.radians(x)
        return 1 / math.tan(x)

    def fx(self):
        self._expression += "x"
        self._info += "x "
        update_info(self._info)

    def fy(self):
        self._expression += "y"
        self._info += "y "
        update_info(self._info)

    def fz(self):
        self._expression += "z"
        self._info += "z "
        update_info(self._info)


    def fmodule_left(self):
        self._expression += "abs("
        self._info += "|"
        update_info(self._info)

    def fmodule_right(self):
        self._expression += ")"
        self._info += "| "
        update_info(self._info)

    def fpi(self):
        self._expression += str(math.pi)
        self._info += "π "
        update_info(self._info)

    def fe(self):
        self._expression += str(math.e)
        self._info += "e "
        update_info(self._info)

    def frigthParenthesis(self):
        self._expression += ")"
        self._info += ") "
        update_info(self._info)

    def fleftParenthesis(self):
        self._expression += "("
        self._info += "("
        update_info(self._info)

    def fequal(self):
        try:
            if 'x' in self._expression or 'y' in self._expression or 'z' in self._expression:
                showerror(title="ОШИБКА УРАВНЕНИЯ!", message="Невозможно посчитать уравнение.")
                self._expression = ''
                self._info = ''
                update_info(self._info)
            else:
                temp_history = self._expression
                self._expression = str(eval(self._expression.strip()))
                with open('history.txt', 'a') as f:
                    f.write(f"{temp_history.strip()} = {self._expression}\n")
                self._info = self._expression
                update_info(self._info)
        except:
            showerror(title="ОШИБКА СЧЁТА!", message="Посчитать введённые данные невозможно!")
            self._expression = ''
            self._info = ''
            update_info(self._info)

class Graphic:
    __graphics = 0
    def __init__(self, expression):
        self.graphic = True # график ли это
        if 'x' not in expression._expression: self.graphic = False

        xs = np.linspace(-1000, 1000, 400)
        ys = []
        for x in xs:
            try:
                y = eval(expression._expression.replace('self', 'Expression'))
            except:
                showerror(title="Неправильное выражение!", message="Ошибка в выражении! Попробуйте снова.")
                self.graphic = False
                break
            ys.append(y)
        if self.graphic:
            self.fig = Figure(figsize=(5, 4), dpi=100)
            self.ax = self.fig.add_subplot(111)
            self.ax.plot(xs, ys, color='black')
            self.ax.grid(True)
            self.ax.axvline(color='black', alpha=0.5)
            self.ax.axhline(color='black', alpha=0.5)


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title("Калькулятор")
        self.width = 320
        self.height = 310
        self.return_size()
        self.resizable(False, False)

        for c in range(4): self.columnconfigure(c, weight=1)
        for r in range(8): self.columnconfigure(r, weight=1)

        self.modes = ["Standart", "Scientific", "Graphics"]
        self.mode = StringVar(value=self.modes[0])
        self.modebox = ttk.Combobox(values=self.modes, state="readonly", textvariable=self.mode)
        self.modebox.bind("<<ComboboxSelected>>", lambda event: self.change_mode(self.modebox.get()))
        self.modebox.grid(row=0, column=0, columnspan=4, sticky='w')

        self.info = ttk.Label(text="0", anchor='center')
        self.info.grid(row=1, column=0, columnspan=4, ipadx=10)

        self.standart_widgets = []
        self.programming_widgets = []
        self.graphics_widgets = []

        self.protocol('WM_DELETE_WINDOW', self.close_program)

        self.standart_calc()  

    def close_program(self):
        self.destroy()

    def forget_all_widgets(self):
        for widget in self.programming_widgets:
            widget.grid_forget()
        for widget in self.graphics_widgets:
            widget.grid_forget()
        for widget in self.standart_widgets:
            widget.grid_forget()

    def standart_calc(self):
        self.forget_all_widgets()
        self.standart_widgets = []
        self.return_size()
        self.author = ttk.Label(text="Гарипов Самат\nK0109-23", anchor='sw')
        self.standart_widgets.append(self.author)
        self.author.grid(row=7, column=0, ipadx=5)

        self.btn7 = ttk.Button(text="7", command=lambda: expression.add_number(7))
        self.btn8 = ttk.Button(text="8", command=lambda: expression.add_number(8))
        self.btn9 = ttk.Button(text="9", command=lambda: expression.add_number(9))
        self.btn4 = ttk.Button(text="4", command=lambda: expression.add_number(4))
        self.btn5 = ttk.Button(text="5", command=lambda: expression.add_number(5))
        self.btn6 = ttk.Button(text="6", command=lambda: expression.add_number(6))
        self.btn1 = ttk.Button(text="1", command=lambda: expression.add_number(1))
        self.btn2 = ttk.Button(text="2", command=lambda: expression.add_number(2))
        self.btn3 = ttk.Button(text="3", command=lambda: expression.add_number(3))
        self.btn0 = ttk.Button(text="0", command=lambda: expression.add_number(0))
        self.standart_widgets.append(self.btn7)
        self.standart_widgets.append(self.btn8)
        self.standart_widgets.append(self.btn9)
        self.standart_widgets.append(self.btn4)
        self.standart_widgets.append(self.btn5)
        self.standart_widgets.append(self.btn6)
        self.standart_widgets.append(self.btn1)
        self.standart_widgets.append(self.btn2)
        self.standart_widgets.append(self.btn3)
        self.standart_widgets.append(self.btn0)

        self.btn7.grid(row=4, column=0, ipadx=7, ipady=10)
        self.btn8.grid(row=4, column=1, ipadx=7, ipady=10)
        self.btn9.grid(row=4, column=2, ipadx=7, ipady=10)
        self.btn4.grid(row=5, column=0, ipadx=7, ipady=10)
        self.btn5.grid(row=5, column=1, ipadx=7, ipady=10)
        self.btn6.grid(row=5, column=2, ipadx=7, ipady=10)
        self.btn1.grid(row=6, column=0, ipadx=7, ipady=10)
        self.btn2.grid(row=6, column=1, ipadx=7, ipady=10)
        self.btn3.grid(row=6, column=2, ipadx=7, ipady=10)
        self.btn0.grid(row=7, column=1, ipadx=7, ipady=10)

        self.percent = ttk.Button(text="%", command=expression.fpercent)
        self.ce = ttk.Button(text="CE", command=expression.fce)
        self.cbtn = ttk.Button(text="C", command=expression.fc)
        self.back = ttk.Button(text="<X", command=expression.fback)
        self.row = ttk.Button(text="X^2", command=expression.frow)
        self.row3 = ttk.Button(text="X^3", command=expression.frow3)
        self.sqrt = ttk.Button(text="sqrt(X)", command=expression.fsqrt)
        self.div = ttk.Button(text="/", command=expression.fdiv)
        self.mul = ttk.Button(text="*", command=expression.fmul)
        self.sub = ttk.Button(text="-", command=expression.fsub)
        self.add = ttk.Button(text="+", command=expression.fadd)
        self.equal = ttk.Button(text="=", command=expression.fequal)
        self.point = ttk.Button(text=".", command=expression.fpoint)
        self.standart_widgets.append(self.percent)
        self.standart_widgets.append(self.ce)
        self.standart_widgets.append(self.cbtn)
        self.standart_widgets.append(self.back)
        self.standart_widgets.append(self.row)
        self.standart_widgets.append(self.sqrt)
        self.standart_widgets.append(self.div)
        self.standart_widgets.append(self.mul)
        self.standart_widgets.append(self.sub)
        self.standart_widgets.append(self.add)
        self.standart_widgets.append(self.equal)
        self.standart_widgets.append(self.point)
        self.standart_widgets.append(self.row3)

        self.row3.grid(row=3, column=0, ipadx=7, ipady=10)
        self.percent.grid(row=2, column=0, ipadx=7, ipady=10)
        self.ce.grid(row=2, column=1, ipadx=7, ipady=10)
        self.cbtn.grid(row=2, column=2, ipadx=7, ipady=10)
        self.back.grid(row=2, column=3, ipadx=7, ipady=10)
        self.row.grid(row=3, column=1, ipadx=7, ipady=10)
        self.sqrt.grid(row=3, column=2, ipadx=7, ipady=10)
        self.div.grid(row=3, column=3, ipadx=7, ipady=10)
        self.mul.grid(row=4, column=3, ipadx=7, ipady=10)
        self.sub.grid(row=5, column=3, ipadx=7, ipady=10)
        self.add.grid(row=6, column=3, ipadx=7, ipady=10)
        self.equal.grid(row=7, column=3, ipadx=7, ipady=10)
        self.point.grid(row=7, column=2, ipadx=7, ipady=10)

    def programming_calc(self):
        self.forget_all_widgets()
        self.standart_widgets = []
        self.programming_widgets = []
        self.change_size(x=500)
        self.btn7 = ttk.Button(text="7", command=lambda: expression.add_number(7))
        self.btn8 = ttk.Button(text="8", command=lambda: expression.add_number(8))
        self.btn9 = ttk.Button(text="9", command=lambda: expression.add_number(9))
        self.btn4 = ttk.Button(text="4", command=lambda: expression.add_number(4))
        self.btn5 = ttk.Button(text="5", command=lambda: expression.add_number(5))
        self.btn6 = ttk.Button(text="6", command=lambda: expression.add_number(6))
        self.btn1 = ttk.Button(text="1", command=lambda: expression.add_number(1))
        self.btn2 = ttk.Button(text="2", command=lambda: expression.add_number(2))
        self.btn3 = ttk.Button(text="3", command=lambda: expression.add_number(3))
        self.btn0 = ttk.Button(text="0", command=lambda: expression.add_number(0))
        self.standart_widgets.append(self.btn7)
        self.standart_widgets.append(self.btn8)
        self.standart_widgets.append(self.btn9)
        self.standart_widgets.append(self.btn4)
        self.standart_widgets.append(self.btn5)
        self.standart_widgets.append(self.btn6)
        self.standart_widgets.append(self.btn1)
        self.standart_widgets.append(self.btn2)
        self.standart_widgets.append(self.btn3)
        self.standart_widgets.append(self.btn0)

        self.btn7.grid(row=4, column=2, ipadx=7, ipady=10)
        self.btn8.grid(row=4, column=3, ipadx=7, ipady=10)
        self.btn9.grid(row=4, column=4, ipadx=7, ipady=10)
        self.btn4.grid(row=5, column=2, ipadx=7, ipady=10)
        self.btn5.grid(row=5, column=3, ipadx=7, ipady=10)
        self.btn6.grid(row=5, column=4, ipadx=7, ipady=10)
        self.btn1.grid(row=6, column=2, ipadx=7, ipady=10)
        self.btn2.grid(row=6, column=3, ipadx=7, ipady=10)
        self.btn3.grid(row=6, column=4, ipadx=7, ipady=10)
        self.btn0.grid(row=7, column=3, ipadx=7, ipady=10)

        self.percent = ttk.Button(text="%", command=expression.fpercent)
        self.ce = ttk.Button(text="CE", command=expression.fce)
        self.cbtn = ttk.Button(text="C", command=expression.fc)
        self.back = ttk.Button(text="<X", command=expression.fback)
        self.row = ttk.Button(text="X^2", command=expression.frow)
        self.row3 = ttk.Button(text="X^3", command=expression.frow3)
        self.sqrt = ttk.Button(text="sqrt(X)", command=expression.fsqrt)
        self.div = ttk.Button(text="/", command=expression.fdiv)
        self.mul = ttk.Button(text="*", command=expression.fmul)
        self.sub = ttk.Button(text="-", command=expression.fsub)
        self.add = ttk.Button(text="+", command=expression.fadd)
        self.equal = ttk.Button(text="=", command=expression.fequal)
        self.point = ttk.Button(text=".", command=expression.fpoint)
        self.standart_widgets.append(self.percent)
        self.standart_widgets.append(self.ce)
        self.standart_widgets.append(self.cbtn)
        self.standart_widgets.append(self.back)
        self.standart_widgets.append(self.row)
        self.standart_widgets.append(self.sqrt)
        self.standart_widgets.append(self.div)
        self.standart_widgets.append(self.mul)
        self.standart_widgets.append(self.sub)
        self.standart_widgets.append(self.add)
        self.standart_widgets.append(self.equal)
        self.standart_widgets.append(self.point)
        self.standart_widgets.append(self.row3)

        self.percent.grid(row=2, column=2, ipadx=7, ipady=10)
        self.ce.grid(row=2, column=3, ipadx=7, ipady=10)
        self.cbtn.grid(row=2, column=4, ipadx=7, ipady=10)
        self.back.grid(row=2, column=5, ipadx=7, ipady=10)
        self.row.grid(row=3, column=3, ipadx=7, ipady=10)
        self.row3.grid(row=3, column=2, ipadx=7, ipady=10)
        self.sqrt.grid(row=3, column=4, ipadx=7, ipady=10)
        self.div.grid(row=3, column=5, ipadx=7, ipady=10)
        self.mul.grid(row=4, column=5, ipadx=7, ipady=10)
        self.sub.grid(row=5, column=5, ipadx=7, ipady=10)
        self.add.grid(row=6, column=5, ipadx=7, ipady=10)
        self.equal.grid(row=7, column=5, ipadx=7, ipady=10)
        self.point.grid(row=7, column=4, ipadx=7, ipady=10)
        # тут будет создание кнопок научных

        self.sin = ttk.Button(text="sin", command=lambda: expression.fsin())
        self.cos = ttk.Button(text="cos", command=lambda: expression.fcos())
        self.tan = ttk.Button(text="tg", command=lambda: expression.ftg())
        self.ctan = ttk.Button(text="ctg", command=lambda: expression.fctg())
        self.x = ttk.Button(text="x", command=lambda: expression.fx())
        self.y = ttk.Button(text="y", command=lambda: expression.fy())
        self.z = ttk.Button(text="z", command=lambda: expression.fz())
        self.leftParenthesis = ttk.Button(text="(...", command=lambda: expression.fleftParenthesis())
        self.rightParenthesis = ttk.Button(text="...)", command=lambda: expression.frigthParenthesis())
        self.left_module = ttk.Button(text="|...", command=lambda: expression.fmodule_left())
        self.right_module = ttk.Button(text="...|", command=lambda: expression.fmodule_right())
        self.pi = ttk.Button(text="π", command=lambda: expression.fpi())
        self.e = ttk.Button(text="e", command=lambda: expression.fe())
        self.programming_widgets.append(self.sin)
        self.programming_widgets.append(self.cos)
        self.programming_widgets.append(self.tan)
        self.programming_widgets.append(self.ctan)
        self.programming_widgets.append(self.x)
        self.programming_widgets.append(self.y)
        self.programming_widgets.append(self.z)
        self.programming_widgets.append(self.leftParenthesis)
        self.programming_widgets.append(self.rightParenthesis)
        self.programming_widgets.append(self.left_module)
        self.programming_widgets.append(self.right_module)
        self.programming_widgets.append(self.pi)
        self.programming_widgets.append(self.e)

        self.sin.grid(row=2, column=0, ipadx=7, ipady=10)
        self.cos.grid(row=2, column=1, ipadx=7, ipady=10)
        self.tan.grid(row=3, column=0, ipadx=7, ipady=10)
        self.ctan.grid(row=3, column=1, ipadx=7, ipady=10)
        self.x.grid(row=7, column=0, ipadx=7, ipady=10)
        self.y.grid(row=7, column=1, ipadx=7, ipady=10)
        self.z.grid(row=7, column=2, ipadx=7, ipady=10)
        self.leftParenthesis.grid(row=4, column=0, ipadx=7, ipady=10)
        self.rightParenthesis.grid(row=4, column=1, ipadx=7, ipady=10)
        self.left_module.grid(row=5, column=0, ipadx=7, ipady=10)
        self.right_module.grid(row=5, column=1, ipadx=7, ipady=10)
        self.pi.grid(row=6, column=0, ipadx=7, ipady=10)
        self.e.grid(row=6, column=1, ipadx=7, ipady=10)

    def graphics_calc(self):
        self.forget_all_widgets()

        self.change_size(500, 500)
        graphic = Graphic(expression)

        if graphic.graphic:
            canvas = FigureCanvasTkAgg(graphic.fig, master=self)
            canvas.draw()
            c = canvas.get_tk_widget()
            c.grid(row=2, column=0, rowspan=9, columnspan=6)
            self.graphics_widgets.append(c)
        else:
            showerror("Неправильный график!", "График, что вы указали, не может быть построен!\nПопробуйте снова.")
            self.return_size()
            self.mode.set("Scientific")
            self.programming_calc()

    def change_size(self, x=320, y=310):
        self.geometry(f'{x}x{y}')
        for c in range(x//40): self.columnconfigure(c, weight=1)
        for r in range(y//75): self.columnconfigure(r, weight=1)

    def return_size(self):
        self.geometry(
            f"{self.width}x{self.height}+{self.winfo_screenwidth() // 2 - self.width // 2}+{self.winfo_screenheight() // 2 - self.height // 2}")
        for c in range(4): self.columnconfigure(c, weight=1)
        for r in range(8): self.columnconfigure(r, weight=1)

    def change_mode(self, mode):
        match mode:
            case "Standart": self.standart_calc()
            case "Scientific": self.programming_calc()
            case "Graphics": self.graphics_calc()

def update_info(expression): 
    if expression == '' or expression == ' ':
        window.info["text"] = '0'
    else:
        window.info["text"] = expression

if __name__ == "__main__":
    expression = Expression()
    window = Window()

    window.mainloop()
import tkinter as tk
import numpy as np
from random import randint, choice
from solver import benchmark, Solver
from connect import AVR_1, AVR_2
from time import sleep

class Cube:
    
    red = 0
    green = 1
    orange = 2
    blue = 3
    yellow = 4
    white = 5
    xf = 0
    xb = 1
    yf = 2
    yb = 3
    zf = 4
    zb = 5
    left = 0
    right = 1
    colors = ["red", "green", "orange", "blue", "yellow", "white"]
    edge = 50
    font1 = ("MSゴシック", 12)
    font2= ("MSゴシック", 17)
    pos = [(edge*2, edge*3), (edge*4, edge*3), (edge*6, edge*3),
               (edge*8, edge*3), (edge*8, edge*1), (edge*8, edge*5)]

    def __init__(self):
        self.masu = np.array([self.red]*4 + [self.green]*4 + [self.orange]*4
                             + [self.blue]*4 + [self.yellow]*4 + [self.white]*4)
        self.cathe = -1

    def reset(self, diff=0):
        self.cathe = -1
        self.masu = np.array([self.red]*4 + [self.green]*4 + [self.orange]*4
                             + [self.blue]*4 + [self.yellow]*4 + [self.white]*4)
        for _ in range(diff):
            self.random()

    def set(self, problem):
        self.masu = np.array(problem).flatten()
        self.cathe = -1

    def observe(self):
        obs = [0] * 84
        i = 0
        for color in self.masu[:15]:
            if i != 2:
                j = i if i < 2 else i - 1
                obs[color*14 + j] = 1
            i += 1
        return np.array(obs).astype(np.float32)

    def random(self):
        for _ in range(10):
            menn, muki = choice([1, 3, 5]), randint(0, 1)
            if self.cathe != menn + (1 - muki):
                self.cathe = menn + muki
                break
        self.rotate(menn, muki)

    def rotate(self, menn, muki):
        piyo = self.masu
        if menn == self.xf:
            if muki == self.left:
                piyo[20:24] = piyo[21], piyo[23], piyo[20], piyo[22]
                piyo[2], piyo[3], piyo[6], piyo[7], piyo[10], piyo[11], piyo[14], piyo[15]  = piyo[6], piyo[7], piyo[10], piyo[11], piyo[14], piyo[15], piyo[2], piyo[3]
            else:
                piyo[20:24] = piyo[22], piyo[20], piyo[23], piyo[21]
                piyo[2], piyo[3], piyo[6], piyo[7], piyo[10], piyo[11], piyo[14], piyo[15]  = piyo[14], piyo[15], piyo[2], piyo[3], piyo[6], piyo[7], piyo[10], piyo[11]
        elif menn == self.xb:
            if muki == self.right:
                piyo[16:20] = piyo[18], piyo[16], piyo[19], piyo[17]
                piyo[0], piyo[1], piyo[4], piyo[5], piyo[8], piyo[9], piyo[12], piyo[13] = piyo[4], piyo[5], piyo[8], piyo[9], piyo[12], piyo[13], piyo[0], piyo[1]
            else:
                piyo[16:20] = piyo[17], piyo[19], piyo[16], piyo[18]
                piyo[0], piyo[1], piyo[4], piyo[5], piyo[8], piyo[9], piyo[12], piyo[13] = piyo[12], piyo[13], piyo[0], piyo[1], piyo[4], piyo[5], piyo[8], piyo[9]
        elif menn == self.yf:
            if muki == self.left:
                piyo[0:4] = piyo[1], piyo[3], piyo[0], piyo[2]
                piyo[17], piyo[19], piyo[13], piyo[15], piyo[21], piyo[23], piyo[6], piyo[4] = piyo[6], piyo[4], piyo[17], piyo[19], piyo[13], piyo[15], piyo[21], piyo[23]
            else:
                piyo[0:4] = piyo[2], piyo[0], piyo[3], piyo[1]
                piyo[17], piyo[19], piyo[13], piyo[15], piyo[21], piyo[23], piyo[6], piyo[4] = piyo[13], piyo[15], piyo[21], piyo[23], piyo[6], piyo[4], piyo[17], piyo[19]
        elif menn == self.yb:
            if muki == self.right:
                piyo[8:12] = piyo[10], piyo[8], piyo[11], piyo[9]
                piyo[5], piyo[7], piyo[22], piyo[20], piyo[14], piyo[12], piyo[18], piyo[16] = piyo[22], piyo[20], piyo[14], piyo[12], piyo[18], piyo[16], piyo[5], piyo[7]
            else:
                piyo[8:12] = piyo[9], piyo[11], piyo[8], piyo[10]
                piyo[5], piyo[7], piyo[22], piyo[20], piyo[14], piyo[12], piyo[18], piyo[16] = piyo[18], piyo[16], piyo[5], piyo[7], piyo[22], piyo[20], piyo[14], piyo[12]
        elif menn == self.zf:
            if muki == self.left:
                piyo[12:16] = piyo[13], piyo[15], piyo[12], piyo[14]
                piyo[20], piyo[21], piyo[2], piyo[0], piyo[19], piyo[18], piyo[9], piyo[11] = piyo[9], piyo[11], piyo[20], piyo[21], piyo[2], piyo[0], piyo[19], piyo[18]
            else:
                piyo[12:16] = piyo[14], piyo[12], piyo[15], piyo[13]
                piyo[20], piyo[21], piyo[2], piyo[0], piyo[19], piyo[18], piyo[9], piyo[11] = piyo[2], piyo[0], piyo[19], piyo[18], piyo[9], piyo[11], piyo[20], piyo[21]
        elif menn == self.zb:
            if muki == self.right:
                piyo[4:8] = piyo[6], piyo[4], piyo[7], piyo[5]
                piyo[22], piyo[23], piyo[3], piyo[1], piyo[17], piyo[16], piyo[8], piyo[10] = piyo[8], piyo[10], piyo[22], piyo[23], piyo[3], piyo[1], piyo[17], piyo[16]
            else:
                piyo[4:8] = piyo[5], piyo[7], piyo[4], piyo[6]
                piyo[22], piyo[23], piyo[3], piyo[1], piyo[17], piyo[16], piyo[8], piyo[10] = piyo[3], piyo[1], piyo[17], piyo[16], piyo[8], piyo[10], piyo[22], piyo[23]

    def render(self, canvas):
        canvas.delete("cube")
        menn = ["yf", "zb", "yb", "zf", "xb", "xf"]
        for i in range(6):
            j = 0
            zeroX, zeroY = self.pos[i]
            for masu in self.masu[i*4:(i+1)*4]:
                num = i * 4 + j
                x, y = (j%2)*self.edge + zeroX, (j//2)*self.edge + zeroY
                canvas.create_rectangle(x, y, x + self.edge, y + self.edge, fill=self.colors[masu], tag="cube")
                canvas.create_text(x + self.edge//2, y + self.edge//2, text=str(num), font=self.font1, tag="cube")
                j += 1
            canvas.create_text(zeroX + self.edge*0.8, zeroY + self.edge*0.8, text=menn[i], font=self.font2, tag="cube")

def complete(cube):
    for i, j in zip(cube.masu, np.array([cube.red]*4 + [cube.green]*4 + [cube.orange]*4
                             + [cube.blue]*4 + [cube.yellow]*4 + [cube.white]*4)):
        if i != j:
            return False
    return True

def start():
    def rotate(menn, muki):
        cube.rotate(menn, muki)
        cube.render(canvas1)
    def reset():
        cube.reset()
        cube.render(canvas1)
    def random():
        cube.random()
        cube.render(canvas1)
    def test():
        ans = solver.solve(cube.masu)
        timer = len(ans)
        if timer == 0:
            return
        piyo, hoge = ["", "xb", "", "yb", "", "zb"], ["left", "right"]
        msg = []
        for menn, muki in ans:
            msg.append(piyo[menn] + " - " + hoge[muki])
        write(msg)
        def _rotate():
            nonlocal timer
            menn, muki = ans[-timer]
            rotate(menn, muki)
            timer -= 1
            if timer > 0:
                root.after(300, _rotate)
        _rotate()
    def write(message):
        canvas3.delete("message")
        i = 0
        j = 0
        for msg in message:
            canvas3.create_text(70+130*j, i*20+330, text=msg, font=("MSゴシック", 17), fill="white", tag="message")
            i += 1
            if i > 12:
                j += 1
                i = 0
    def avr_1_connect():
        canvas3.delete("avr1")
        if avr_1.connect(txt1.get()):
            canvas3.create_text(130, 60, text="OK", font=("MSゴシック", 17), fill="green", tag="avr1")
        else:
            canvas3.create_text(130, 60, text="NG", font=("MSゴシック", 17), fill="red", tag="avr1")
    def avr_2_connect():
        canvas3.delete("avr2")
        if avr_2.connect(txt2.get()):
            canvas3.create_text(330, 60, text="OK", font=("MSゴシック", 17), fill="green", tag="avr2")
        else:
            canvas3.create_text(330, 60, text="NG", font=("MSゴシック", 17), fill="red", tag="avr2")
    def avr_1_close():
        canvas3.delete("avr1")
        avr_1.close()
        canvas3.create_text(130, 60, text="NG", font=("MSゴシック", 17), fill="red", tag="avr1")
    def avr_2_close():
        canvas3.delete("avr2")
        avr_2.close()
        canvas3.create_text(330, 60, text="NG", font=("MSゴシック", 17), fill="red", tag="avr2")
    def avr_1_test():
        if avr_1.ser == None:
            return
        data = []
        for _ in range(4):
            sleep(0.5)
            data.append(avr_1.receive())
        print(data)
    def avr_2_test():
        if avr_2.ser == None:
            return
        avr_2.send(b'a')
        avr_2.send(b'b')
        avr_2.send(b'c')
        avr_2.send(b'd')
        avr_2.send(b'e')
        avr_2.send(b'f')
        avr_2.send(b'g')
        avr_2.send(b'h')
        avr_2.send(b'i')
        avr_2.send(b'j')
    def _sub_read_color(): #1面読む
        data = []
        avr_2.send(b'i')
        for _ in range(4):
            sleep(1.5)
            data.append(avr_1.receive())
            avr_2.send(b'e')
        avr_2.send(b'j')
        data[2], data[3] = data[3], data[2]
        print(data)
        return data
    def read_color():
        if avr_1.ser == None or avr_2.ser == None:
            return
        nonlocal problem, count
        if count == 0:
            problem[3] = _sub_read_color()
            avr_2.send(b'b')
        elif count == 1:
            problem[2] = _sub_read_color()
            avr_2.send(b'b')
        elif count == 2:
            problem[1] = _sub_read_color()
            avr_2.send(b'b')
        elif count == 3:
            problem[0] = _sub_read_color()
            avr_2.send(b'b')
            avr_2.send(b'c')
        elif count == 4:
            problem[4] = _sub_read_color()
            avr_2.send(b'c')
            avr_2.send(b'c')
        elif count == 5:
            problem[5] = _sub_read_color()
            avr_2.send(b'c')
            if not check():
                problem = [[-1]*4 for _ in range(6)]
            else:
                cube.set(problem)
                cube.render(canvas1)
                count = 0
            return
        count += 1
        root.after(5000, read_color)
    def solve_and_rotate():
        nonlocal problem
        if avr_2.ser == None or not check():
            return
        answer = solve(problem)
        for menn, muki in answer:
            if menn == 1:
                avr_2.send(b'd')
                if muki == 0:
                    avr_2.send(b'h')
                else:
                    avr_2.send(b'g')
                avr_2.send(b'c')
            elif menn == 3:
                avr_2.send(b'a')
                if muki == 0:
                    avr_2.send(b'h')
                else:
                    avr_2.send(b'g')
                avr_2.send(b'b')
            else:
                if muki == 0:
                    avr_2.send(b'h')
                else:
                    avr_2.send(b'g')
    def check():
        nonlocal problem
        for i in np.array(problem).flatten():
            if i < 0 or i > 5:
                return False
        return True
    count = 0
    timer = 0
    problem = [[-1]*4]*6
    root = tk.Tk()
    root.title(u'ルービックキューブソルバー')
    root.geometry("1000x600")
    root.resizable(False, False)
    canvas1 = tk.Canvas(width=600, height=400, bg="gray70", relief="ridge")
    canvas2 = tk.Canvas(width=600, height=200, bg="white", relief="ridge")
    canvas3 = tk.Canvas(width=400, height=600, bg="gray55", relief="ridge")
    canvas1.place(x=0, y=0)
    canvas2.place(x=0, y=400)
    canvas3.place(x=600, y=0)
    canvas3.create_text(50, 300, text="出力", font=("MSゴシック", 19), fill="lawn green")
    canvas3.create_text(100, 17, text="カラーセンサ", font=("MSゴシック", 17), fill="orange")
    canvas3.create_text(300, 17, text="モータ", font=("MSゴシック", 17), fill="cyan")
    canvas3.create_text(60, 60, text="接続 :", font=("MSゴシック", 17), fill="white")
    canvas3.create_text(130, 60, text="NG", font=("MSゴシック", 17), fill="red", tag="avr1")
    canvas3.create_text(260, 60, text="接続 :", font=("MSゴシック", 17), fill="white")
    canvas3.create_text(330, 60, text="NG", font=("MSゴシック", 17), fill="red", tag="avr2")
    canvas3.create_text(53, 105, text="ポート :", font=("MSゴシック", 17), fill="white")
    canvas3.create_text(253, 105, text="ポート :", font=("MSゴシック", 17), fill="white")
    canvas3.create_line(0, 35, 400, 35, width=2, fill="white")
    canvas3.create_line(200, 0, 200, 270, width=2, fill="white")
    canvas3.create_line(0, 270, 400, 270, width=2, fill="white")
    canvas2.create_line(440, 0, 440, 200, width=2, fill="gray65")
    canvas2.create_text(520, 35, text="Arduino接続必要", font=("MSゴシック", 14), fill="red2")
    canvas2.create_text(470, 92, text="1.", font=("MSゴシック", 14), fill="gray20")
    canvas2.create_text(470, 152, text="2.", font=("MSゴシック", 14), fill="gray20")
    txt1 = tk.Entry(canvas3, width=12)
    txt1.place(x=100, y=97)
    txt2 = tk.Entry(canvas3, width=12)
    txt2.place(x=300, y=97)
    cube = Cube()
    solver = Solver()
    avr_1, avr_2 = AVR_1(), AVR_2()
    cube.render(canvas1)
    tk.Button(canvas2, text="xb - left", command=lambda : rotate(1, 0)).place(x=60, y=60)
    tk.Button(canvas2, text="xb - right", command=lambda : rotate(1, 1)).place(x=60, y=120)
    tk.Button(canvas2, text="yb - left", command=lambda : rotate(3, 0)).place(x=140, y=60)
    tk.Button(canvas2, text="yb - right", command=lambda : rotate(3, 1)).place(x=140, y=120)
    tk.Button(canvas2, text="zb - left", command=lambda : rotate(5, 0)).place(x=220, y=60)
    tk.Button(canvas2, text="zb - right", command=lambda : rotate(5, 1)).place(x=220, y=120)
    tk.Button(canvas2, text="ランダム回転", command=random, fg="red").place(x=320, y=40)
    tk.Button(canvas2, text="マス初期化", command=reset, fg="blue").place(x=320, y=90)
    tk.Button(canvas2, text="AIで解く", command=test, fg="green").place(x=320, y=140)
    tk.Button(canvas2, text="マス読み込み", command=read_color, fg="black").place(x=490, y=80)
    tk.Button(canvas2, text="解く・回転実行", command=solve_and_rotate, fg="purple").place(x=490, y=140)
    tk.Button(canvas3, text="AVR-1(センサ) - 接続", command=avr_1_connect, fg="green").place(x=50, y=150)
    tk.Button(canvas3, text="AVR-1(センサ) - テスト", command=avr_1_test, fg="blue").place(x=50, y=185)
    tk.Button(canvas3, text="AVR-1(センサ) - 切断", command=avr_1_close, fg="red").place(x=50, y=220)
    tk.Button(canvas3, text="AVR-2(モータ) - 接続", command=avr_2_connect, fg="green").place(x=250, y=150)
    tk.Button(canvas3, text="AVR-2(モータ) - テスト", command=avr_2_test, fg="blue").place(x=250, y=185)
    tk.Button(canvas3, text="AVR-2(モータ) - 切断", command=avr_2_close, fg="red").place(x=250, y=220)

if __name__ == "__main__":
    start()

#---------------------------------------------------------------
#定義
import tkinter
import random
import time
import sys
from penguin import *
from PIL import Image, ImageTk
#---------------------------------------------------------------
#スクリーンについて
SCREEN_W=600    #スクリーンの横幅
SCREEN_H=450    #スクリーンの縦幅
SCREEN_C=("#d9e1f2")     #スクリーンの色
#---------------------------------------------------------------
#ゲーム内について
ADD_SCORE=10    #追加されるポイント
MISS_SCORE=1
PENGUIN_IMG = "pengin.png"  # ペンギンの画像
#---------------------------------------------------------------
#穴について
HOLE_C =("#8ea9db") #穴の色
NUM_H_HOLE = 4      # 横方向の穴の数
NUM_V_HOLE = 3      # 縦方向の穴の数
WIDTH_HOLE = 100    # 穴の幅（長軸の長さ）
WIDTH_SPACE = 20    # 穴と穴のスペースの幅
HEIGHT_SPACE = 70   # 穴と穴のスペースの高さ
#---------------------------------------------------------------
#時間間隔について
PENGUIN_UPDATE_INTERVAL = 100   # ペンギンの状態や位置を更新する時間間隔
FIGURE_UPDATE_INTERVAL = 100    # ペンギンの画像を更新する時間間隔
PENGUIN_CHOICE_INTERVAL = 2000     #時間間隔1
PENGUIN_CHOICE_INTERVAL2 = 1500     # 時間間隔2
PENGUIN_CHOICE_INTERVAL3 = 1300     # 時間間隔3
#---------------------------------------------------------------
# ゲームのクラス 
class Game:
    def __init__(self,game):
        self.width = SCREEN_W   #横の長さ
        self.height = SCREEN_H  #縦の長さ
        self.point=0
        self.misspoint=3
        self.game = game
        self.Canvus()    #キャンバスを作成する
        self.drawBackground()
        self.drawHoles()
        self.drawPenguins()
        self.update()
        self.choice()
        self.updatepengin()
    
    def Canvus(self):   # キャンバスの作成
        self.canvas = tkinter.Canvas(width=self.width,height=self.height)
        self.canvas.pack()
    
    def drawBackground(self):   #背景の作成
        # キャンバス全面に水色の四角形を描画
        self.bg = self.canvas.create_rectangle(0, 0, self.width, self.height,fill=SCREEN_C,outline=SCREEN_C)
        self.logo=self.canvas.create_text(300,20,text=("Penguin Pen! Pen!"),font=("Malgun Gothic Semilight",20,"bold"),fill="blue",justify="left",anchor="n")
        self.canvas.create_text(500,30,text=("Score : 0"),font=("MSゴシック",16,"bold"),fill="deep sky blue",justify="left",tag="mae")
        self.canvas.create_text(50,30,text=("HP : 3"),font=("MSゴシック",16,"bold"),justify="left",tag="missmae")

    def drawHoles(self):    #穴の作成
        self.hole_coords = []   #穴のリストを作成
        for v in range(NUM_V_HOLE):
            for h in range(NUM_H_HOLE):
                x = h * (WIDTH_HOLE + WIDTH_SPACE) + WIDTH_SPACE + WIDTH_HOLE / 2   #穴の中心のx座標
                y = v * (HEIGHT_HOLE + HEIGHT_SPACE) + HEIGHT_SPACE + HEIGHT_HOLE / 2   #穴の中心のy座標
                x1 = (x - WIDTH_HOLE / 2)+50     #穴の左上のx座標
                y1 = (y - HEIGHT_HOLE / 2)+80    #穴の左上のy座標
                x2 = (x + WIDTH_HOLE / 2)+50     #穴の右下のx座標
                y2 = (y + HEIGHT_HOLE / 2)+80    #穴の右下のy座標
                self.canvas.create_oval(x1, y1, x2, y2,fill=HOLE_C,outline=HOLE_C)  #穴を描画する
                self.hole_coords.append((x, y)) #穴のリストに追加する

    def drawPenguins(self):     #ペンギンを作成する
        picture = Image.open(PENGUIN_IMG)   # ペンギンの画像を読み込む
        newpicture =picture.crop(picture.getbbox())    #画像の外側を消す
        size = (WIDTH_HOLE - 40) / newpicture.width #ペンギンの画像を穴の幅に合わせる
        picture_2 = (round(size * newpicture.width),round(size * newpicture.height))
        penguin_img = newpicture.resize(picture_2)
        self.penguin_image = ImageTk.PhotoImage(penguin_img)
        self.penguins=[]    #ペンギンの管理リストを作成する
        for hole in self.hole_coords:
            x, y = hole    # 穴の座標を取得
            picture = self.canvas.create_image(x, y,anchor=tkinter.S,image=self.penguin_image)    #穴の中心に画像を表示
            self.canvas.lower(picture,"all")
            width=self.penguin_image.width()    #ペンギンオブジェクト(width)を作成する
            height=self.penguin_image.height()  #ペンギンオブジェクト(height)を作成する
            penguin=Penguin(x,y,width,height,1,picture) #ペンギンオブジェクトを作成する
            self.penguins.append(penguin)   #オブジェクトをリストに追加する
            self.canvas.tag_bind(picture, "<ButtonPress>", self.onClick)

    def onClick(self,event):
        self.canvas.create_text(300,400,text=("Hit !!"),font=("MSゴシック",20,"bold"),fill="red",justify="left",tag="hit")
        self.canvas.delete("mae")
        for p in self.penguins:# ペンギンの画像クリックを判断
            if p.isHit(event.x, event.y): #クリックした時
                self.canvas.delete("Y")
                p.hit()
                self.point += ADD_SCORE
                self.score=self.canvas.create_text(500,30,text=("Score : "+str(self.point)),font=("MSゴシック",16,"bold"),fill="deep sky blue",justify="left",tag="Y")

    def choice(self): #穴ランダムで穴からペンギンを出す
        self.canvas.delete("miss")
        self.canvas.delete("hit")
        hide_penguins = []  # 穴に隠れているリストを作成
        for penguin in self.penguins:
            if not penguin.is_appearing:
                hide_penguins.append(penguin)
        if len(hide_penguins) != 0: # 穴に隠れているペンギンがいる場合ランダムに選択して穴から出させる
            penguin = random.choice(hide_penguins)
            penguin.appear()
        if self.point <= 100:
            self.game.after(PENGUIN_CHOICE_INTERVAL, self.choice) 
        if self.point >= 100 and self.point <= 300:
            self.game.after(PENGUIN_CHOICE_INTERVAL2, self.choice)
        if self.point >= 300: 
            self.game.after(PENGUIN_CHOICE_INTERVAL3,self.choice)

    def update(self):   #画像を更新する
        for penguin in self.penguins:
            if penguin.is_appearing and penguin.is_draw:    # 出現中&描画フラグONの画像の場合
                self.canvas.lift(penguin.figure, "all") # ペンギンの画像を最前面に移動
                self.canvas.coords(penguin.figure, penguin.x+50, penguin.y+80)  # ペンギンの位置を更新
            else:
                self.canvas.lower(penguin.figure, "all")    # ペンギンの画像を最背面に移動
        self.game.after(FIGURE_UPDATE_INTERVAL, self.update)  # FIGURE_UPDATE_INTERVAL後に再度ペンギンの状態を更新
    
    def updatepengin(self): 
        for p in self.penguins:
            is_hitted=p.is_hitted
            before_appearing = p.is_appearing
            p.update()  # ペンギンの状態や位置を更新する
            after_appearing = p.is_appearing
            if not is_hitted and before_appearing and not after_appearing:
                self.canvas.create_text(300,400,text=("-MISS-"),font=("MSゴシック",20,"bold"),fill="blue",justify="left",tag="miss")
                self.canvas.delete("missmae")
                self.canvas.delete("A")
                self.misspoint -= MISS_SCORE
                self.miss=self.canvas.create_text(50,30,text=("HP : "+str(self.misspoint)),font=("MSゴシック",16,"bold"),justify="left",tag="A")
                if self.misspoint<=0:
                    time.sleep(4)
                    sys.exit()
        self.game.after(PENGUIN_UPDATE_INTERVAL, self.updatepengin)   # MOLE_UPDATE_INTERVAL後に再度ペンギンの状態を更新

tk = tkinter.Tk()
tk.title("Penguin Pen! Pen!")
game = Game(tk)
tk.mainloop()
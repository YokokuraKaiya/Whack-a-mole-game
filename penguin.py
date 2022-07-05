HEIGHT_HOLE = 30    # 穴の高さ（短軸の長さ）

class Penguin:
    def __init__(self, x, y, width, height, speed, figure):
         self.x = x  # 中央下の位置（横方向）
         self.y = y  # 中央下の位置（縦方向）
         self.width = width # 画像の幅
         self.height = height # 画像の高さ
         self.figure = figure # 描画画像の図形ID
         self.hole_y = y  # モグラが穴に潜る高さ
         self.top_y = self.hole_y - HEIGHT_HOLE / 3 # 穴から出る高さ
         self.speed = speed # 移動スピード
         self.point = 10 # 叩いた時にゲットできるポイント
         self.is_up = False # 上方向に移動中かどうかを管理するフラグ
         self.is_draw = True # 描画するかどうかを管理するフラグ
         self.is_hitted = False # 既に叩かれているかどうかを管理するフラグ
         self.is_appearing = False # 穴から出ているかどうかを管理するフラグ

    def appear(self):
        self.is_appearing=True
        self.is_up=True

    def hit(self):
        self.is_up = False
        self.is_hitted = True
    
    def isHit(self, mouse_x, mouse_y): #ペンギンを叩いたかを判断する
        if not self.is_appearing:   # 穴から出ていない時
            return False
        if self.is_hitted:  #すでに叩かれている時
            return False

        x1 = self.x - self.width / 2    #ペンギンの画像が表示されている左上のx座標
        y1 = self.y - self.height       #ペンギンの画像が表示されている左上のy座標
        x2 = self.x + self.width / 2    #ペンギンの画像が表示されている右下のx座標
        y2 = self.y                     #ペンギンの画像が表示されている右下のy座標

        if x1+50 <= mouse_x and x2+50 >= mouse_x: #衝突判定（マウスとペンギン）
            if y1+80 <= mouse_y and y2+80 >= mouse_y:
                return True # 叩かれた
        return False    # 叩かれていない

    def update(self):
        if self.is_up:
            self.y = max(self.top_y, self.y - self.speed)
            if self.y == self.top_y:# 上方向の上限に移動したから穴に戻る動きを開始
                self.is_up = False
        else:# 下方向への移動中
            self.y = min(self.hole_y, self.y + self.speed)
            if self.y == self.hole_y:   #穴に戻った時、状態をリセットする
                self.is_appearing = False
                self.is_hitted = False
                self.is_draw =True
        if self.is_hitted:
            self.is_draw = 0

from bonus import Bonus
from carposition import Carposition
from color import Color
from stage import Stage
from app import App

import time
import RPi.GPIO as GPIO # ラスパイ用のモジュールで，windowsはインストール不可

class Main:
    def __init__(self) -> None:
        self.stbtn_gpio = None 
        self.led_gpio = None
        self.score = None
        self.next_level = None
        self.need_score = None
        self.final_score = None
        self.ranking = [None, None, None]
        self.isStart = None
        self.isControl = None
        self.color =[None, None, None]
        self.isBonus = None
        self.bonus_color = None
        self.bonus = None
        self.start_time = None
        self.stage_speed = None
        self.elapsed_time = None

        # クラスの呼び出し
        self.stage_class = Stage()
        self.bonus_class = Bonus()
        self.carposition_class = Carposition()
        self.color_class = Color()
        self.app_class = App()


    def Main(self):
        """
        メイン処理(未完成)
        """
        # if(self.isStart == True):
        #     self.start()

        if(self.isControl == True):
            while True:
                # 後で考える
                # score, judgeColor, carposition.controlメゾットの3並列処理
                
                if(self.isControl == False):
                    break


    def start(self) -> None:
        """
        ゲームを開始する関数（未完成）
        """
        # スタート画面を表示させる処理
        self.app_class.change_page("home")

        # スタートボタンが押されたら開始
        if(self.isStart == True):
            #スタートボタンが押された際の時間(int型)を格納
            self.start_time = time.time() 
            self.isStart = False

            # カウント画面を表示させる処理
            self.app_class.change_page("countdown")

            # 5秒待機
            time.sleep(5) 

            # 白色LEDを点灯させる処理
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.led_gpio, GPIO.OUT)
            GPIO.output(self.led_gpio, GPIO.HIGH)

    def Score(self) -> None:
        """
        スコアを更新する関数（完成）
        """
        # 経過時間
        self.elapsed_time = time.time() - self.start_time

        # スコア更新
        self.score = self.stage_speed * self.elapsed_time
        self.level, self.stage_speed, self.need_level = self.stage_class.changeSpeed(self.score)
        self.next_need = self.next_level - self.score
    
    def judgeColor(self) -> None:
        """
        光センサーから読み取ったRGB値によって処理する関数（完成）
        """
        self.color = self.color.readColor()
        
        if(self.color == [0, 0, 0] or self.color == [128, 128, 128]):
            # ゲーム終了処理
            self.gameOver()
            
        elif(self.color == [255, 255, 0]):
            # ボーナスタイムに入る処理
            self.isBonus = True
            self.bonus_class.setBonus()
        
        if (self.isBonus == True):
            # ボーナス獲得処理
            # ボーナス画面を表示させる処理
            self.app_class.change_page("bonus")

            if(self.color == [255, 0, 0]):
                # 光センサーが赤を検知した際の処理
                self.isBonus = False
                self.bonus_color = "red"
                self.bonus = self.bonus_class.result(Bonus(self.bonus_color))

            elif(self.color == [0, 0, 255]):
                # 光センサーが黄色を検知した際の処理
                self.isBonus = False
                self.bonus_color = "yellow"
                self.bonus = self.bonus_class.resultBonus(self.bonus_color)

            elif(self.color == [255, 255, 255]):
                # 光センサーが白を検知した際の処理
                self.isBonus = False
                self.bonus_color = "white"
                self.bonus = self.bonus_class.resultBonus(self.bonus_color)

            elif(self.color == [0, 0, 0] or self.color == [128, 128, 128]):
                # 光センサーが黒，または白を検知した際の処理
                self.isBonus = False
                self.gameOver()
    
    def gameOver(self) -> None:
        """
        ゲームオーバー時の処理（完成かも）
        """
        self.isControl = False
        
        # 白色LEDを消灯する（少し怪しい）
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_gpio, GPIO.OUT)
        GPIO.output(self.led_gpio, GPIO.LOW)

        # 最終スコアを計算
        self.final_score = self.score + self.bonus

        # ゲーム終了画面を表示させる処理
        self.app_class.change_page("gameover")

        self.isStart = False

        # 初期化
        self.color_class.sleepColor()
        self.carposition_class.resetPosition()
        self.stage_class.stopStage()
        self.score = 0
        self.bonus = 0
        self.next_level = 0
        self.need_score = 0
        self.stage = 0

        # ランキングの更新
        self.sortRank()
        time.sleep(5)

        # スタート画面を表示させる処理
        self.app_class.change_page("home")
    
    def sortRank(self, final_score) -> None:
        """
        ランキングを更新する関数(完成)
        """
        # ランキングの更新
        new_score = self.score + [final_score] # スコア追記
        new_score = sorted(new_score, reverse=True) # 降順にソート
        new_score.pop(-1) # 末尾のスコアを削除
        self.score = new_score # ランキングスコア更新
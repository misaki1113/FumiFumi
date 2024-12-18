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


    def Main(self):
        # if(self.isStart == True):
        #     self.start()

        if(self.isControl == True):
            while True:
                # 後で考える
                # score, judgeColor, carposition.controlメゾットの3並列処理
                
                if(self.isControl == False):
                    break


    def start(self) -> None:
        # スタート画面を表示させる処理（後に考えて書く）
        # appクラスのchange_page(/)を実行して遷移するつもり

        if(self.isStart == True):
            self.start_time = time.time() #スタートボタンが押された際の時間(int型)
            self.isStart == False

            # カウント画面を表示させる処理(後に考えて書く)
            # appクラスのchange_page(countdown)を実行して遷移するつもり

            time.sleep(5) 

            # 白色LEDを点灯させる処理
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.led_gpio, GPIO.OUT)
            GPIO.output(self.led_gpio, GPIO.HIGH)

    def Score(self) -> None:
        # 経過時間
        self.elapsed_time = time.time() - self.start_time

        # スコア更新
        self.score = self.stage_speed + self.elapsed_time
        self.level, self.stage_speed, self.need_level = self.stage_class.changeSpeed(self.score)
        self.next_need = self.next_level - self.score
    
    def judgeColor(self) -> None:
        self.color = self.color.readColor()
        if(self.color == [0, 0, 0] or self.color == [128, 128, 128]):
            # ゲーム終了画面を表示させる処理(後に考えて書く)
            # appクラスのchange_page(gameover)を実行して遷移するつもり
            pass
        elif(self.color == [255, 255, 0]):
            self.isBonus = True
            self.bonus_class.setBonus()
        
        if (self.isBonus == True):
            # ボーナス画面を表示させる処理(後に考えて書く)
            # appクラスのchange_page(bonus)を実行して遷移するつもり

            if(self.color == [255, 0, 0]):
                self.isBonus = False
                self.bonus_color = "red"
                self.bonus = self.bonus_class.result(Bonus(self.bonus_color))

            elif(self.color == [0, 0, 255]):
                self.isBonus = False
                self.bonus_color = "yellow"
                self.bonus = self.bonus_class.resultBonus(self.bonus_color)

            elif(self.color == [255, 255, 255]):
                self.isBonus = False
                self.bonus_color = "white"
                self.bonus = self.bonus_class.resultBonus(self.bonus_color)

            elif(self.color == [0, 0, 0] or self.color == [128, 128, 128]):
                self.isBonus = False
                self.gameOver()
    
    def gameOver(self) -> None:
        self.isControl = False
        
        # 白色LEDを消灯する
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_gpio, GPIO.OUT)
        GPIO.output(self.led_gpio, GPIO.LOW)

        self.final_score = self.score + self.bonus

        # ゲーム終了画面を表示させる処理(後に考えて書く)
        # appクラスのchange_page(gameover)を実行して遷移するつもり

        self.isStart = False

        self.color_class.sleepColor()
        self.carposition_class.resetPosition()
        self.stage_class.stopStage()
        self.score = 0
        self.bonus = 0
        self.next_level = 0
        self.need_score = 0
        self.stage = 0

        self.sortRank()
        time.sleep(5)

        # スタート画面を表示させる処理（後に考えて書く）
        # appクラスのchange_page(/)を実行して遷移するつもり
    
    def sortRank(self, final_score) -> None:
        # ランキングの更新
        for score in self.ranking:
            
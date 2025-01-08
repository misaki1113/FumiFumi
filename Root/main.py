from bonus import Bonus
from carposition import CarPosition
from color import ColorSensor
from stage import stage
from app import App

import time
import RPi.GPIO as GPIO # ラスパイ用のモジュールで，windowsはインストール不可
import concurrent.futures

score = None
next_level = None
need_score = None
final_score = None
ranking = [None, None, None]
bonus = None

isStart = None
isControl = None


class Main:
    def __init__(self) -> None:
        self.stbtn_gpio = 29 
        self.led_gpio = 15
        self.color =[None, None, None]
        self.isBonus = None
        self.bonus_color = None
        self.start_time = None
        self.stage_speed = None
        self.elapsed_time = None

        # クラスの呼び出し
        self.stage_class = stage()
        self.bonus_class = Bonus()
        self.carposition_class = CarPosition()
        self.color_class = ColorSensor()
        self.app_class = App()


    def Main(self):
        """
        メイン処理(完成)
        """
        while True:
            if(isStart == True):
                self.start()

            if(isControl == True):
                # score, judgeColor, carposition.controlメゾットの3並列処理            
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    executor.submit(self.Score())
                    executor.submit(self.judgeColor())
                    executor.submit(self.carposition_class.control())


    def start(self) -> None:
        """
        ゲームを開始する関数（完成）
        """
        # スタート画面を表示させる処理
        self.app_class.change_page("home")

        # スタートボタンが押されたら開始
        if(isStart == True):
            #スタートボタンが押された際の時間(int型)を格納
            self.start_time = time.time() 
            isStart = False

            # カウント画面を表示させる処理
            self.app_class.change_page("countdown")

            # 8秒待機
            time.sleep(8) 

            #コントロール可
            isControl = True

            self.app_class.change_page("score")

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
        score = self.stage_speed * self.elapsed_time
        self.level, self.stage_speed, self.need_level = self.stage_class.changeSpeed(score)
        self.next_need = next_level - score
    
    def judgeColor(self) -> None:
        """
        光センサーから読み取ったRGB値によって処理する関数（完成）
        """
        self.color = self.color_class.readColor()
        
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
                bonus = self.bonus_class.result(Bonus(self.bonus_color))

            elif(self.color == [0, 0, 255]):
                # 光センサーが黄色を検知した際の処理
                self.isBonus = False
                self.bonus_color = "yellow"
                bonus = self.bonus_class.resultBonus(self.bonus_color)

            elif(self.color == [255, 255, 255]):
                # 光センサーが白を検知した際の処理
                self.isBonus = False
                self.bonus_color = "white"
                bonus = self.bonus_class.resultBonus(self.bonus_color)

            elif(self.color == [0, 0, 0] or self.color == [128, 128, 128]):
                # 光センサーが黒，または白を検知した際の処理
                self.isBonus = False
                self.gameOver()
        
        elif(self.isBonus == False):
            # スコア・ランキング画面を表示
            self.app_class.change_page("score")
    
    def gameOver(self) -> None:
        """
        ゲームオーバー時の処理（完成かも）
        """
        isControl = False
        self.isBonus = False
        
        # 白色LEDを消灯する（少し怪しい）
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_gpio, GPIO.OUT)
        GPIO.output(self.led_gpio, GPIO.LOW)

        # 最終スコアを計算
        final_score = score + bonus

        # ゲーム終了画面を表示させる処理
        self.app_class.change_page("gameover")

        # 初期化
        self.color_class.sleepColor()
        self.carposition_class.resetPosition()
        self.stage_class.stopStage()
        score = 0
        bonus = 0
        next_level = 0
        need_score = 0
        self.stage = 0

        # ランキングの更新
        self.sortRank()
        time.sleep(5)

        isStart = True

        # スタート画面を表示させる処理
        self.app_class.change_page("home")
    
    def sortRank(self, final_score) -> None:
        """
        ランキングを更新する関数(完成)
        """
        # ランキングの更新
        new_score = score + [final_score] # スコア追記
        new_score = sorted(new_score, reverse=True) # 降順にソート
        new_score.pop(-1) # 末尾のスコアを削除
        score = new_score # ランキングスコア更新
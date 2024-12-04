from bonus import Bonus
from carposition import Carposition
from  color import Color

import time
import RPI.GPIO as GPIO
class Main:
    def __init__(self) -> None:
        self.stbtn_gpio = None 
        self.led_gpio = None
        self.score = None
        self.next_level = None
        self.need_level = None
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

    def Main(self):
        if(self.isStart == True):
            
            self.start()

    def start(self) -> None:
        # スタート画面を表示させる処理（後に考えて書く）

        if(self.isStart == True):
            self.isStart == False
            # カウント画面を表示させる処理(後に考えて書く)

            time.sleep(5) 

            # っ白色LEDを点灯させる処理（後に考えて書く）

    def score(self) -> None:

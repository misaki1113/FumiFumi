import RPi.GPIO as GPIO
import time

distance_move = 85  # ステップ数
leftbtn_gpio = 6   # 左操作盤
midbtn_gpio = 19   # 中央操作盤
rightbtn_gpio = 26 # 右操作盤

steppingStep_gpio = 20  # STEP端子
steppingDir_gpio = 21   # DIR端子
steppingMs2_gpio = 16   # MS2端子

class CarPosition:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(leftbtn_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(midbtn_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(rightbtn_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(steppingStep_gpio, GPIO.OUT)
        GPIO.setup(steppingDir_gpio, GPIO.OUT)
        GPIO.setup(steppingMs2_gpio, GPIO.OUT)

        # 1/4マイクロステップモードをON
        GPIO.output(steppingMs2_gpio, GPIO.HIGH)

        self.isLeft = False
        self.isMid = False
        self.isRight = False
        self.num_move = 0

    def control(self):
        # 左操作盤が押された場合
        if GPIO.input(leftbtn_gpio) == GPIO.HIGH:
            if self.isMid:
                self.isMid = False
                self.changePosition(-1)
            elif self.isRight:
                self.isRight = False
                self.isLeft = True
            else:
                self.isLeft = True

        # 中央操作盤が押された場合
        if GPIO.input(midbtn_gpio) == GPIO.HIGH:
            if self.isRight:
                self.isRight = False
                self.changePosition(1)
            elif self.isLeft:
                self.isLeft = False
                self.changePosition(-1)
            else:
                self.isMid = True

        # 右操作盤が押された場合
        if GPIO.input(rightbtn_gpio) == GPIO.HIGH:
            if self.isMid:
                self.isMid = False
                self.changePosition(1)
            elif self.isLeft:
                self.isLeft = False
                self.isRight = True
            else:
                self.isRight = True

    def changePosition(self, step):
        if -10 < self.num_move < 10:
            # 方向を決定（stepが1なら右、-1なら左）
            GPIO.output(steppingDir_gpio, GPIO.HIGH if step > 0 else GPIO.LOW)

            for _ in range(distance_move):
                GPIO.output(steppingStep_gpio, GPIO.HIGH)
                time.sleep(0.001) 
                GPIO.output(steppingStep_gpio, GPIO.LOW)
                time.sleep(0.001)

            # num_moveを更新
            self.num_move += step

    def resetPosition(self):
        steps_to_reset = self.num_move * distance_move

        if steps_to_reset == 0:
            return
        
        # 方向を決定(steps_to_resetが正なら左、負なら右)
        GPIO.output(steppingDir_gpio, GPIO.LOW if steps_to_reset > 0 else GPIO.HIGH)

        # モータをリセット位置まで移動
        for _ in range(abs(steps_to_reset)):
            GPIO.output(steppingStep_gpio, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(steppingStep_gpio, GPIO.LOW)
            time.sleep(0.001)

        self.num_move = 0

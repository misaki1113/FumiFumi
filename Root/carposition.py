import RPi.GPIO as GPIO
import time

class CarPosition:
    
    distance_move = 85  # 可動機の移動ステップ数

    def __init__(self):
        self.leftbtn_gpio = 6   # 左操作盤
        self.midbtn_gpio = 19    # 中央操作盤
        self.rightbtn_gpio = 26  # 右操作盤

        self.steppingStep_gpio = 20  # STEP端子
        self.steppingDir_gpio = 21   # DIR端子
        self.steppingMs2_gpio = 16   # MS2端子

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.leftbtn_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.midbtn_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.rightbtn_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.steppingStep_gpio, GPIO.OUT)
        GPIO.setup(self.steppingDir_gpio, GPIO.OUT)
        GPIO.setup(self.steppingMs2_gpio, GPIO.OUT)

        # 1/4マイクロステップモードをON
        GPIO.output(self.steppingMs2_gpio, GPIO.HIGH)

        self.isLeft = False
        self.isMid = False
        self.isRight = False
        self.num_move = 0

    def control(self):
        # 左操作盤が押された場合
        if GPIO.input(self.leftbtn_gpio) == GPIO.HIGH:
            if self.isMid:
                self.isMid = False
                self.changePosition(-1)
            elif self.isRight:
                self.isRight = False
                self.isLeft = True
            else:
                self.isLeft = True

        # 中央操作盤が押された場合
        if GPIO.input(self.midbtn_gpio) == GPIO.HIGH:
            if self.isRight:
                self.isRight = False
                self.changePosition(1)
            elif self.isLeft:
                self.isLeft = False
                self.changePosition(-1)
            else:
                self.isMid = True

        # 右操作盤が押された場合
        if GPIO.input(self.rightbtn_gpio) == GPIO.HIGH:
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
            # 移動するステップ数をdistance_moveに基づき設定
            steps_to_move = self.distance_move
            # 方向を決定
            GPIO.output(self.steppingDir_gpio, GPIO.HIGH if step > 0 else GPIO.LOW)

            # ステッピングモータを動かす
            for _ in range(steps_to_move):
                GPIO.output(self.steppingStep_gpio, GPIO.HIGH)
                time.sleep(0.001)  # STEP信号の間隔
                GPIO.output(self.steppingStep_gpio, GPIO.LOW)
                time.sleep(0.001)

            # num_moveを更新（stepが1なら前進、-1なら後退）
            self.num_move += step

    def resetPosition(self):
        steps_to_reset = self.num_move * self.distance_move

        # リセットが不要な場合に処理を終了
        if steps_to_reset == 0:
            return
        
        # 方向を決定(正の値は前進、負の値は後退)
        GPIO.output(self.steppingDir_gpio, GPIO.LOW if steps_to_reset > 0 else GPIO.HIGH)

        # モータをリセット位置まで移動
        for _ in range(abs(steps_to_reset)):
            GPIO.output(self.steppingStep_gpio, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self.steppingStep_gpio, GPIO.LOW)
            time.sleep(0.001)

        self.num_move = 0

import RPi.GPIO as GPIO
import time

class stage:
	def stage_init(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		self.RPWM = 19;  # GPIO pin 19 to the RPWM on the BTS7960
		self.LPWM = 26;  # GPIO pin 26 to the LPWM on the BTS7960

		self.L_EN = 20;  # connect GPIO pin 20 to L_EN on the BTS7960
		self.R_EN = 21;  # connect GPIO pin 21 to R_EN on the BTS7960

		GPIO.setup(self.RPWM, GPIO.OUT)
		GPIO.setup(self.LPWM, GPIO.OUT)
		GPIO.setup(self.L_EN, GPIO.OUT)
		GPIO.setup(self.R_EN, GPIO.OUT)

		GPIO.output(self.R_EN, True)
		GPIO.output(self.L_EN, True)

		self.rpwm= GPIO.PWM(self.RPWM, 500)
		self.lpwm= GPIO.PWM(self.LPWM, 500)

		self.rpwm.start(0)

	def changeSpeed(self,score):
		level = int(score/2000) + 1
		stage_speed = level*0.5 + 3
		geard_speed = level*1.25 + 7.6

		DutyCycle = 100 * (geard_speed/200)

		self.rpwm.ChangeDutyCycle(DutyCycle)
		time.sleep(0.02)

		return level, stage_speed, geard_speed

	def stopStage(self):
		DutyCycle = 0

		self.rpwm.ChangeDutyCycle(DutyCycle)
		time.sleep(0.02)


	


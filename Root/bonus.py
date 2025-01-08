import RPi.GPIO as GPIO
import random

result_bonus = [0, 0, 0]

class Bonus:

    def __init__(self):
        self.result_bonus = 0

    def setBonus(self):
        value_bonus = [10, 50, 100]
        self.result_bonus = random.sample(value_bonus, 3)

    def resultBonus(self, bonus_color):
        color = bonus_color

        if(color == "red"):
            bonus = self.result_bonus[0]
        elif(color == "blue"):
            bonus = self.result_bonus[1]
        else:
            bonus== self.result_bonus[2]

        return bonus

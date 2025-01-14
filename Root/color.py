import smbus
import time

slave_address = 0x2A

sensor_control = 0x00
timing_H = 0x01
timing_L = 0x02
data_red_H = 0x03
data_red_L = 0x04
data_green_H = 0x05
data_green_L = 0x06
data_blue_H = 0x07
data_blue_L = 0x08

ctrl_reset = 0x80
ctrl_sleep = 0x40
ctrl_gain = 0x08
ctrl_mode = 0x04

ctrl_time = 0x1  # 0x0:87,5µs,0x1:1.4ms,0x2:22.4ms,0x3:179.2ms

bus = smbus.SMBus(1)

class ColorSensor:

    def __init__(self):
        self.address = slave_address
        self.setGain(1)
        self.setTime(ctrl_time)
        self.setMode()
        self.start()

    def setGain(self, gain):
        control_data = self.getConfig()
        if gain == 1:  # 1:GAIN_HIGH, 0:GAIN_LOW
            control_data |= ctrl_gain
        else:
            control_data &= ~(ctrl_gain)
        bus.write_byte_data(self.address, sensor_control, control_data)

    def setTime(self, itime):
        self.itime = itime
        control_data = self.getConfig()
        control_data &= 0xFC  # 最下位の2ビットをゼロにする
        control_data |= itime  # 測定時間を設定
        bus.write_byte_data(self.address, sensor_control, control_data)

    def setMode(self):
        control_data = self.getConfig()

        # 固定時間モードに設定するため、CTRL_MODEビットをクリア
        control_data &= ~ctrl_mode  # CTRL_MODEビットを0に設定
        bus.write_byte_data(self.address, sensor_control, control_data)

    def start(self):
        control_data = self.getConfig()
        control_data |= ctrl_reset  # RESETビットをオン
        bus.write_byte_data(self.address, sensor_control, control_data)
        time.sleep(0.001) 

        control_data &= ~ctrl_reset  # RESETビットをオフ
        bus.write_byte_data(self.address, sensor_control, control_data)

        control_data &= 0x3F  # RESET off, SLEEP off
        bus.write_byte_data(self.address, sensor_control, control_data)

    def sleep(self):
        control_data = self.getConfig()
        control_data |= ctrl_sleep
        bus.write_byte_data(self.address, sensor_control, control_data)

    def getConfig(self):
        control_data = bus.read_byte_data(self.address, sensor_control)
        return control_data

    def read(self):
        # 遅延処理
        if self.itime == 0x0:  # 0x0: delay 88usec
            time.sleep(88 * 4 / 1000000)
            time.sleep(0.001)  # wait buffer

        elif self.itime == 0x1:  # 0x1: delay 2msec
            time.sleep(2 * 4 / 1000)
            time.sleep(0.001)  # wait buffer

        elif self.itime == 0x2:  # 0x2: delay 23msec
            time.sleep(23 * 4 / 1000)
            time.sleep(0.001)  # wait buffer

        elif self.itime == 0x3:  # 0x3: delay 180msec
            time.sleep(180 * 4 / 1000)
            time.sleep(0.001)  # wait buffer

        # カラーセンサデータの取得
        sensor_data = bus.read_i2c_block_data(self.address, data_red_H, 6)

        # 赤色データの取得とスケーリング
        color_red = (sensor_data[0] << 8) | sensor_data[1]
        r = min(max(int(color_red / 256), 0), 255)

        # 緑色データの取得とスケーリング
        color_green = (sensor_data[2] << 8) | sensor_data[3]
        g = min(max(int(color_green / 256), 0), 255)

        # 青色データの取得とスケーリング
        color_blue = (sensor_data[4] << 8) | sensor_data[5]
        b = min(max(int(color_blue / 256), 0), 255)

        color = [r, g, b]
        return color

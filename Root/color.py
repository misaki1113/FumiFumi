import smbus
import time

class S11059:

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

    # S11059 Control bits
    ctrl_reset = 0x80
    ctrl_sleep = 0x40
    ctrl_gain = 0x08
    ctrl_mode = 0x04

    ctrl_time = 0x1  # 0x0:87,5μs,0x1:1.4ms,0x2:22.4ms,0x3:179.2ms

    bus = smbus.SMBus(1)

    def __init__(self):
        self.address = S11059.slave_address
        self.setGain(1)
        self.setTime(S11059.ctrl_time)
        self.setMode()
        self.start()

    def setGain(self, gain):
        data = self.getConfig()
        if gain == 1:  # 1:GAIN_HIGH, 0:GAIN_LOW
            data |= S11059.ctrl_gain
        else:
            data &= ~(S11059.ctrl_gain)
        S11059.bus.write_byte_data(self.address, S11059.sensor_control, data)

    def setTime(self, itime):
        self.itime = itime
        data = self.getConfig()
        data &= 0xFC  # 最下位の2ビットをゼロにする
        data |= itime  # 測定時間を設定
        S11059.bus.write_byte_data(self.address, S11059.sensor_control, data)

    def setMode(self):
        data = self.getConfig()

        # 固定時間モードに設定するため、CTRL_MODEビットをクリア
        data &= ~S11059.ctrl_mode  # CTRL_MODEビットを0に設定
        S11059.bus.write_byte_data(self.address, S11059.sensor_control, data)
    
    def start(self):
        data = self.getConfig()
        data &= 0x3F  # RESET off, SLEEP off
        S11059.bus.write_byte_data(self.address, S11059.sensor_control, data)

    def sleep(self):
        data = self.getConfig()
        data |= S11059.ctrl_sleep
        S11059.bus.write_byte_data(self.address, S11059.sensor_control, data)

    def getConfig(self):
        control_data = S11059.bus.read_byte_data(self.address, S11059.sensor_control)
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
        sensor_data = S11059.bus.read_i2c_block_data(self.address, S11059.data_red_H, 8)

        # 赤色データの取得とスケーリング
        data_red_H = sensor_data[0]
        data_red_L = sensor_data[1]
        color_red = (data_red_H << 8) | data_red_L
        r = min(max(int(color_red / 256), 0), 255)

        # 緑色データの取得とスケーリング
        data_green_H = sensor_data[2]
        data_green_L = sensor_data[3]
        color_green = (data_green_H << 8) | data_green_L
        g = min(max(int(color_green / 256), 0), 255)

        # 青色データの取得とスケーリング
        data_blue_H = sensor_data[4]
        data_blue_L = sensor_data[5]
        color_blue = (data_blue_H << 8) | data_blue_L
        b = min(max(int(color_blue / 256), 0), 255)

        color = [r, g, b]
        return color

import smbus
import time

slave_address = 0x2A

sensor_control	= 0x00
timing_H     = 0x01
timing_L     = 0x02
data_red_H   = 0x03
data_red_L   = 0x04
data_green_H = 0x05
data_green_L = 0x06
data_blue_H  = 0x07
data_blue_L  = 0x08


# S11059 Control bits
ctrl_reset   = 0x80
ctrl_sleep   = 0x40
ctrl_gain    = 0x08
ctrl_mode    = 0x04

# S11059 Measurement time select
ctrl_time = 0x1 # 0x0:87,5μs,0x1:1.4ms,0x2:22.4ms,0x3:179.2ms


# SMBus
bus = smbus.SMBus(1)

## S11059 Class
class S11059:

    def __init__(self, address=SLAVE_ADDRESS):
        self.address = address
        self.setGain(1)
        self.setTime(ctrl_time)  
        self.setMode()  
        self.start() 

    ## Set Gain
    def setGain(self, gain):
        data = self.getConfig()
        if gain == 1:#1:GAIN_HIGH,0:GAIN_LOW
            data |= ctrl_gain
        else:
            data &= ~(ctrl_gain)
        bus.write_byte_data(self.address, control, data)

    ## Set Time
    def setTime(self, itime):
        self.itime = itime
        data = self.getConfig()
        data &= 0xFC  # 最下位の2ビットをゼロにする
        data |= itime  # 測定時間を設定
        bus.write_byte_data(self.address, control, data)

    ## Set Mode 
    def setMode(self):
        data = self.getConfig()

        # 固定時間モードに設定するため、CTRL_MODEビットをクリア
        data &= ~ctrl_mode  # CTRL_MODEビットを0に設定
        bus.write_byte_data(self.address, control, data)

    ## Start measurement
    def start(self):
        data = self.getConfig()
        data &= 0x3F  # RESET off, SLEEP off
        bus.write_byte_data(self.address, control, data)
　　
　　## Stop measurement
　　def sleep(self)
　　　　data = self.getConfig()
　　　　data |= ctrl_sleep
　　　　bus.write_byte_data(self.address, control, data)

    ## Get Config
    def getConfig(self):
        control_data = bus.read_byte_data(self.address, control)
        return control_data

    ## Read Measurement data
    def read(self):
        # 1. 遅延処理
        if self.itime == 0x0:  # 0x0: delay 88usec
            time.sleep(88 * 4 / 1000000)  # micro second
            time.sleep(0.001)            # wait buffer

        elif self.itime == 0x1:  # 0x1: delay 1.4msec
            time.sleep(2 * 4 / 1000)
            time.sleep(0.001)             # wait buffer

        elif self.itime == 0x2:  # 0x2: delay 22.4msec
            time.sleep(23 * 4 / 1000)
            time.sleep(0.001)             # wait buffer

        elif self.itime == 0x3:  # 0x3: delay 179.2msec
            time.sleep(180 * 4 / 1000)
            time.sleep(0.001)             # wait buffer

        # 2. カラーセンサデータの取得
        sensor_data = bus.read_i2c_block_data(self.address, data_red_h, 8)

        # 2.1 赤色データの取得とスケーリング
        color_red_high = sensor_data[0]
        color_red_low = sensor_data[1]
        color_red = (color_red_high << 8) | color_red_low
        r = min(max(int(color_red / 256), 0), 255)  # 0-255にスケーリング

        # 2.2 緑色データの取得とスケーリング
        color_green_high = sensor_data[2]
        color_green_low = sensor_data[3]
        color_green = (color_green_high << 8) | color_green_low
        g = min(max(int(color_green / 256), 0), 255)  # 0-255にスケーリング

        # 2.3 青色データの取得とスケーリング
        color_blue_high = sensor_data[4]
        color_blue_low = sensor_data[5]
        color_blue = (color_blue_high << 8) | color_blue_low
        b = min(max(int(color_blue / 256), 0), 255)  # 0-255にスケーリング

        # 3. RGB値を格納したリストを返す
        color = [r, g, b]
        return color

# _*_ coding:utf-8 _*_

import spidev
import time

spi = spidev.SpiDev()
spi.open(1,0)
spi.max_speed_hz = 1000000#これがないときはうまく読み込めなかった。

while True:

	try:
		resp = spi.xfer2([0x68,0x00])
		print(hex(resp[0]),hex(resp[1]))
		value = ((resp[0] << 8) + resp[1]) & 0x3ff#上位バイト分を8ビット左にシフトしてから下位バイト分を足し、10ビット分のマスクをかける
		print(value)
		time.sleep(0.1)
	except KeyboardInterrupt:
		break
spi.close()

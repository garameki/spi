# _*_ coding:utf-8 _*_

import spidev
import time
from time import sleep

spi = spidev.SpiDev()




spi.open(0,0)
spi.mode = 0x03			#モード3 CPOL:1 CPHA:1 cpha must be 1
spi.max_speed_hz = 1000000	#これがないときはうまく読み込めなかった。

resp = spi.xfer([0x81,0x03])	#K熱電対

resp = spi.xfer([0x80,0x40])	#計測

dummy = 0x00
byte_read = [dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy,dummy]
resp = spi.xfer2(byte_read)
for i in range(1,len(byte_read)):
	print(hex(i-1),hex(resp[i]))

resp = spi.xfer2([0x0C,0x0D,0x0E,dummy])
value = resp[1] * 256 + resp[2]
if (resp[1] & 0x80) != 0:
	value = -1 * (~(value - 1) & 0x7FFF)
print("TC temperature :",value*0.0625)

resp = spi.xfer2([0x0A,0x0B,dummy])
value = (resp[1] << 6)  + (resp[2] >> 2)
if (resp[1] & 0x80) != 0:
	value = -1 * (~(value - 1) & 0x7FFF)
print("CJ temperature :",value*0.015625)

resp = spi.xfer([0x80,0x00])
sleep(0.5)

spi.close()


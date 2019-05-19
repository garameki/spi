# _*_ coding:utf-8 _*_

from time import sleep
import spidev
spi = spidev.SpiDev()

spi.open(0,0)			#/sys/bus/spi/devices/dev0.0を使う
spi.mode = 0x03			#モード3 CPOL:1 CPHA:1 cpha must be 1
spi.max_speed_hz = 1000000	#最大クロック周波数

resp = spi.xfer([0x81,0x03])	#K熱電対を選択
resp = spi.xfer([0x80,0xC1])	#計測
sleep(0.1)			#計測を待つ

print("全レジスタの値")
print("アドレス 値");
resp = spi.readbytes(17)
for i in range(1,len(resp)):
	print("{0:02X}h      {1:02X}h".format(i-1,resp[i]))

dummy = 0
resp = spi.xfer2([0x0C,0x0D,0x0E,dummy])	#熱電対の温度を読み込み
value = resp[1] * 256 + resp[2]
if (resp[1] & 0x80) != 0:
	value = -1 * (~(value - 1) & 0x7FFF)	#2の補数の10進数化
print("熱電対温度 :{}℃".format(value*0.0625))

resp = spi.xfer2([0x0A,0x0B,dummy])		#冷接点の温度を読み込み
value = (resp[1] << 6)  + (resp[2] >> 2)
if (resp[1] & 0x80) != 0:
	value = -1 * (~(value - 1) & 0x7FFF)	#2の補数の10進数化
print("冷接点温度 :{}℃".format(value*0.015625))

spi.close()

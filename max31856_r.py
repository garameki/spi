#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import sys

import RPi.GPIO as GPIO
from time import sleep
import spidev

GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN)

spi = spidev.SpiDev()
spi.open(0,0)			#/sys/bus/spi/devices/dev0.0を使う
spi.mode = 0x03			#モード3 CPOL:1 CPHA:1 cpha must be 1
spi.max_speed_hz = 1000000	#最大クロック周波数

args = sys.argv
if len(args)==2:
	if args[1] == "reset":
		#FAULTピンのリセット
		resp = spi.xfer2([0x80,0x17])
		sleep(1)


#通常計測
resp = spi.xfer2([0x80,0x55,0x35,0x00,0x3C,0xF6,0x57,0x80,0xFE,0xC0,0x00])	#設定と同時に計測するのでCR0の第6ビットを立てる
sleep(1)			#計測を待つ

print("全レジスタの値")
print("アドレス 値");
resp = spi.readbytes(17)
for i in range(1,len(resp)):
	print("{0:02X}h      {1:02X}h".format(i-1,resp[i]))

#Faultの検知
if not GPIO.input(25):
	if (resp[16] & 0x80) != 0:print("Fault : Cold Junction Out of Range")
	if (resp[16] & 0x40) != 0:print("Fault : Thermocouple Out of Range")
	if (resp[16] & 0x20) != 0:print("Fault : Cold Junction High Fault")
	if (resp[16] & 0x10) != 0:print("Fault : Cold Junction Low Fault")
	if (resp[16] & 0x08) != 0:print("Fault : Thermocouple Temperature High Fault")
	if (resp[16] & 0x04) != 0:print("Fault : Thermocouple Temperature Low Fault")
	if (resp[16] & 0x02) != 0:print("Fault : Overvoltage or Undervoltage Input Fault")
	if (resp[16] & 0x01) != 0:print("Fault : Thermocouple Open-Circuit Fault")
else:

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
GPIO.cleanup()

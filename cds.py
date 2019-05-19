# _*_ coding:utf-8 _*_

import RPi.GPIO as GPIO
import spidev
import time

flag = True
GPIO.setwarnings(False)

try:
	GPIO.cleanup()
except:
	pass

GPIO.setmode(GPIO.BCM)
try:
	GPIO.setup(6,GPIO.OUT)
except:
	pass

spi = spidev.SpiDev()
try:
	spi.open(1,0)
except:
	print("There is not '/sys/bus/spi/devices/spi1.0'")
	flag = False
if(flag):
	spi.max_speed_hz = 1000000

	GPIO.output(6,GPIO.LOW)

	resp = spi.xfer2([0x68,0x00])
	#print(hex(resp[0]),hex(resp[1]))
	value = ((resp[0] << 8) + resp[1]) & 0x3ff#上位バイト分を8ビット左にシフトしてから下位バイト分を足し、10ビット分のマスクをかける
	#print(value)
	spi.close()

if(value < 800):
	GPIO.output(6,GPIO.HIGH)
	
#GPIO.cleanup()

#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

while True:
	try:
		resp = spi.xfer2([0x0,0x0,0x0,0x0])

		value  = (resp[3] << 0)
		value += (resp[2] << 8)
		value += (resp[1] << 16)
		value += (resp[0] << 24)
		print('{:032b}'.format(value))
		
		error   =  value & 0x00010007
		if error != 0:
			fault   =  value & 0x00010000
			short_v =  value & 4
			short_g =  value & 2
			open_c  =  value & 1
			if short_v != 0:
				print("熱電対がVccと短絡しています")
				break
			elif short_g != 0:
				print("熱電対がGNDと短絡しています")
				break
			elif open_c != 0:
				print("熱電対が繋がっていないか断線しています")
				break
			elif fault != 0:
				print("読み込みに失敗しました")
				break
			else:
				print("原因不明のエラーです")

		t_out   = ((value & 0xfffc0000) >> 18) * 0.25
		t_in    = ((value & 0x0000fff0) >>  4) * 0.0625
		print('熱電対{:4.1f}℃ 回路{:3.1f}℃'.format(t_out,t_in))

		time.sleep(0.5)
	except KeyboardInterrupt:
		break

spi.close()

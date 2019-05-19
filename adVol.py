#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

count = 0
while True:
	count += 1
	if count == 10:
		print()
		count = 0

	try:
		resp = spi.xfer2([0x68,0x00])
		print(hex(resp[0]),hex(resp[1]))

		value = ((resp[0] << 8) + resp[1]) & 0x3ff
		print(value)
		time.sleep(0.1)
	except KeyboardInterrupt:
		break

spi.close()

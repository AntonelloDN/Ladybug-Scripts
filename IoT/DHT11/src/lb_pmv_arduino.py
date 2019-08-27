# A basic example to use Ladybug tools API with DHT11 sensor.
#
# This file is part of Ladybug.
#
# Copyright (c) 2013-2019, Antonello Di Nunzio <antonellodinunzio@gmail.com>
# Ladybug is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3 of the License,
# or (at your option) any later version.
#
# Ladybug is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>


import time
import serial
import yaml
import matplotlib.pyplot as plt
from ladybug_comfort.pmv import predicted_mean_vote


def get_variables():

	ser = None

	with open("config.yml", 'r') as ymlfile:
		cfg = yaml.safe_load(ymlfile)
	try:
		ser = serial.Serial(cfg["serial"]["path"])
	except serial.serialutil.SerialException as e:
		print(e)
		return None, None

	return ser, cfg


def run_calculation(ser, plt, cfg):

	x = 0
	valx = []
	valy = []

	while(True):

		time.sleep(1)
		ser_bytes = ser.readline()
		temperature, humidity = map(int, ser_bytes.decode("utf-8").split(':'))

		# This script will assume that the mean radiant temperature is equal to air temperature
		results = predicted_mean_vote(temperature, temperature, cfg["condition"]["wind_speed"], humidity, cfg["condition"]["metabolic_rate"], cfg["condition"]["clothing_level"])
		print(temperature, humidity, results["pmv"])

		valx.append(x)
		valy.append(results["pmv"])

		line, = plt.plot(valx, valy, color='r', linewidth=1)
		plt.pause(1)
		line.remove()
		x+=1

	plt.ion()

def main():

	plt.axis([0, 100, -3, 3])
	plt.ylabel("pmv")
	plt.xlabel("seconds")
	plt.title("PMV LADYBUG COMFORT")
	
	ser, cfg = get_variables()

	if ser:
		run_calculation(ser, plt, cfg)

if __name__ == '__main__':

	main()
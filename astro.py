#!/usr/bin/python

from lxml import html
import requests
import time
import os
import string
import re
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

lcd = Adafruit_CharLCDPlate()
lcd.begin(16,2)
lcd.clear()
os.system('clear')

while 1:

        page = requests.get('http://www.swpc.noaa.gov/SWN/sw_dials.html')
        tree = html.fromstring(page.text)
        pageXray = requests.get('http://www.lmsal.com/solarsoft/last_events/')
        treeXray = html.fromstring(pageXray.text)

        mag_field = tree.xpath('//tr[2]/td[1]/text()[2]')
        speed_field = tree.xpath('//tr[2]/td[3]/text()[2]')
        pressure_field = tree.xpath('//tr[5]/td[3]/text()[2]')
        xray_field = treeXray.xpath('//tr[46]/td[6]/text()')

        xRayNom = re.compile('CB')
        xRayWatch = re.compile('M')
        xRayWarn = re.compile('X')

        mag = [ float(re.sub("[^0-9.]", " ", x)) for x in mag_field ]
        speed = [ float(re.sub("[^0-9.]", " ", x)) for x in speed_field ]
        pressure = [ float(re.sub("[^0-9.]", " ", x)) for x in pressure_field ]

        mag_disp = 'Mag Flux ' + str(mag[0]) + 'nT '
        speed_disp = 'Speed ' + str(speed[0]) + 'km/s '
        pressure_disp = 'Pressure ' + str(pressure[0]) + 'nPa '
        xray_disp = 'Cur Flare ' + xray_field[0]

        if (mag[0] >= 0 and mag[0] < 50) or pressure <= 10 or xRayNom.findall(xray_field):
                lcd.backlight(lcd.GREEN)
                lcd.message(mag_disp + '\n' + pressure_disp)
		print 'NOMINAL CONDITIONS Magnetic Field:',mag[0],'nT Speed:',speed[0],'km/s Pressure: ',pressure[0],'nPa ',xray_field[0]
                time.sleep(7.5)
                lcd.clear()
                os.system('clear')
         elif (mag[0] <= -5 and mag[0] >= 9) or (pressure[0] > 10 and pressure [0] <=25) or xRayWatch.findall(xray_field):
                lcd.backlight(lcd.YELLOW)
                lcd.message(mag_disp + '\n' + pressure_disp)
                print 'WATCH CONDITIONS Magnetic Field:',mag[0],'nT Speed:',speed[0], 'km/s Pressure:',pressure[0],'nPa ',xray_field[0]
                time.sleep(7.5)
                lcd.clear()
                lcd.message(xray_disp + '\n' + speed_disp)
                time.sleep(7.5)
                lcd.clear()
                os.system('clear')

        elif mag[0] <= -10 or pressure[0] > 25 or xRayWarn.findall(xray_field):
                lcd.backlight(lcd.RED)
                lcd.message(mag_disp + '\n' + pressure_disp)
                print 'WARNING CONDITIONS Magnetic Field:',mag[0],'nT Speed:',speed[0], 'km/s Pressure:',pressure[0],'nPa ',xray_field[0]
                time.sleep(7.5)
                lcd.clear()
                lcd.message(xray_disp + '\n' + speed_disp)
                time.sleep(7.5)
                lcd.clear()
                os.system('clear')

				

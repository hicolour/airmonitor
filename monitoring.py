#!/bin/python
import httplib, urllib
import RPi.GPIO as GPIO
import serial
import time
import sys
import statsd
from struct import *


debug=0
# work for pms3003
# data structure: https://github.com/avaldebe/AQmon/blob/master/Documents/PMS3003_LOGOELE.pdf
# fix me: the format is different between /dev/ttyUSBX(USB to Serial) and /dev/ttyAMA0(GPIO RX)
#          ttyAMA0:0042 004d 0014 0022 0033
#          ttyUSB0:4d42 1400 2500 2f00

class g3sensor():
    def __init__(self):
        if debug: print "init"
	self.endian = sys.byteorder
    def conn_serial_port(self, device):
        if debug: print device
        self.serial = serial.Serial(device, baudrate=9600)
        if debug: print "conn ok"

    def check_keyword(self):
        if debug: print "check_keyword"
        while True:
            token = self.serial.read()
    	    token_hex=token.encode('hex')
    	    if debug: print token_hex
    	    if token_hex == '42':
    	        if debug: print "get 42"
    	        token2 = self.serial.read()
    	        token2_hex=token2.encode('hex')
    	        if debug: print token2_hex
    	        if token2_hex == '4d':
    	            if debug: print "get 4d"
                    return True
		elif token2_hex == '00': # fixme
		    if debug: print "get 00"
		    token3 = self.serial.read()
		    token3_hex=token3.encode('hex')
		    if token3_hex == '4d':
			if debug: print "get 4d"
			return True
		    
    def vertify_data(self, data):
	if debug: print data
        n = 2
	sum = int('42',16)+int('4d',16)
        for i in range(0, len(data)-4, n):
            #print data[i:i+n]
	    sum=sum+int(data[i:i+n],16)
	versum = int(data[40]+data[41]+data[42]+data[43],16)
	if debug: print sum
        if debug: print versum
	if sum == versum:
	    print "data correct"
	
    def read_data(self):
        data = self.serial.read(22)
        data_hex=data.encode('hex')
        if debug: self.vertify_data(data_hex)
        #pm1_cf=int(data_hex[4]+data_hex[5]+data_hex[6]+data_hex[7],16)
        #pm25_cf=int(data_hex[8]+data_hex[9]+data_hex[10]+data_hex[11],16)
        #pm10_cf=int(data_hex[12]+data_hex[13]+data_hex[14]+data_hex[15],16)
        pm1=int(data_hex[16]+data_hex[17]+data_hex[18]+data_hex[19],16)
        pm25=int(data_hex[20]+data_hex[21]+data_hex[22]+data_hex[23],16)
        pm10=int(data_hex[24]+data_hex[25]+data_hex[26]+data_hex[27],16)
        if debug: print "pm1_cf: "+str(pm1_cf)
        if debug: print "pm25_cf: "+str(pm25_cf)
        if debug: print "pm10_cf: "+str(pm10_cf)
        if debug: print "pm1: "+str(pm1)
        if debug: print "pm25: "+str(pm25)
        if debug: print "pm10: "+str(pm10)
	print " - Data:"
        print "  - pm1: "+str(pm1)
        print "  - pm25: "+str(pm25)
        print "  - pm10: "+str(pm10)
  #Statsd Push
	print " - Data push to StatsD"
	sc = statsd.StatsClient('<IP>', 8125, prefix='com.prochera.cracow.out.pm')
	sc.gauge('pm1',pm1)
	sc.gauge('pm25',pm25)
	sc.gauge('pm10',pm10)
	# THING SPEAk PUSH
	print " - Data push to ThingSpeak"
	params = urllib.urlencode({'field1': pm10,  'field2': pm25 , 'api_key': '<API_KEY>' }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
	    conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print response.status, response.reason
            data = response.read()	
        except:
            print " - Data push to ThinkSpeak failed"
    	print " - Data push completed "
	self.serial.close()
        return data

    def read(self, argv):
        tty=argv[0:]
        self.conn_serial_port(tty)
        if self.check_keyword() == True:
            self.data = self.read_data()
            if debug: print self.data
            return self.data

if __name__ == '__main__': 
    air=g3sensor()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(21, False)
    while True:
        pmdata=0
        try:
        	GPIO.output(21, True)
		print " - Warming ..."
		time.sleep(15)
		print " - Data colelction ..."
		pmdata=air.read("/dev/ttyAMA0")
                GPIO.output(21, False)
 		time.sleep(15) 
        except: 
	     	GPIO.output(21, False)
            	next

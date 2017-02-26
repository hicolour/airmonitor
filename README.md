# airmonitor 

![airmonitor v1](/meta/airmonitor-v1-2.png)
![airmonitor v1](/meta/airmonitor-v1-1.png)
![airmonitor v1](/meta/airmonitor-v1-3.png)

## airmonitor v1
### hardware componenets

 * **PMS*003**
    * [PMS1003](http://aqicn.org/sensor/pms1003/)
    * [PMS3003](http://aqicn.org/sensor/pms3003/)
    * [PMS5003](http://aqicn.org/sensor/pms5003-7003/)
    * [PMS7003](http://aqicn.org/sensor/pms5003-7003/)
 * DHT22 
 * Relay (two on/off primary and slave pm sensor)
 * RaspberryPi A+
 * WiFi Module
 
 
### software componenets

  * Python 2.7
  * [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT)
  
  * **Android ThingSpeak Widgets App** [Google Play](https://play.google.com/store/apps/details?id=ua.livi.thingspeakmonitor)
  
 
### cloud componenets

  * [ThingSpeak IoT](http://thingspeak.com)
  * StatsD-Graphite-Graphana - for in details graphs
  
### case (will not work for v2 which will have two PM sensors, 7003 could fit  )

![1](/meta/airmonitor-v1-1.jpg)
![2](/meta/airmonitor-v1-2.jpg)
![3](/meta/airmonitor-v1-3.jpg)

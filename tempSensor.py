import os
import time
import MySQLdb
from datetime import datetime


class temperatureSensor():

    def __init___(self):
        self.verbose = True
        print('temperatureSensor() class initiated')

    def loadDrivers(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')


    def testOutput(self):
        print('Output Test')


    def readRawTemperature(self, path):
    
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        return lines


    def readTemperature(self, path):
    
        lines = self.readRawTemperature(path)
    
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = temp_raw()

        temp_output = lines[1].find('t=')

        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            temp_c = float(temp_string) / 1000.0
        
        return temp_c



    def recordTemp(self):

        cnx = MySQLdb.connect(host="localhost",
                      user='home', 
                      passwd='password',
                      db='home'
                     )

        cursor_sensor = cnx.cursor()
        query  = ("select * from home.sensor where 1=1 and model = 'DS18B20'")
        cursor_sensor.execute(query) 

        cursor_reading = cnx.cursor()
        insert_str  = "insert into home.sensor_readings values("


        for row in cursor_sensor:
            time_now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            insert_str = insert_str + "'"+time_now+"','"+row[0]+"','"+row[8]+"','TEMP',"+str(self.readTemperature(row[9]))+",'C')"
            print(insert_str)
            cursor_reading.execute(insert_str)


        cursor_sensor.close()
        cursor_reading.close()
        cnx.commit()
        cnx.close()


######################################
######################################











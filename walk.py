import pywapi
import string 
import time
import datetime
from fractions import Fraction
from decimal import Decimal
from datetime import date
points = 0
end = 0

day = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}

weather_com_result = pywapi.get_weather_from_weather_com('USMA0011') 

print "==================================================================="
print "==================================================================="
print "=================== W E A T H E R . C O M ========================="
print "==================================================================="
print "==================================================================="
#time for code!!!

dat = datetime.date.today() + datetime.timedelta(days=1)
dayname = datetime.date.weekday(dat)
for ddd, eee in day.iteritems():
    if dayname == ddd:
        break

for aaa,bbb in weather_com_result.iteritems():
    if aaa == "forecasts":
        tcast = bbb[1]
        for key, value in tcast.iteritems():
            if "high" == key:
                temp = value
            if "day" == key:
                forecast = value
for name, result in forecast.iteritems():
    if "text" == name:
        weather = result
    if "chance_precip" == name:
        precip = int(result)
    if "wind" == name:
        wind = result
for title, data in wind.iteritems():
    if "speed" == title:
        wind_speed = data
temp = int(temp) * 1.8 + 32
print dat
print "temperature: " + str(temp)
print "weather: " + str(weather)
print "precipitation: " + str(precip)
wind = round(int(wind_speed) * 0.6214, 0)
print "wind: " + str(wind)
if temp > 31:
    if temp < 86:
        points = points + round(float(temp)/16, 1)
if "Sunny" in weather:
    if "Mostly Sunny" == weather:
        points = points + 1
    else:
        points = points + 0.5
if "Cloudy" in weather:
    if "Mostly Cloudy" == weather:
        points = points + 1
    else:
        points = points + 0.5
else:
    points = points + 0

if precip <= 20:
    points = points + 5
elif precip >= 80:
    end = end + 1
else:
    predec = 1./(float(precip) / 100)
    points = points + float(Decimal(predec))

if wind <= 20:
    points = points + 3
else:
    points = points + 3 - ((wind - 15)/15) * 3
print "total points: " + str(points)
if end >= 1:
    print "you should not walk!"
else:
    if points > 6:
        print "you should walk!"
    elif points < 8:
        print "you should not walk!"
    else:
        print "you could walk, but you dont really have to. your choice!"

print "Thanks for using this app. \n"
print "Please note that ALL INFO IS A SUGGESTION."
print "IS NOT TO THE FAULT OF VICTOR CHEN THAT YOU DONT WALK ON A SUNNY DAY, OR WALK IN THE COLD RAIN."
print "==============================================================================================="
print "All data is from weather.com. data is retrieved using pywapi 0.3.8."
print "==============================================================================================="
print "Thanks to my science fair advisor, ms.Sullivan and her collegue, Will Gilbert for support and help in the code!"
print "thanks to my parents for the support!"
print "The program would not have been possible without them."
print "==============================================================================================="
print "Thank you :)"
print "Program made by Victor Chen, idea by Victor Chen. DO NOT COPY."

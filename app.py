from flask import Flask
import pywapi
import string 
import time
import datetime
from fractions import Fraction
from decimal import Decimal
from datetime import date
app = Flask(__name__)
@app.route("/")
def hello_world():
    city = input("Enter city name: ")
    lookup = pywapi.get_location_ids(city)
    for i in lookup:
        location_id = i
    weather_com_result = pywapi.get_weather_from_weather_com(location_id)
    points = 0
    end = 0
    day = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
    forecast = 0
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
    wind = round(int(wind_speed) * 0.6214, 0)
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
    if end >= 1:
        return "you should not walk!<br/>" + str(dat) + "<br/>temperature: " + str(temp) + "<br/>weather: " + str(weather) + "<br/>precipitation: " + str(precip) + "%" + "<br/>wind: " + str(wind)
    else:
        if points > 6:
            return "you should walk!<br/>" + str(dat) + "<br/>temperature: " + str(temp) + "<br/>weather: " + str(weather) + "<br/>precipitation: " + str(precip) + "%" + "<br/>wind: " + str(wind) 
        elif points < 8:
            return "you should not walk!<br/>" + str(dat) + "<br/>temperature: " + str(temp) + "<br/>weather: " + str(weather) + "<br/>precipitation: " + str(precip) + "%" + "<br/>wind: " + str(wind)
        else:
           return "you could walk, but you dont really have to. your choice!<br/>" + str(dat) + "<br/>temperature: " + str(temp) + "<br/>weather: " + str(weather) + "<br/>precipitation: " + str(precip) + "%" + "<br/>wind: " + str(wind)
    
    
if __name__ == "__main__":
    app.run()

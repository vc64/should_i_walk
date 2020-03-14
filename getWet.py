from flask import Flask
import json
import datetime
import requests

app = Flask(__name__)


@app.route("/")
def weatherWalk():

    def getWeather():
        url = "http://api.openweathermap.org/data/2.5/forecast?zip=02476,&appid=547a912a67e217c4fece39eddaf081dc"

        results = requests.get(url)

        data = results.json()

        today = datetime.date.today() + datetime.timedelta(days=1)
        # goal is 12pm UTC bc arlington would be 8 am

        datetimeNow = data['list'][0]["dt_txt"]

        timeNow = datetimeNow.split(" ")[1]

        timeHr = int(timeNow[0:2])

        if timeHr >= 12:
            timeDiff = ((24 - timeHr) + 12) // 3
        else:
            timeDiff = (12 - int(timeHr)) % 3

        forecast = data['list'][timeDiff]

        temp = (float(forecast["main"]["temp"]) - 273.15) * 9 / 5 + 32

        wind = float(forecast["wind"]["speed"])

        weather = forecast["weather"][0]["main"]

        details = forecast["weather"][0]["description"]

        return [temp, wind, weather, details, str(today) + '<br/>Temperature: ' + str(temp) + '<br/>Wind Speed: ' + str(wind) + "<br/>Weather: " + weather + "<br/>Details: " + details]

    points = 0
    results = getWeather()
    temp = results[0]
    wind = results[1]
    weather = results[2]
    details = results[3]

    report = results[4]

    if temp < 32:
        points -= 1
    elif temp > 85:
        points -= 1
    elif 75 > temp > 60:
        points += 2
    else:
        points += 1

    if wind <= 5:
        points += 2
    elif wind <= 10:
        points += 1
    elif wind >= 20:
        points -= 2
    elif wind >= 30:
        points -= 10

    if "heavy" in details:
        points -= 10

    if weather == "Clear":
        points += 1
    elif weather == "Snow":
        points -= 5
    elif weather == "Rain":
        if details == "light rain":
            points -= 2
        else:
            points -= 3
    elif weather == "Thunderstorm":
        if details == "light thunderstorm":
            points -= 3
        else:
            points -= 10
    elif weather == "Drizzle":
        if details == "light intesity drizzle":
            points -= 1
        else:
            points -= 3
    elif details == "overcast clouds":
        points -= 1
    else:
        if details == "mist":
            points -= 2
        else:
            points -= 10

    if points >= 5:
        return "walk<br/>" + report
    elif points <= -5:
        return "no walk<br/>" + report
    else:
        return "your choice<br/>" + report


if __name__ == "__main__":
    app.run()

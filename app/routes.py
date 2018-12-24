from flask import render_template
from app import app
import json
import datetime


@app.route('/')
def frontpage():

    # open the data
    with open('scrapedata.json') as json_data:
        data = json.load(json_data)

    week = data.pop("week")

    weekdays = {
        0: "Maanantai",
        1: "Tiistai",
        2: "Keskiviikko",
        3: "Torstai",
        4: "Perjantai",
        5: "Lauantai",
        6: "Sunnuntai"
    }
    weekday = datetime.datetime.today().weekday()
    current_day = weekdays.get(weekday)

    menus = {}
    for restaurant in data:
        try:
            menus[restaurant] = data[restaurant][current_day]
        except KeyError:
            continue

    return render_template('frontpage.html', week=week, day=current_day, menus=menus)


@app.route('/ravintola/<restaurant>')
def ravintola(restaurant):

    # open the data
    with open('scrapedata.json') as json_data:
        data = json.load(json_data)

    week = data.pop("week")

    menus = data[restaurant]

    return render_template('restaurant.html', week=week, restaurant=restaurant, menus=menus)

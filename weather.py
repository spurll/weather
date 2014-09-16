#!/usr/bin/env python

# Written by Gem Newman. This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.


from argparse import ArgumentParser
from datetime import date
from slackutils import Slack
import requests, re

import config


REQUEST = "http://api.openweathermap.org/data/2.5/forecast/daily?q={city}"    \
          "&mode=json&units=metric&cnt=2&APPID={app_id}"
ICON = "http://openweathermap.org/img/w/{code}.png"

MESSAGE = u"Today's temperature is expected to have a high of {high:.0f}"     \
          u"\u00B0C and a low of {low:.0f}\u00B0C. The wind will be {wdir} "  \
          u"{wspd:.0f} km/h. Looking up, you should expect to see {sky} with "\
          u"{cloud:.0f}% cloud cover."
PRECIP = " It looks like {type} today, about {amount:.1f} millimetres."

TERSE_MESSAGE = u"High: {high:.0f}\u00B0C, Low: {low:.0f}\u00B0C\n" \
                u"Wind: {wdir} {wspd:.0f} km/h\nCloud cover: {sky} "          \
                u"({cloud:.0f}%)"
TERSE_PRECIP = "\nPrecipitation: {amount:.1f} mm {type}"


def main():
    parser = ArgumentParser(description="Sends a Slack message containing "
                            "information about today's weather forecast.")
    parser.add_argument("recipient", help="The Slack user(s) or channel(s) to "
                        "to send the message to.", nargs="+")
    parser.add_argument("-c", "--city", help="The city whose weather you would"
                        "like to check. Defaults to {}.".format(
                        config.DEFAULT_CITY), default=config.DEFAULT_CITY)
    parser.add_argument("-n", "--notify", help="Tags the user (or @channel) in"
                        " the message.", action="store_true")
    parser.add_argument("-t", "--terse", help="Delivers the weather with fewer"
                        " words.", action="store_true")
    args = parser.parse_args()

    weather = check_weather(args.city)
    message, icon = format_message(weather, args.terse)

    s = Slack(config.SLACK_TOKEN, name=config.SLACK_USER, verbose=True)
    for recipient in args.recipient:
        s.send(recipient, message, icon=icon, notify=args.notify)


def check_weather(city):
    today = None

    r = requests.get(REQUEST.format(city=city, app_id=config.OWM_TOKEN))

    if r.status_code == 200:
        try:
            today = [f for f in r.json().get("list")
                     if date.fromtimestamp(f["dt"]) == date.today()][0]
            today["precip"] = {key: value for key, value in today.iteritems()
                               if key in ["rain", "snow", "sleet", "hail"]}

        except IndexError as e:
            print "Error: Unable to find weather forecasts for today: {}"     \
                  .format(e)

    else:
        print "Error: Unable to fetch weather data. Request returned: {}"     \
              .format(r.status_code)

    return today


def format_message(weather, terse):
    if weather:
        icon = ICON.format(code=weather["weather"][0]["icon"])

        if terse:
            message = TERSE_MESSAGE
            precip = TERSE_PRECIP
        else:
            message = MESSAGE
            precip = PRECIP

        message = message.format(
            high=weather["temp"]["max"],
            low=weather["temp"]["min"],
            wdir=direction(weather["deg"], terse),
            wspd=weather["speed"] * 3.6,
            sky=weather["weather"][0]["description"],
            cloud=weather["clouds"]
        )

        for key, value in weather["precip"].iteritems():
            message += precip.format(type=key, amount=value)

    else:
        message = "Unable to fetch weather data."
        icon = None

    return message, icon


def direction(degrees, terse):
    if (degrees > 360 - 11.25) or (degrees <= 11.25):
        wind = "N" if terse else "north"
    elif (degrees > 11.25) and (degrees <= 22.5 * 2 - 11.25):
        wind = "NNE" if terse else "north-northeast"
    elif (degrees > 22.5 * 2 - 11.25) and (degrees <= 22.5 * 3 - 11.25):
        wind = "NE" if terse else "northeast"
    elif (degrees > 22.5 * 3 - 11.25) and (degrees <= 22.5 * 4 - 11.25):
        wind = "ENE" if terse else "east-northeast"
    elif (degrees > 22.5 * 4 - 11.25) and (degrees <= 22.5 * 5 - 11.25):
        wind = "E" if terse else "east"
    elif (degrees > 22.5 * 5 - 11.25) and (degrees <= 22.5 * 6 - 11.25):
        wind = "ESE" if terse else "east-southeast"
    elif (degrees > 22.5 * 6 - 11.25) and (degrees <= 22.5 * 7 - 11.25):
        wind = "SE" if terse else "southest"
    elif (degrees > 22.5 * 7 - 11.25) and (degrees <= 22.5 * 8 - 11.25):
        wind = "SSE" if terse else "south-southeast"
    elif (degrees > 22.5 * 8 - 11.25) and (degrees <= 22.5 * 9 - 11.25):
        wind = "S" if terse else "south"
    elif (degrees > 22.5 * 9 - 11.25) and (degrees <= 22.5 * 10 - 11.25):
        wind = "SSW" if terse else "south-southwest"
    elif (degrees > 22.5 * 10 - 11.25) and (degrees <= 22.5 * 11 - 11.25):
        wind = "SW" if terse else "southwest"
    elif (degrees > 22.5 * 11 - 11.25) and (degrees <= 22.5 * 12 - 11.25):
        wind = "WSW" if terse else "west-southwest"
    elif (degrees > 22.5 * 12 - 11.25) and (degrees <= 22.5 * 13 - 11.25):
        wind = "W" if terse else "west"
    elif (degrees > 22.5 * 13 - 11.25) and (degrees <= 22.5 * 14 - 11.25):
        wind = "WNW" if terse else "west-northwest"
    elif (degrees > 22.5 * 14 - 11.25) and (degrees <= 22.5 * 15 - 11.25):
        wind = "NW" if terse else "northwest"
    elif (degrees > 22.5 * 15 - 11.25) and (degrees <= 360 - 11.25):
        wind = "NNW" if terse else "north-northwest"

    return wind


if __name__ == "__main__":
    main()


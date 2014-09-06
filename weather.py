#!/usr/bin/env python

# Written by Gem Newman. This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from argparse import ArgumentParser
import requests, re

import config


REQUEST = "http://api.openweathermap.org/data/2.5/forecast/daily?q={city}"    \
          "&mode=xml&units=metric&cnt=1&APPID={app_id}"
ICON = "http://openweathermap.org/img/w/{code}.png"

MESSAGE = u"Today's temperature is expected to have a high of {high:.0f}"     \
          u"\u00B0C and a low of {low:.0f}\u00B0C. The wind will be {wdir} "  \
          u"{wspd:.0f} km/h. Looking up, you should expect to see {cloud}."
PRECIP = " It looks like {type} today, about {amount:.1f} millimetres."

TERSE_MESSAGE = u"Temperature: {high:.0f}\u00B0C (H), {low:.0f}\u00B0C (L)\n" \
                u"Wind: {wdir} {wspd:.0f} km/h\nCloudcover: {cloud}"
TERSE_PRECIP = "\nPrecipitation: {amount:.1f} mm {type}"


def main():
    parser = ArgumentParser(description="Sends a Slack message containing "
                            "information about today's weather forecast.")
    parser.add_argument("recipient", help="The Slack user(s) or channel(s) to "
                        "to send the message to.", nargs="+")
    parser.add_argument("-c", "--city", help="The city whose weather you would"
                        "like to check. Defaults to {}.".format(
                        config.DEFAULT_CITY), default=config.DEFAULT_CITY)
    parser.add_argument("-t", "--terse", help="Delivers the weather with fewer"
                        "words.", action="store_true")
    args = parser.parse_args()

    weather = check_weather(args.city)
    message, icon = format_message(weather, args.terse)

    for recipient in args.recipient:
        destination = determine_destination(recipient)
        send_message(destination, message, icon)


def determine_destination(destination):
    if destination[0] in ["#", "@"]:
        return destination

    candidates = []

    pattern = re.compile(r"{}".format(destination), re.IGNORECASE)

    for i in list_users() + list_channels():
        match = re.search(pattern, i["name"])

        # Users have a "real name" in addition to their user name.
        if not match and "real" in i:
            match = re.search(pattern, i["real"])

        if match: candidates.append(i["id"])

    if len(candidates) == 1:
        return candidates[0]

    if not candidates:
        print 'Error: No users or channels named "{}".'.format(destination)
    else:
        print "Error: Unable to identify destination. Possible matches: {}"   \
              .format(", ".join(candidates))

    return None


def list_users():
    users = []

    payload = {"token": config.SLACK_TOKEN}
    r = requests.post("https://slack.com/api/users.list", data=payload)

    if check_response(r):
        users = [{"slack_id": m["id"],
                  "id": "@{}".format(m["name"]),
                  "name": m["name"],
                  "real": m["real_name"]}
                 for m in r.json()["members"]]

    return users


def list_channels():
    channels = []

    payload = {"token": config.SLACK_TOKEN, "exclude_archived": 1}
    r = requests.post("https://slack.com/api/channels.list", data=payload)

    if check_response(r):
        channels = [{"slack_id": c["id"],
                     "id": "#{}".format(c["name"]),
                     "name": c["name"]}
                    for c in r.json()["channels"]]

    return channels


def check_weather(city):
    weather = {}

    r = requests.get(REQUEST.format(city=city, app_id=config.OWM_TOKEN))

    if r.status_code == 200:
        root = ET.fromstring(r.text)
        forecast = root.find("forecast")[0]

        weather["symbol"] = forecast.find("symbol").attrib
        weather["temperature"] = forecast.find("temperature").attrib
        weather["precip"] = forecast.find("precipitation").attrib
        weather["wind_spd"] = forecast.find("windSpeed").attrib
        weather["wind_dir"] = forecast.find("windDirection").attrib
        weather["cloud"] = forecast.find("clouds").attrib

    else:
        print("Error: Unable to fetch weather data. Request returned {}."
              .format(r.status_code))

    return weather


def format_message(weather, terse):
    if weather:
        icon = ICON.format(code=weather["symbol"]["var"])

        if terse:
            message = TERSE_MESSAGE.format(
                high=float(weather["temperature"]["max"]),
                low=float(weather["temperature"]["min"]),
                wdir=weather["wind_dir"]["code"],
                wspd=float(weather["wind_spd"]["mps"]) * 3.6,
                cloud=weather["cloud"]["all"] + weather["cloud"]["unit"]
            )

            if weather["precip"]:
                message += TERSE_PRECIP.format(
                    type=weather["precip"]["type"],
                    amount=float(weather["precip"]["value"])
                )

        else:
            message = MESSAGE.format(
                high=float(weather["temperature"]["max"]),
                low=float(weather["temperature"]["min"]),
                wdir=weather["wind_dir"]["name"].lower(),
                wspd=float(weather["wind_spd"]["mps"]) * 3.6,
                cloud=weather["cloud"]["value"]
            )

            if weather["precip"]:
                message += PRECIP.format(
                    type=weather["precip"]["type"],
                    amount=float(weather["precip"]["value"])
                )

    else:
        message = "Unable to fetch weather data."
        icon = None

    return message, icon


def send_message(destination, message, icon):
    payload = {"token": config.SLACK_TOKEN,
               "channel": destination,
               "username": config.SLACK_USER,
               "icon_url": icon,
               "link_names": 1,
               "text": message}
    r = requests.post("https://slack.com/api/chat.postMessage", data=payload)

    if check_response(r):
        print "Message delivered to {}.".format(destination)


def check_response(r):
    # Check the HTTP response.
    if r.status_code != 200:
        print "HTTP Code {}: {}".format(r.status_code, r.text)
        return False

    # Request was successful. Now check Slack's response.
    if not r.json()["ok"]:
        print "Slack Error: {}".format(r.json()["error"])
        return False

    return True


if __name__ == "__main__":
    main()


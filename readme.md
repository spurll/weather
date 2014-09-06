Weather Message
===============

Sends a Slack message containing information about today's weather forecast.

Installation
============

Configuration
-------------

You'll need to create a file called `config.py` containing your Slack API token (which can be obtained from the [Slack API page](http://api.slack.com)) and the desired user name for your bot. These must be named `SLACK_TOKEN` and `SLACK_USER`, respectively.

The configuration file must also contain an OpenWeatherMap API token (you'll have to [sign up for OpenWeatherMap](http://openweathermap.org/appid)) and the name of the city whose weather you're interested in (this city can by overridden on the command line). These must be named `OWM_TOKEN` and `DEFAULT_CITY`.

For example:

```python
SLACK_TOKEN = 'XXXX-XXXX-XXXX-XXXX-XXXX'
SLACK_USER = 'BotName'

OWM_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
DEFAULT_CITY = 'Winnipeg'
```

Requirements
------------

* Slack (this one is sort of key)
* requests

Bugs and Feature Requests
=========================

Feature Requests
----------------

* Add custom icon support
* Should probably use the JSON API instead of XML

Known Bugs
----------

None

Slack
=====

Information about Slack is available on [their website](http://www.slack.com). Information about the Slack API is available [here](http://api.slack.com).

OpenWeatherMap
==============

Information about OpenWeatherMap is available on [their website](http://openweathermap.org). Information about their API is available [here](http://openweathermap.org/api).

License Information
===================

Written by Gem Newman. [GitHub](https://github.com/spurll/) | [Blog](http://www.startleddisbelief.com) | [Twitter](https://twitter.com/spurll)

This work is licensed under Creative Commons [BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/). Use of the OpenWeatherMaps API is subject to the Creative Commons [BY-SA 2.0](http://creativecommons.org/licenses/by-sa/2.0/) license.


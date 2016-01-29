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

* requests
* [slackutils](https://github.com/spurll/slackutils/)

Bugs and Feature Requests
=========================

Feature Requests
----------------

* Currently uses icons provided by OpenWeatherMap, but support for a set of custom icons would be great.

Known Bugs
----------

None

Slack
=====

Information about Slack is available on [their website](http://www.slack.com). Information about the Slack API is available [here](http://api.slack.com).

OpenWeatherMap
==============

Information about OpenWeatherMap is available on [their website](http://openweathermap.org). Information about their API is available [here](http://openweathermap.org/api).

Special Thanks
==============

This was [BCJ](https://github.com/bcj)'s idea.

License Information
===================

Written by Gem Newman. [Website](http://spurll.com) | [GitHub](https://github.com/spurll/) | [Twitter](https://twitter.com/spurll)

This work is licensed under Creative Commons [BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).

Remember: [GitHub is not my CV.](https://blog.jcoglan.com/2013/11/15/why-github-is-not-your-cv/)

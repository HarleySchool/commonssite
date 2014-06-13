Commons Control Data Collection
===============================

This is the source for the Harley School's [Commons Control](http://commonscontrol.harleyschool.org) website. The codebase includes both a standard web server, and data scrapers which periodically collect and store data from the various smart systems in the building.

---

<!--BREAK-->
<!--Table of contents will go here-->
<!--BREAK-->

Server
------

Commons Control uses [Django 1.6](http://docs.djangoproject.com) for the server logic. What this means is that whenever somebody uses their browser to interact with `commonscontrol.harleyschool.org`, the python code in the `server/` directory is executed to form a response. The response is typically an html page, but there are other functions as well.

Django provides a _framework_ on which the site is built, but it does not provide content. Here's a truncated list of Django's features:

* handles all network transactions (communicating back and forth with the client's browser)
* auto-generated admin pages so non-coders can do password-protected database management
* a template language for generating HTML pages on-the-fly.
* database Object-Relational Mapping (ORM). This is a fancy code term for "making database data and transactions easy to manipulate in code".
* database management. Django and an app called South work together to automate, as much as possible, managing and migrating the database
* ...and tons of other features which we don't use

Django is very well documented. Most questions can be answered by reading their docs.

__Directory Structure__

Originally this was not a django project. An artifact of the old-ways is that the `server/` directory is not the root directory, we have two settings files, and the imports are somewhat inconsistent.

`scrapers/` contains the threaded scheduler we use to scraped data. Running it looks like this (make sure your virtualenv is activated first):

    cd server # because imports are broken
    python ../scrapers/log_continuous.py

`server/` contains the django server. It is a mixture of auto-generated and custom files. `server/manage.py` is the django management program from whence all server control begins.

`server/webapp/` contains metadata about the server, like the server settings and wsgi script

`server/static/` contains global static files like shared CSS styles and javascript

`server/static/js/commonsapi.js` contains our small custom javascript class with convenience functions for interacting with the server API from a browser.

`server/hvac/`, `server/electric`/, etc. are our custom django apps. In `server/webapp/settings.py`, we can activate or deactivate apps by adding/removing them from `INSTALLED_APPS`. That is also how django knows where to look for our code.

`server/timeseries/` is our super-app. It is the generic data-manipulation app which pulls in information from the other systems apps.

`server/timeseries/models.py` contains the generic 'base' model as well as the `ModelRegistry` model, and a model for saving generic `Series`

`server/timeseries/scrapers.py` contains the generic base scraper class

`server/timeseries/urls.py` is a small file which django uses to determine how URLs are mapped to views (i.e. python functions).

`server/timeseries/views/*` contain code that is first executed when a client connects to the server.

`server/timeseries/helpers.py` contains most of the server logic. This is the file to read if you need to understand the API format.

`server/timeseries/templates/timeseries/*` are the template files used to build all of the "analyze" UI

`server/mysystem/models.py` (where `mysystem` is 'hvac', 'electic', 'solar', etc...) contains classes which define the database tables (models) for that system. Models that extend `TimeseriesBase` can be registered in the `ModelRegistry` (thereby automatically plugging in to the graph/download/status functions)

`server/mysystem/scrapers.py` contains classes which extend `ScraperBase` and handle both connecting to that system's data server, and converting from their format to one of the Models. These are the classes which are executed by `log_continuous.py`.

Front-End
-----------

The [Django templating language](https://docs.djangoproject.com/en/dev/topics/templates/) provides a way to translate from python state to formatted HTML. For example, the `/status` page is generated on the server by looping over the systems returned by `helpers.systems_schema` and creating a table row for each one.

JavaScript and [JQuery](https://http://api.jquery.com/) are the in-browser scripting languages. They handle communication with the server. Live graphs are made by having javascript periodically request new data from the server with AJAX.

We use [HighCharts](http://www.highcharts.com/) to make graphs. HighCharts is free for non-profit sites. Everything that makes our graphs pretty, interactive, and animated comes from HighCharts. We are responsible for coming up with the data.

Twitter's [Bootstrap](http://getbootstrap.com/) is an easy way to make things look good and work well across browsers and screen sizes. Bootstrap manages our page layouts. We also use two bootstrap extensions: [Multiselect](http://davidstutz.github.io/bootstrap-multiselect/) for the drop-down menus, and [Date Range Picker](https://github.com/dangrossman/bootstrap-daterangepicker) for the calendars on analyze.html.

Contributing
-----------

Before you start writing code, you will want to set up a local testing environment on your computer. To do so, follow the instructions [on this wiki page](https://github.com/HarleySchool/commonssite/wiki/Getting-Started-%28on-Mac-or-Linux%29).

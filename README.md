Commons Control Data Collection
===============================

If you plan on making changes to the data collection system, please read this document first! There are many interacting systems each with their own code and their own rules.

Updated April 2, 2014

---

<!--BREAK-->
<!--Table of contents will go here-->
<!--BREAK-->

Back-End
-----------

Commons Control uses [Django](http://docs.djangoproject.com) for the server logic (aka "back-end"). What this means is that whenever somebody uses their browser to interact with `commonscontrol.harleyschool.org`, the python code in the `server/` directory is executed to form a response. The response is typically an html page, but there are other pages which create and serve csv files (or do anything else we want!).

To get started contributing, follow the instructions [on this wiki page](https://github.com/HarleySchool/commonssite/wiki/Getting-Started-%28on-Mac-or-Linux%29).

Front-End
-----------

We use the Django template language to generate HTML pages.

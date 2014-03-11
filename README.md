<style type="text/css"> *{font-family:arial,helvetica,sans-serif;}</style>

Commons Control Data Collection
===============================

If you plan on making changes to the data collection system, please read this document first! There are many interacting systems each with their own code and their own rules.

Updated February 11, 2014

---

<!--BREAK-->
<!--Table of contents will go here-->
<!--BREAK-->

The Web-App
-----------

Commons Control uses [Django](http://docs.djangoproject.com) for the server logic. What this means is that whenever somebody uses their browser to interact with `commonscontrol.harleyschool.org`, the pthon code in the `webapp/` directory is executed to form a response. The response is typically an html page, but there are other pages which create and serve csv files.


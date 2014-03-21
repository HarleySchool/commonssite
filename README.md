<style type="text/css"> *{font-family:arial,helvetica,sans-serif;}</style>

Commons Control Data Collection
===============================

If you plan on making changes to the data collection system, please read this document first! There are many interacting systems each with their own code and their own rules.

Updated February 11, 2014

---

<!--BREAK-->
<!--Table of contents will go here-->
<!--BREAK-->

Back-End
-----------

Commons Control uses [Django](http://docs.djangoproject.com) for the server logic (aka "back-end"). What this means is that whenever somebody uses their browser to interact with `commonscontrol.harleyschool.org`, the python code in the `server/` directory is executed to form a response. The response is typically an html page, but there are other pages which create and serve csv files (or do anything else we want!).

__setting up your Mac or Linux computer for back-end development__:

1. Ask me (rlange at harleyschool dot org) for permission to access the code on [GitHub](http://github.com).
2. Make a directory "~/code" on your machine
3. From the command-line, navigate to "~/code" and run `git clone git@github.com:wrongu/commonssite.git`
4. (if you don't have it already, install [Python](https://www.python.org/download/) and [pip](http://www.pip-installer.org/en/latest/installing.html). You can check if you have them by running `which python` and `which pip` from the command line).
5. Download and install [virtualenv](http://virtualenv.org) with pip by running `sudo pip install virtualenv` (if you aren't an administrator on your computer, install it locally with `pip install virtualenv --user`)
6. Make a directory "~/.virtualenv". Go there in the command line and run `virtualenv --system-site-packages Django` (if you installed virtualenv with `--user`, you may need to find where it is first.. on my machine it was "~/.local/bin/virtualenv")
7. Open the file "~/.virtualenv/Django/bin/activate" with your editor of choice. In the blank space after "export PATH", add the following:

		export PYTHONPATH="~/code:$PYTHONPATH"
		export DJANGO_SETTINGS_MODULE="commonssite.server.webapp.settings"

8. That's pretty much it for setup! Now when you run `source ~/.virtualenv/Django/bin/activate`, you should be able to run any of the code in the commonssite repository. Just type `deactivate` to get out of that virtual environment. Since that's a lot of typing, a shortcut is to modify "~/.bash_aliases" (or "~/.bashrc" if it doesn't exist) with the following:

		alias djenv='source ~/.virtualenv/Django/bin/activate'

Now run `source ~/.bashrc`, and you should be able to start our new Django environment just by typing `djenv`

Front-End
-----------

We use the Django template language to generate HTML pages.
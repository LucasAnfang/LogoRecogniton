 /$$                                        /$$$$$$$            /$$                        /$$    /$$                          /$$$$$$     /$$$$$$
| $$                                       | $$__  $$          | $$                       | $$   |__/                         /$$__  $$   /$$$_  $$
| $$       /$$$$$$  /$$$$$$  /$$$$$$       | $$  \ $$ /$$$$$$ /$$$$$$   /$$$$$$  /$$$$$$$/$$$$$$  /$$ /$$$$$$ /$$$$$$$       |__/  \ $$  | $$$$\ $$
| $$      /$$__  $$/$$__  $$/$$__  $$      | $$  | $$/$$__  $|_  $$_/  /$$__  $$/$$_____|_  $$_/ | $$/$$__  $| $$__  $$        /$$$$$$/  | $$ $$ $$
| $$     | $$  \ $| $$  \ $| $$  \ $$      | $$  | $| $$$$$$$$ | $$   | $$$$$$$| $$       | $$   | $| $$  \ $| $$  \ $$       /$$____/   | $$\ $$$$
| $$     | $$  | $| $$  | $| $$  | $$      | $$  | $| $$_____/ | $$ /$| $$_____| $$       | $$ /$| $| $$  | $| $$  | $$      | $$        | $$ \ $$$
| $$$$$$$|  $$$$$$|  $$$$$$|  $$$$$$/      | $$$$$$$|  $$$$$$$ |  $$$$|  $$$$$$|  $$$$$$$ |  $$$$| $|  $$$$$$| $$  | $$      | $$$$$$$$/$|  $$$$$$/
|________/\______/ \____  $$\______/       |_______/ \_______/  \___/  \_______/\_______/  \___/ |__/\______/|__/  |__/      |________|__/\______/
                  /$$  \ $$
                 |  $$$$$$/
                  \______/

Setup:
  1) Current version supported is python 2.7
    $ sudo chown -R $USER /Library/Python/2.7 (If do not have this setup open terminal and enter command)

  2) Setup pip and a virtual environment to maintain all the packages (You could use anaconda instead of virtual env)
    $ sudo easy_install pip
    $ sudo pip install --upgrade virtualenv
    $ python -m virtualenv custom-env-name (Create your virtual env)

  3) Activate your virtual env
    source custom-env-name/bin/activate (This will activate your virtual env session allowing you to add packages using pip)
    (To deactivate the session just type the command 'deactivate')

  4) First install all needed packages for this project using the requirements.txt file
    $ pip install -r requirements.txt (If you need to add a new package to your project add it to the requirements file so all can have it)

Current Objectives:
  Investigate:
  Containerization of our processes and use Kubernetes & Docker or another viable container management utility.

  Processing Drivers:
  Build out the driver to use a logging table instead of log files (serialized custom log objects) at various positions in the networked file system
  Build in a processing Queue(/Logging Table?)for work to accumulate so one or more drivers can be spun up to process from the same work queue at the same time

  Networked File System:
  Build more functional to make multithreading current feature set easier. Utilize tqdm to show progress instead of prints.
  Current Logging structure has serialized logs at specific points but this means making multiple requests to first get all
  of the brands then use this info to create the paths and see if logs are at those domains THEN downloading and deserializing
  these logs to just find a few buckets needing processing (This is a nightmare that needs to stop). Make a log database for this
  that maintains timestamps and recent actions taken. This will be easier to make changes to and maintain.

  Web App:
  The current Instagram scraper is open source built in python. The web app needs to be able to call the scraper and query/manage
  various database tables (log table, processed posts table, etc.)

  Instagram Scraper:
  Build out the scraper with finer tuned queries of Instagram's data to further the goal of finding users and understanding a brand's image
  https://docs.microsoft.com/en-us/azure/sql-database/sql-database-connect-query-python
  https://docs.microsoft.com/en-us/sql/connect/python/python-driver-for-sql-server
  https://docs.microsoft.com/en-us/azure/app-service/app-service-web-get-started-python

Cool Tools:
  TQDM:
    Link: https://pypi.python.org/pypi/tqdm
    Note: tqdm provides an easy system for adding progress bars that are very helpful to gage cycle timing and visualize a long progress
  NOSE:
    Link: https://pypi.python.org/pypi/nose/1.3.7
    Note: nose is a useful library for TDD (Test driven development)
Other Helpful Commands:
  find . -name \*.pyc -delete (delete all pyc files)

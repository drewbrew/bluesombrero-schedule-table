# Blue Sombrero calendar table generator

## What is this?

If your local soccer team uses Blue Sombrero/Stack Sports/Stack Connect/etc. for its player/team management system, it supports a `webcal://` export link that you can import into your Google/Apple/Microsoft/Yahoo/etc. calendar for viewing wherever.

However, I've found that some parents don't like relying on their phones for everything and like to have a more at-a-glance view. This enables you generate a quick and easy table setup to send to your team as a coach or team parent.

## How do I use this?
1. [Install Python 3.12](https://wsvincent.com/install-python/). Will's guide is a great resource for any computer.
2. Install [pipenv](https://pipenv.pypa.io/en/latest/installation.html).  This is what I use for dependency management, and since this is an extremely simple app, it always makes sure you get the latest and greatest.
3. From a command prompt/terminal in this directory, run `pipenv run flask run`. (Yes, the use of `run` twice is intentional).
4. You'll see a warning that this is not for production use (good) and  then `* Running on http://127.0.0.1:5000`. Yay!
5. Open http://127.0.0.1:5000/ on your web browser of choice.
6. Paste the webcal link (see below for how to get it).
7. Click submit.
8. Enjoy the table in all its web 0.5 glory.

## Wait, how do I get my webcal link?

**Note**: these instructions only apply for [AYS0 498](https://ayso498.org) in Madison, AL.  You'll have to navigate your own team's setup, but this should give you a rough idea.

1. Log in to your team's Stack Sports portal.
2. Once you're on the "My Account" page, scroll down to the notification feed.
3. You should see a notification that your child was added to a specific team. Click that notification.
4. That will take you to the Team Directory inside the Team Central heading. Go to the Calendar tab.
5. You'll see an Agenda view. In the top right, there are print and export buttons. Click Export.
6. In the modal dialog that pops up, you should see a `webcal://calendar.bluesombrero.com/...` link already highlighted. Right-click on that and choose Copy.
7. Return to the form above.

## How can I customize this?
1. Change your time zone. Since AYSO 498 is in Central Time, the default is America/Chicago.
2. Change your team colors: the default is blue vs red, and you can adjust them in [style.css](static/style.css) at the bottom of the file to change the background colors, and you also need to change the color names in [app.py](/app.py).

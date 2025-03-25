"""Simple app for rendering a game schedule into a table form"""

from collections import Counter
import datetime
from dataclasses import dataclass
from collections.abc import Iterable
import zoneinfo

from flask import Flask, render_template, request, abort
from icalendar.cal import Calendar, Event
import requests


HOME_TEAM_COLOR = "blue"
AWAY_TEAM_COLOR = "red"

TIME_ZONE = zoneinfo.ZoneInfo("America/Chicago")


app = Flask(__name__)


@dataclass
class Game:
    title: str
    start: datetime.datetime
    end: datetime.datetime
    location: str
    home_team: str = ""
    visiting_team: str = ""

    @classmethod
    def from_ical_event(cls, event: Event):
        start: datetime.datetime = event.decoded("dtstart")
        if "duration" in event:
            end: datetime.datetime = event.decoded(
                "dtend", default=start + event.decoded("duration")
            )
        else:
            end = event.decoded("dtend", default=start)
        description = event.get("description", "").split("\n")
        description = "\n".join(map(lambda s: s.rjust(len(s) + 5), description))
        summary: str = event.get("summary", default="")
        home_team = ""
        visiting_team = ""
        if " Vs " in summary:
            home_team, visiting_team = (i.strip() for i in summary.split(" Vs "))
        return cls(
            title=summary,
            start=start.astimezone(TIME_ZONE),
            end=end.astimezone(TIME_ZONE),
            location=description,
            home_team=home_team,
            visiting_team=visiting_team,
        )


def fetch_url(url: str) -> str:
    """Fetch a calendar from a URL and return the data"""
    if url.startswith("webcal://"):
        url = url.replace("webcal://", "https://")
    response = requests.get(url)
    response.raise_for_status()
    return response.content.decode()


def parse_calendar(calendar_data: str) -> Calendar:
    return Calendar.from_ical(calendar_data)


def parse_event(event: Event) -> Game:
    """Parse an ical event for ease of display in a table"""
    return Game.from_ical_event(event)


def identify_my_team(games: Iterable[Game]) -> str:
    """Given some games, pick the team for whom this schedule was generated

    Hint: it's the one that appears every week
    """
    teams: list[str] = []
    for game in games:
        teams.extend((game.home_team, game.visiting_team))
    counter = Counter(teams)
    return counter.most_common(1)[0][0]


@app.route("/", methods=["GET", "POST"])
def main():
    """The basic page"""
    if request.method == "GET":
        return render_template("home.html")

    try:
        url = request.form["url"]
    except KeyError:
        abort(400, "bad form data")
    if not url:
        abort(400, "bat form data")
    cal_data = fetch_url(url)
    calendar = parse_calendar(cal_data)
    games = [parse_event(game) for game in calendar.walk("vevent")]
    my_team = identify_my_team(games=games)
    print(f"{my_team=}")
    return render_template(
        "schedule.html",
        games=games,
        my_team=my_team,
        home_color_name=HOME_TEAM_COLOR,
        away_color_name=AWAY_TEAM_COLOR,
    )

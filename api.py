from flask import Flask, g, jsonify, request, make_response, render_template
from icalevents import icalevents
from datetime import date, timedelta
import requests
import os
import bccocal
from babel.dates import format_date, format_time

app = Flask(__name__)

locale = 'de_DE'

@app.route('/', methods=["GET"])
def get_index():
    return "TBD"

@app.route('/week', methods=["GET"])
def show_week():
    c = bccocal.BccoCalendar(os.environ["BCCO_CALENDAR_URL"])
    today = date.today() - timedelta(7)
    all_events = c.get_events_for_week(today)
    start = min(all_events.keys())
    end = max(all_events.keys())
    model = {
        'church': "Linnenbach",
        'start': fd(start),
        'end': fd(end),
        'days': [
            get_day_model(date, events)
            for (date, events)
            in all_events.items()],
    }
    return render_template('week.html', model=model)

def get_day_model(date, events):
    return {
        'name': format_date(date, 'EE', locale=locale),
        'date': format_date(date, 'dd.MM.', locale=locale),
        'events': [get_event_model(e) for e in events],
    }

def get_event_model(event):
    return {
        'title': event['name'],
        'begin': ft(event['begin']),
        'end': ft(event['end']),
        'style': get_style(event),
        'classes': ' '.join(event['tags']),
    }

def get_style(event):
    return "grid-row: {0} / {1}".format(
        get_time_index(event['begin']),
        get_time_index(event['end'])
    )

def get_time_index(time):
    base = (time.hour - 8) * 2 + 1
    if time.minute < 15:
        return base
    elif time.minute < 45:
        return base + 1
    else:
        return base + 2

def fd(date):
    return format_date(date, locale=locale)

def ft(time):
    return format_time(time, format='short', locale=locale)
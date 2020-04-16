from flask import Flask, g, jsonify, request, make_response
import requests
import os
from ics import Calendar

app = Flask(__name__)

@app.route('/', methods=["GET"])
def get_index():
    cal_ur = os.environ["BCCO_CALENDAR_URL"]
    data = requests.get(cal_ur)
    calendar = Calendar(data.text)
    result = {}
    for event in calendar.events:
        if event.status == "CONFIRMED":
            result[event.uid] = {
                "name": event.name,
                "tags": get_tags(event.description),
                "begin": event.begin.datetime,
                "end": event.end.datetime,
            }
    return jsonify(result)

def get_tags(description):
    tags = ['#BCC', '#BUK', '#ZOOM']
    return [t for t in tags if t in description.upper()]
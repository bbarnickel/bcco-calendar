import requests
from icalevents import icalevents
from datetime import timedelta

class BccoCalendar:
    def __init__(self, url):
        data = requests.get(url)
        self.content = data.text

    def get_events_for_week(self, date):
        start, end = _calc_week(date)
        return self._get_events(start, end)

    def _get_events(self, start, end):
        events = icalevents.events(
            string_content=self.content.encode('utf-8'),
            start=start,
            end=end)
        current = start
        result = {}
        while current <= end:
            result[current] = [
                {
                    "name": event.summary,
                    "tags": _get_tags(event.description),
                    "begin": event.start,
                    "end": event.end,
                }
                for event in events
                if event.start.date() == current
            ]

            current += timedelta(1)
        return result


def _calc_week(date):
    delta = timedelta(date.weekday())
    start = date - delta
    end   = start + timedelta(6)
    return (start, end)    


def _get_tags(description):
    tags = ['#bcc', '#buk', '#zoom', '#frakaare', '#kids', '#stream', '#bmm']
    return [t[1:] for t in tags if t in description.lower()]
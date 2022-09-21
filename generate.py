import pathlib
import requests
import lxml.html
from icalendar import Calendar, Event, Timezone
from datetime import datetime, timedelta

URL = "https://www.inf.upol.cz/vyzkum/seminare"

if __name__ == "__main__":
    response = requests.get(URL)

    tree = lxml.html.fromstring(response.text)

    seminars = tree.xpath("/html/body/main/div[1]/table")[0]

    cal = Calendar()
    timezone = Timezone()

    timezone.add("tzid", "Europe/Prague")
    
    cal.add_component(timezone)

    for event in seminars.findall("tr"):
        date, info = event.findall("td")
        date = date.text.strip()
        name, _, talk, time_place = [text.strip("\n") for text in info.itertext()]
        time, place = time_place.split(", ")

        date_time = datetime.strptime(
            f"{date} {datetime.today().year} {time}", "%d. %m. %Y %H:%M"
        )

        event = Event()

        event.add("summary", f"{talk} - {name}")
        event.add("dtstart", date_time)
        event.add("dtend", date_time + timedelta(hours=1))
        event.add("location", "17. listopadu 12 Olomouc, Czechia")
        event.add("URL", "https://www.inf.upol.cz/vyzkum/seminare")
        event.add("description", f"room {place.strip()}")

        cal.add_component(event)

    pathlib.Path("kmi_seminar.ics").write_bytes(cal.to_ical())

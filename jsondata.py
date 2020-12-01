import requests
import json
import plotly.express as px
import sys
from operator import itemgetter
from datetime import datetime, timedelta

def retrieveData (startDate, endDate):
    r = requests.get ('http://data.chesapeakebay.net/api.JSON/WaterQuality/WaterQuality/{0}/{1}/6/23/Station/1730/123'.format(startDate, endDate))
    rows = json.loads (r.text)
    filteredRows = []
    for row in rows:
        if row ["Depth"] == 8:
            filteredRows.append(row)
    sortedlist = sorted(filteredRows, key=itemgetter('SampleDate'))
    fig = px.line(sortedlist, x = "SampleDate", y = "MeasureValue", title = 'Historic Oxygen Levels')
    fig.write_image("fig1.png")

now = datetime.now()
startDate = now - timedelta(days = 365*2)

startFormat = startDate.strftime("%m-%d-%Y")
endFormat = now.strftime("%m-%d-%Y")
retrieveData (startFormat, endFormat)

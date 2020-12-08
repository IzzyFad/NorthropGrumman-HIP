import requests
import json
import plotly.express as px
import sys
from operator import itemgetter
from datetime import datetime, timedelta

def retrieveData (startDate, endDate, parameterID, dataTitle,outputFileName, measuredDepth, units):
    r = requests.get ('http://data.chesapeakebay.net/api.JSON/WaterQuality/WaterQuality/{0}/{1}/6/23/Station/1730/{2}'.format(startDate, endDate, parameterID))
    rows = json.loads (r.text)
    filteredRows = []
    for row in rows:
        if row ["Depth"] == measuredDepth:
            filteredRows.append(row)
    sortedlist = sorted(filteredRows, key=itemgetter('SampleDate'))
    fig = px.line(sortedlist, x = "SampleDate", y = "MeasureValue", title = dataTitle)
    fig.write_image("docs/{0}.png".format(outputFileName))

now = datetime.now()
startDate = now - timedelta(days = 365*2)

startFormat = startDate.strftime("%m-%d-%Y")
endFormat = now.strftime("%m-%d-%Y")
retrieveData (startFormat, endFormat, 31, "Historical Oxygen Levels", "oxygen", 8, "MG/L")
retrieveData (startFormat, endFormat, 109, "Historical Total Nitrogen Levels", "nitrogen", 0.5, "MG/L")
retrieveData (startFormat, endFormat, 114, "Historical Total Phosphorous Levels", "phosphorous", 0.5, "MG/L")
retrieveData (startFormat, endFormat, 85, "Historical Turbidity Levels", "turbidity", 0.5, "Meters")
retrieveData (startFormat, endFormat, 123, "Historical Water Temperature Levels", "temperature", 4, "Degrees Celsius")

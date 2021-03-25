import requests
import json
import plotly.express as px
import sys
from operator import itemgetter
from datetime import datetime, timedelta
from string import Template


def retrieveData (startDate, endDate, parameterID, dataTitle,outputFileName, measuredDepth, units, lineValue=None):
    url = 'http://data.chesapeakebay.net/api.JSON/WaterQuality/WaterQuality/{0}/{1}/0,1/6/23/Station/1730/{2}'.format(startDate, endDate, parameterID)
    print(url)
    r = requests.get (url)
    rows = json.loads (r.text)
    filteredRows = []
    for row in rows:
        if row ["Depth"] == measuredDepth:
            filteredRows.append(row)
    sortedlist = sorted(filteredRows, key=itemgetter('SampleDate'))
    fig = px.line(sortedlist, x = "SampleDate", y = "MeasureValue", title = dataTitle, labels = {"MeasureValue": units, "SampleDate": "Dates"})
    if lineValue is not None: #None = null
        fig.add_hline(y=lineValue, line_color="red") #Horizontal line for max levels
    fig.write_image("docs/{0}.png".format(outputFileName))
    return sortedlist

def fillTemplate(filename, datavalues):
    file = open("./templates/"+filename,"rt")
    content = file.read()
    file.close()
    s = Template(content)
    output = s.substitute(datavalues)
    outputFile = open("./docs/"+filename,"wt")
    outputFile.write(output)
    outputFile.close()

def fillParameterTemplate(filename, datavalue, date):
    fillTemplate(filename,{"datavalue": datavalue, "date": date[:10]})

now = datetime.now()
startDate = now - timedelta(days = 365*2)

startFormat = startDate.strftime("%m-%d-%Y")
endFormat = now.strftime("%m-%d-%Y")
oxygen = retrieveData (startFormat, endFormat, 31, "Historical Oxygen Levels", "oxygen", 8, "MG/L", 5)
oxygenIsSafe = oxygen[len(oxygen)-1]["MeasureValue"] >= 5
fillParameterTemplate("oxygen.html", oxygen[len(oxygen)-1]["MeasureValue"], oxygen[len(oxygen)-1]["SampleDate"])

nitrate = retrieveData (startFormat, endFormat, 109, "Historical Total Nitrogen Levels", "nitrate", 0.5, "MG/L", 6)
nitrateIsSafe = nitrate[len(nitrate)-1]["MeasureValue"] <= 6
fillParameterTemplate("nitrate.html", nitrate[len(nitrate)-1]["MeasureValue"], nitrate[len(nitrate)-1]["SampleDate"])

phosphate = retrieveData (startFormat, endFormat, 114, "Historical Total Phosphorous Levels", "phosphate", 0.5, "MG/L", 0.05)
phosphateIsSafe = phosphate[len(phosphate)-1]["MeasureValue"] <= 0.05
fillParameterTemplate("phosphate.html", phosphate[len(phosphate)-1]["MeasureValue"], phosphate[len(phosphate)-1]["SampleDate"])

turbidity = retrieveData (startFormat, endFormat, 85, "Historical Turbidity Levels", "turbidity", 0.5, "Meters", 0.12)
turbidityIsSafe = turbidity[len(turbidity)-1]["MeasureValue"] >= 0.12
fillParameterTemplate("turbidity.html", turbidity[len(turbidity)-1]["MeasureValue"], turbidity[len(turbidity)-1]["SampleDate"])

watertempdata = retrieveData (startFormat, endFormat, 123, "Historical Water Temperature Levels", "temperature", 4, "Degrees Celsius")
fillParameterTemplate("watertemp.html", watertempdata[len(watertempdata)-1]["MeasureValue"], watertempdata[len(watertempdata)-1]["SampleDate"])

isSafe = oxygenIsSafe and nitrateIsSafe and phosphateIsSafe and turbidityIsSafe

fillTemplate("index.html", {
    "safety": "YES" if isSafe else "NO",
    "watertemp": watertempdata[len(watertempdata)-1]["MeasureValue"],
    "phosphate": phosphate[len(phosphate)-1]["MeasureValue"],
    "turbidity": turbidity[len(turbidity)-1]["MeasureValue"],
    "oxygen": oxygen[len(oxygen)-1]["MeasureValue"],
    "nitrate": nitrate[len(nitrate)-1]["MeasureValue"],
    "date": endFormat
})

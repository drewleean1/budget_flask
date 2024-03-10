from flask import Flask, render_template
import base64
from io import BytesIO
import requests
import json 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

app = Flask(__name__, 
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')


def monthlySpendIn(year): 
    response = requests.get('https://budget-drewleean-80248645fdf0.herokuapp.com/expenses/year/' + str(year))
    response = json.loads(response.text)

    spend_by_month= {}
    months = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul",
              "08": "Aug", "09": "Sep", "10":"0ct", "11": "Nov", "12":"Dec"}

    for x in response: 
        if x["amount"] < 0: continue
        try:
            spend_by_month[x["date"][5:7]] += x["amount"]
        except: 
            spend_by_month[x["date"][5:7]] = x["amount"]

    temp = []

    for k in sorted(spend_by_month.keys()): 
        print(type(k))
        temp.append({"month": months[k], "amount":spend_by_month[k]})

    data = {"monthly": temp}
    
    fig = Figure()

    df = pd.DataFrame(data['monthly'])
    d = df.plot.bar(x="month", y="amount")

    return d

@app.route("/createBar/<year>")
def createBar(year):
    plot = monthlySpendIn(year)
    buf = BytesIO()
    plot.figure.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

if __name__ == "__main__": 
    app.run(host='0.0.0.0')


#Used documentation (non-exhaustive):
#https://stackoverflow.com/questions/44618376/easiest-way-to-plot-data-from-json-with-matplotlib    
#https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
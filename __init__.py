from flask import Flask, render_template
import base64
from io import BytesIO
import requests
import json 
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

app = Flask(__name__, 
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

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

    for x in spend_by_month.keys(): 
        spend_by_month[x] = round(spend_by_month[x], 2)

    temp = []
    exes = []
    wives =[]

    for k in sorted(spend_by_month.keys()): 
        temp.append({"month": months[k], "amount": spend_by_month[k]})
        exes.append(months[k])
        wives.append(spend_by_month[k])

    data = {"monthly": temp}
    
    fig = Figure()

    df = pd.DataFrame(data['monthly'])
    d = df.plot.bar(x="month", y="amount")
    addlabels(exes, wives)

    return d

def catSpendIn(month, year): 
    response = requests.get('https://budget-drewleean-80248645fdf0.herokuapp.com/expenses/month/' + str(month) + '/year/' +str(year)) 
    response = json.loads(response.text)
    
    spend_by_cat = {}

    for x in response: 
        if x["amount"] < 0: continue
        try: 
            spend_by_cat[x["category"]] += x["amount"]
        except: 
            spend_by_cat[x["category"]] = x["amount"]

    for x in spend_by_cat.keys(): 
        spend_by_cat[x] = round(spend_by_cat[x], 0)

    temp = []
    exes = []
    wives = []

    for k in spend_by_cat.keys(): 
        temp.append({"category": k, "amount": spend_by_cat[k]})
        exes.append(k)
        wives.append(spend_by_cat[k])


    data = {"category": temp}

    fig = Figure()
    df = pd.DataFrame(data["category"])
    d = df.plot.bar(x="category", y = "amount")
    addlabels(exes,wives)

    return d

@app.route("/createBar/<year>")
def createBar(year):
    plot = monthlySpendIn(year)
    buf = BytesIO()
    plot.figure.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

@app.route("/catBar/<month>/<year>")
def categoryBar(month, year): 
    plot = catSpendIn(month, year)
    buf = BytesIO()
    plot.figure.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

if __name__ == "__main__": 
    app.run(host='0.0.0.0', port = int(os.environ.get('PORT', 33507)))



#Used documentation (non-exhaustive):
#https://stackoverflow.com/questions/44618376/easiest-way-to-plot-data-from-json-with-matplotlib    
#https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
#https://stackoverflow.com/questions/17260338/deploying-flask-with-heroku
#https://cs.wellesley.edu/~webdb/lectures/flask/flask.html\
#https://flask.palletsprojects.com/en/3.0.x/tutorial/deploy/
#https://www.geeksforgeeks.org/adding-value-labels-on-a-matplotlib-bar-chart/
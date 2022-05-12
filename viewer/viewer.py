from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for
)
import json
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from . import postgresClient

bp = Blueprint("viewer", __name__)
dbClient = postgresClient.Client()

@bp.route("/test")
def test():
    return render_template("home.html")


@bp.route("/", methods=['GET', 'POST'])
def home():
    print("home with {}".format(request.method))
    if request.method == 'GET':
        return redirect(url_for('viewer.timelines', timeinterval = "3days"))
    else:
        # return redirect(url_for('viewer.test'))
        # return render_template('home.html')
        return redirect(url_for('viewer.test'))
        print(request.json.get("val"))
        timeinterval = request.json.get("val")
        #return {}
        # timeinterval = request.json.get("val")
        # print(timeinterval) 
        return redirect(url_for('viewer.timelines', timeinterval = timeinterval))

@bp.route("/timelines/<string:timeinterval>", methods=['GET', 'POST'])
def timelines(timeinterval):
    print("timelines with timeinterval: {}, {}".format(timeinterval, request.method))
    user = request.args.get('user')
    print(user)
    if timeinterval == None:
        timeinterval = "3days"
    
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02)

    time, values = dbClient.getTimeSeries("temperature", timeinterval, "OUT", "BME280")   
    fig.append_trace(go.Scatter(x=time, y=values), row=1, col=1)
    time, values = dbClient.getTimeSeries("temperature", timeinterval, "HOME-LR")   
    fig.append_trace(go.Scatter(x=time, y=values), row=1, col=1)

    time, values = dbClient.getTimeSeries("humidity", timeinterval, "OUT")
    fig.append_trace(go.Scatter(x=time, y=values), row=2, col=1)
    time, values = dbClient.getTimeSeries("pressure", timeinterval, "OUT", "BME280")
    fig.append_trace(go.Scatter(x=time, y=values), row=3, col=1)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # print(graphJSON)
    return render_template('timelines.html', graphJSON=graphJSON, btnChecked=timeinterval)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

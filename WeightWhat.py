import base64
import urllib
import numpy as np
import io
import os
import psycopg2
import functools
import matplotlib
from flask import Flask, render_template, Response, request, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_datepicker import datepicker
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, FloatField
from wtforms.validators import Required
from pprint import pprint
matplotlib.use("agg")
from matplotlib import pyplot as plt
from weightwhatclasses.wwforms import LoginForm, DateForm
from weightwhatclasses.db_models import Measurement, User, LoginData
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


# establish path for db
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
dp = datepicker(app)
datepicker.picker(dp, id='.dp', maxDate='2019-07-01', minDate='2018-10-01', btnsId='dpbtn')
# app config
app.config["SECRET_KEY"] = "RoundAndProud"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# add Migrate for Alembc wrapper
migrate = Migrate(app, db)


@app.route('/', methods=['POST', 'GET'])
def index():
    d_form = DateForm()
    log_form = LoginForm()
    return render_template("index.html", log_form=log_form, date_form=d_form)


@app.route('/plot')
def plot_png():
    """
    A much cleaner rednering of the plot here:
    https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    :return:
    """

    plot = get_data()
    output = io.BytesIO()
    plot.savefig(output, format='png')
    output.seek(0)
    img = base64.b64encode(output.read())
    png = 'data:image/png;base64,' + urllib.parse.quote(img)
    #FigureCanvas(plot).print_png(output)
    return render_template("plot.html", img=png)


def array_to_plot(func):
    @functools.wraps(func)
    def wrapper():
        arr = func()
        serial_arr = arr[0]
        dates_arr = arr[1]
        weight_arr = arr[2]
        """
        fig = Figure()
        axis = fig.add_subplot(1,1,1)
        axis.plot(dates_arr, weight_arr)
        """
        #plt.plot(serial_arr, label="serial")
        #plt.plot(dates_arr, label='dates')
        #plt.plot(weight_arr, label='weight')
        #plt.plot(dates_arr, weight_arr)
        plt.plot_date(dates_arr, weight_arr, xdate=True, ydate=False, drawstyle='steps')
        plt.xlabel("Dates")
        plt.ylabel("Weight")
        plt.title("Weight plot")
        #fig_size = plt.rcParams["figure.figsize"]
        #fig_size[0] = 14
        #fig_size[1] = 9
        #plt.rcParams["figure.figsize"] = fig_size
        return plt
    return wrapper


def convert_data_to_array(func):
    @functools.wraps(func)
    def wrapper():
        inpt = func()
        serial = np.asarray([s[0] for s in inpt])
        dates = np.asarray([d[1] for d in inpt])
        weight = np.asarray([w[2] for w in inpt])
        return serial, dates, weight
    return wrapper


@array_to_plot
@app.before_first_request
@convert_data_to_array
def get_data():
    # connection config
    dbname = 'newton'
    user_name = 'newton'
    host_type = '/tmp/'
    host_type = '/tmp/'

    # create connection command
    pg_command = "dbname={dbname} user={user} host={host}".format(dbname=dbname, user=user_name, host=host_type)

    # establish connection
    conn = psycopg2.connect(pg_command)

    # create cursor on the connection
    cursor = conn.cursor()

    # define query
    query = "SELECT * FROM waga;"

    # execute query
    cursor.execute(query)

    # get all data from the query
    data = cursor.fetchall()

    pprint(data)

    # define data series
    serial = [s[0] for s in data]
    dates = [d[1] for d in data]
    weight = [w[2] for w in data]
    print(serial, "\n", dates, "\n", weight)
    return data


if __name__ == '__main__':
    app.run(debug=True)

# -*- coding: utf-8 -*-

import flask
from flask import Flask, request, json,render_template,redirect,url_for,jsonify,json
import datetime
import os
import sys
app = Flask(__name__)
app.config['DEBUG'] = True
import collections


# check whether the directory has the json file or not

try:
    with open('data.json', 'r') as data_file:
        data_file = json.load(data_file)
except FileNotFoundError:
    data_file = collections.defaultdict(list)
    # create the keys
    key_list = ['Time_Duration',
                'Temperature' ,
                'Date',
                'Distance',
                'Energy_level',
                'weather_type',
                'time_day',
                'Date']
    for i in key_list:
        data_file[i] = []

# Create the list for weather type, time of day and energy level
weather_type = ['Rainy','overcast','dense cloud','sunny','windy','Hot','Humid','cool']
energy_level = ['Exhausted','Low','Satisfactory','Feeling Good']
time_day = ['Early Morning','Morning','Afternoon','Evening','After Dark']

""" read the list of users"""
@app.route("/")        # Standard Flask endpoint
def homepage():
    return render_template("user_form.html",weather_type = weather_type, energy_level = energy_level,
        time_day = time_day)

@app.route("/application_history")
def application_history():
    application_history_url = plot_url
    return redirect(webbrowser.open_new_tab(application_history_url))

@app.route('/addDetails', methods=['POST'])
def addDetails():
    data = request.form
    Day = data['Day']
    Time_Duration = data['Duration']
    try:
        Temperature = float(data['Temperature'])
    except ValueError:
        Temperature = None
    Date = datetime.datetime.now()
    try:
        Distance = float(data['Distance_Km'])
    except ValueError:
        Distance = None
    Energy_level = data['Energy_Level']
    weather_type = data['weather_type']
    time_day = data['time_day']

    # Save the data
    json_data = dict(Time_Duration = Time_Duration,
                    Temperature = Temperature,
                    Date = Date,
                    Distance = Distance,
                    Energy_level = Energy_level,
                    weather_type = weather_type,
                    time_day = time_day)

    json_keys = list(json_data.keys())
    for i in range(len(json_keys)):
        data_file[json_keys[i]].append(json_data[json_keys[i]])
    with open("data.json","w") as outfile:
        json.dump(data_file, outfile)
    return render_template('user_form_response.html')

@app.route('/application_details', methods=['GET'])
def application_details():
    return render_template('application_table.html')

@app.route('/delete_form', methods=['GET'])
def delete_form():
    return render_template('delete_details.html')



@app.route('/delete', methods=['POST'])
def delete():
    templateData = {}
    connection = mysql.connector.connect(host=db_auth['host'], 
                                         user=db_auth['dbuser'],
                                         port=3306,
                                         passwd=db_auth['db_pass'], 
                                         db=db_auth['dbname'])

    cursor = connection.cursor()    
    data = request.form
    cursor.execute("""delete from company_email1 where Company_Name=%s;""",(data['Company'],))
    connection.commit()
    cursor.close()
    connection.close()    
    templateData['redirect_url'] = url_for('application_details')
    return render_template('delete_details_response.html',**templateData)

@app.route('/index_get_data', methods=['GET'])
def stuff():
    import requests
    response = requests.get(url)    
    columns = response.json()['columns']    
    collection = [dict(zip(columns, response.json()['data'][i])) for i in range(len(response.json()['data']))]
    data = {"data": collection}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5001)

import trafiklab
from flask import Flask, render_template, abort

app = Flask(__name__)

# Routes

@app.route('/')
def home():
    skogas = trafiklab.get_station_data(740000757)
    fabodvagen = trafiklab.get_station_data(740045561)
    if skogas == False or fabodvagen == False:
        abort(404)
    return render_template('main.html', tables=[skogas, fabodvagen])

@app.route('/station/<station_id>')
def station(station_id):
    station_data = trafiklab.get_station_data(station_id=station_id)
    if station_data == False:
        abort(404)
    return render_template('main.html', tables=[station_data])

@app.route('/json/<station_id>')
def json(station_id):
    station_data = trafiklab.get_data(station_id=station_id)
    if station_data == False:
        abort(404)
    return station_data

# Starta webbappen när man kör python-filen
if __name__ == "__main__":
    app.run(debug=True)
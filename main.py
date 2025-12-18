import trafiklab
from flask import Flask, render_template

# Skapa en Flask-app
app = Flask(__name__)

# Ange vad som händer när man går in på startsidan '/'
@app.route('/')
def home():
    skogas = trafiklab.get_station_data(740000757)
    fabodvagen = trafiklab.get_station_data(740045561)
    return render_template('main.html', tables=[skogas, fabodvagen])

@app.route('/json')
def json():
    station_data = trafiklab.get_station_data()
    return station_data

# Starta webbappen när man kör python-filen
if __name__ == "__main__":
    app.run(debug=True)
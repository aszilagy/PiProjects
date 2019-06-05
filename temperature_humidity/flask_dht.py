import dht11_example as dt
from flask import Flask, render_template, request, session, redirect, url_for
from passlib.hash import sha256_crypt as sha
import configparser as cf
from pprint import pprint

app = Flask(__name__)
app.secret_key = b'0a0s9dkk1l$#1340!%%91'

@app.route('/', methods=['GET'])
def main():
    tReadObj = dt.TempReader()
    rDay, rTime, temp, rHumid = dt.TempReader.getTemp(tReadObj)
    return render_template('index.html', roomDay=rDay, roomTime=rTime, roomTemp=temp, roomHumidity=rHumid)

@app.route('/get_temp/')
def test_temp():
    tReadObj = dt.TempReader()
    rDay, rTime, temp, rHumid = dt.TempReader.getTemp(tReadObj)
    return '{} {} {} {}'.format(rDay, rTime, temp, rHumid)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 80
    app.run(debug=True, host=host, port=port)


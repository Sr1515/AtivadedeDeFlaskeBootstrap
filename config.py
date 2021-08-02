from flask import Flask
import psycopg2


app = Flask(__name__)
app.secret_key = 'concessionaria2021'
db = psycopg2.connect(
    database='concessionaria', user='postgres', password='123', host='127.0.0.1', port='5432')


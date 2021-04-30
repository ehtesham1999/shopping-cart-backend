from flask import Flask
from os import environ
from dotenv import load_dotenv
load_dotenv('.env')
from pymongo import MongoClient

app = Flask(__name__)
cluster = MongoClient(environ.get('DATABASE_URL'))


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

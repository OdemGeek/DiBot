from flask import Flask
from threading import Thread
import io

app = Flask('')


@app.route('/')
def home():
    data = None
    with open('index.html', 'r') as file:
        data = file.read().replace('\n', '')
    return data
    #return "If you are reading this, it means that you somehow found this page. Well then I can only recommend to subscribe to me :) \n odemgeek.github.io\ntwitter.com/OdemGeek\nwww.youtube.com/c/OdemGeek"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()

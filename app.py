from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'welcome to shopping app!'


if __name__ == '__main__':
    app.run()

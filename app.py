from flask import Flask, render_template, request, redirect,jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)


# Connect to the database
engine = create_engine("mysql+mysqlconnector://flask:root@localhost/flask")
# Test the connection
cur = engine.connect()

import routes

@app.route('/admin/')
@app.route('/admin')
def admin():
    return render_template('admin/dashboard/index.html')


if __name__ == '__main__':
    app.run()

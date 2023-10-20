from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(host='localhost',
                             user='root',
                             passwd='',
                             db='flask',
                             port=3306)

cur = db.cursor(dictionary=True)


import routes

@app.route('/admin/')
@app.route('/admin')
def admin():
    return render_template('admin/dashboard/index.html')


if __name__ == '__main__':
    app.run()

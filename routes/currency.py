from app import app, render_template, request, redirect, db, cur
import sqlite3 as sql


@app.route('/admin/currency')
def currency():
    cur.execute("SELECT * FROM currency")
    rows = cur.fetchall()
    return render_template('admin/currency/currency.html', module_key='currency', rows=rows)

# Add Currency
@app.route('/admin/add_currency_index')
def addCurrencyIndex():
    return render_template('admin/currency/add_currency.html')

@app.route('/admin/add_currency', methods=['POST'])
def add_currency():
    msg = ""
    if request.method == "POST":
        try:
            code = request.form['code']
            symbol = request.form['symbol']
            is_default = request.form['is_default']
            sell_out_price = request.form['sell_out_price']

            insert_query = "INSERT INTO currency (code, symbol, is_default, sell_out_price) VALUES (%s, %s, %s, %s)"
            data = (code, symbol, is_default, sell_out_price)

            with db.cursor() as cursor:
                cursor.execute(insert_query, data)
                db.commit()
                
            msg = "Record successfully added"
            return redirect('/admin/currency')
        except db.Error as err:
            db.rollback()
            msg = "Error in insert operation: " + str(err)
    return msg

# Edit Currency
@app.route('/admin/edit_currency_index/<int:id>')
def editCurrencyIndex(id):
    cur.execute("SELECT * FROM currency WHERE id = %s", (id,))
    rows = cur.fetchall()
    return render_template('admin/currency/edit_currency.html', rows=rows)

@app.route('/admin/edit_currency', methods=['POST'])
def edit_currency():
    if request.method == "POST":
        try:
            id = request.form['id']
            code = request.form['code']
            symbol = request.form['symbol']
            is_default = request.form['is_default']
            sell_out_price = request.form['sell_out_price']

            update_query = "UPDATE currency SET code=%s, symbol=%s, is_default=%s, sell_out_price=%s WHERE id=%s"
            data = (code, symbol, is_default, sell_out_price, id)
            
            with db.cursor() as cursor:
                cursor.execute(update_query, data)
                db.commit()
            msg = "Record successfully updated"
            return redirect('/admin/currency')
        except db.Error as err:
            db.rollback()
            msg = "Error in update operation: " + str(err)
    return msg

# Delete Currency
@app.route('/admin/delete_currency', methods=['POST'])
def delete_currency():
    if request.method == "POST":
        try:
            id = request.form['id']

            delete_query = "DELETE FROM currency WHERE id = %s"
            
            with db.cursor() as cursor:
                cursor.execute(delete_query, (id,))
                db.commit()
            msg = "Record successfully deleted"
            return redirect('/admin/currency')
        except db.Error:
            db.rollback()
            msg = "Error in delete operation"
    return msg

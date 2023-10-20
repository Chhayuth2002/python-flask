from app import app, render_template, request, redirect, db, cur
import sqlite3 as sql


@app.route('/admin/customer')
def customer():
    cur.execute("SELECT * FROM customer")
    rows = cur.fetchall()
    return render_template('admin/customer/customer.html', module_key='customer', rows=rows)

# Add Customer
@app.route('/admin/add_customer_index')
def addCustomerIndex():
    return render_template('admin/customer/add_customer.html')

@app.route('/admin/add_customer', methods=['POST'])
def add_customer():
    msg = ""
    if request.method == "POST":
        try:
            name = request.form['name']
            status = request.form['status']

            insert_query = "INSERT INTO customer (name, status) VALUES (%s, %s)"
            data = (name, status)

            with db.cursor() as cursor:
                cursor.execute(insert_query, data)
                db.commit()
                
            msg = "Record successfully added"
            return redirect('/admin/customer')
        except db.Error as err:
            db.rollback()
            msg = "Error in insert operation: " + str(err)
    return msg

# Edit Customer
@app.route('/admin/edit_customer_index/<int:id>')
def editCustomerIndex(id):
    cur.execute("SELECT * FROM customer WHERE id = %s", (id,))
    rows = cur.fetchall()
    return render_template('admin/customer/edit_customer.html', row=rows)

@app.route('/admin/edit_customer', methods=['POST'])
def edit_customer():
    if request.method == "POST":
        try:
            id = request.form['id']
            name = request.form['name']
            status = request.form['status']

            update_query = "UPDATE customer SET name=%s, status=%s WHERE id=%s"
            data = (name, status, id)
            
            with db.cursor() as cursor:
                cursor.execute(update_query, data)
                db.commit()
            msg = "Record successfully updated"
            return redirect('/admin/customer')
        except db.Error as err:
            db.rollback()
            msg = "Error in update operation: " + str(err)
    return msg

# Delete Customer
@app.route('/admin/delete_customer', methods=['POST'])
def delete_customer():
    if request.method == "POST":
        try:
            id = request.form['id']

            delete_query = "DELETE FROM customer WHERE id = %s"
            
            with db.cursor() as cursor:
                cursor.execute(delete_query, (id,))
                db.commit()
            msg = "Record successfully deleted"
            return redirect('/admin/customer')
        except db.Error:
            db.rollback()
            msg = "Error in delete operation"
    return msg

from app import app, render_template, request, redirect, db, cur
import sqlite3 as sql

@app.route('/admin/user')
def user():
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    return render_template('admin/user/user.html', module_key='user', rows=rows)

# Add User
@app.route('/admin/add_user_index')
def addUserIndex():
    return render_template('admin/user/add_user.html')

@app.route('/admin/add_user', methods=['POST'])
def add_user():
    msg = ""
    if request.method == "POST":
        try:
            name = request.form['name']
            status = request.form['status']

            insert_query = "INSERT INTO user (name, status) VALUES ( %s, %s)"
            data = (name, status)

            with db.cursor() as cursor:
                cursor.execute(insert_query, data)
                db.commit()
                
            msg = "Record successfully added"
            return redirect('/admin/user')
        except db.Error as err:
            db.rollback()
            msg = "Error in insert operation: " + str(err)
    return msg

# Edit User
@app.route('/admin/edit_user_index/<int:id>')
def editUserIndex(id):
    cur.execute("SELECT * FROM user WHERE id = %s", (id,))
    rows = cur.fetchall()
    return render_template('admin/user/edit_user.html', rows=rows)

@app.route('/admin/edit_user', methods=['POST'])
def edit_user():
    if request.method == "POST":
        try:
            id = request.form['id']
            name = request.form['name']
            status = request.form['status']

            update_query = "UPDATE user SET name=%s, status=%s WHERE id=%s"
            data = (name, status, id)
            
            with db.cursor() as cursor:
                cursor.execute(update_query, data)
                db.commit()
            msg = "Record successfully updated"
            return redirect('/admin/user')
        except db.Error as err:
            db.rollback()
            msg = "Error in update operation: " + str(err)
    return msg

# Delete User
@app.route('/admin/delete_user', methods=['POST'])
def delete_user():
    if request.method == "POST":
        try:
            id = request.form['id']

            delete_query = "DELETE FROM user WHERE id = %s"
            
            with db.cursor() as cursor:
                cursor.execute(delete_query, (id,))
                db.commit()
            msg = "Record successfully deleted"
            return redirect('/admin/user')
        except db.Error:
            db.rollback()
            msg = "Error in delete operation"
    return msg

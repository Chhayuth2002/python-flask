from app import app, render_template, request, redirect
import sqlite3 as sql


@app.route('/admin/student')
def student():
    con = sql.connect("ss34.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from students")
    rows = cur.fetchall()
    return render_template('admin/student/student.html', module_key='student', rows=rows)


@app.route('/admin/add_student_index')
def addStudentIndex():
    return render_template('admin/student/add_student.html')


@app.route('/admin/edit_student_index/<string:student_name>')
def editStudentIndex(student_name):
    #
    con = sql.connect("ss34.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(f"select * from students where name = '{student_name}'")
    rows = cur.fetchall()
    return render_template('admin/student/edit_student.html', rows=rows)


@app.route('/admin/delete_student', methods=['POST'])
def delete_student():
    if request.method == "POST":
        try:
            name = request.form['name']
            with sql.connect("ss34.db") as con:
                cur = con.cursor()
                cur.execute(f"DELETE FROM students WHERE name = '{name}'")
                con.commit()
                msg = "Record successfully deleted"
                return redirect('/admin/student')
        except:
            con.rollback()
            msg = "error in insert operation"


@app.route('/admin/edit_student', methods=['POST'])
def edit_student():
    if request.method == "POST":
        try:
            name = request.form['name']
            gender = request.form['gender']
            address = request.form['address']
            phone = request.form['phone']

            with sql.connect("ss34.db") as con:
                cur = con.cursor()
                cur.execute(f"update students set "
                            f"gender = '{gender}', "
                            f"address = '{address}', "
                            f"phone = '{phone}' "
                            f"where name = '{name}'")
                con.commit()
                msg = "Record successfully updated"
                return redirect('/admin/student')
        except:
            con.rollback()
            msg = "error in insert operation"


@app.route('/admin/add_student', methods=['POST'])
def add_student():
    if request.method == "POST":
        try:
            name = request.form['name']
            gender = request.form['gender']
            address = request.form['address']
            phone = request.form['phone']

            with sql.connect("ss34.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, gender, address, phone) VALUES (?, ?, ?, ?)",
                            (name, gender, address, phone))
                con.commit()
                msg = "Record successfully added"
                return redirect('/admin/student')
        except sql.IntegrityError as e:
            con.rollback()
            msg = f"Error in insert operation: {str(e)}"
        finally:
            con.close()
    return msg


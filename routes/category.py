from app import app, render_template, request, redirect, cur, db
import sqlite3 as sql


@app.route('/admin/category')
def category():
    cur.execute("select * from category")
    rows = cur.fetchall()
    return render_template('admin/category/category.html', module_key='category', rows=rows)


# Add Category
@app.route('/admin/add_category_index')
def addCategoryIndex():
    return render_template('admin/category/add_category.html')


@app.route('/admin/add_category', methods=['POST'])
def add_category():
    msg = ""
    if request.method == "POST":
        try:
            name = request.form['category_name']
            status = request.form['status']

            insert_query = "INSERT INTO category (category_name, status) VALUES (%s, %s)"
            data = (name, status)

            with db.cursor() as cursor:
                cursor.execute(insert_query, data)
                db.commit()
                
            msg = "Record successfully added"
            return redirect('/admin/category')
        except db.Error as err:
            db.rollback()
            msg = "Error in insert operation: " + str(err)
    return msg

# Edit Product


@app.route('/admin/edit_category_index/<int:category_id>')
def editCategoryIndex(category_id):
    cur.execute(
        f"select * from category where category_id = '{category_id}'")
    rows = cur.fetchall()
    return render_template('admin/category/edit_category.html', rows=rows)


@app.route('/admin/edit_category', methods=['POST'])
def edit_category():
    if request.method == "POST":
        try:
            id = request.form['category_id']
            name = request.form['category_name']
            status = request.form['status']
            
            
            update_query = "UPDATE category SET category_name=%s, status=%s WHERE category_id=%s"
            data = (name, status, id)
            with db.cursor() as cursor:
                cursor.execute(update_query, data)
                db.commit()
            msg = "Record successfully updated"
            return redirect('/admin/category')
        except db.Error as err:
            db.rollback()
            msg = "Error in update operation: " + str(err)
    return msg

# Delete Category


@app.route('/admin/delete_category', methods=['POST'])
def delete_category():
    if request.method == "POST":
        try:
            name = request.form['category_name']

            delete_query = "DELETE FROM category WHERE category_name = %s"
            
            with db.cursor() as cursor:
                cursor.execute(delete_query, (name,))
                db.commit()
            msg = "Record successfully deleted"
            return redirect('/admin/category')
        except:
            db.rollback()
            msg = "error in delete operation"
    return msg

from app import app, render_template, request, redirect, db, cur
import sqlite3 as sql


@app.route('/admin/product')
def product():
    cur.execute("SELECT * FROM product JOIN category ON product.category_id = category.category_id ORDER BY product.product_id")
    rows = cur.fetchall()
    return render_template('admin/product/product.html', module_key='product', rows=rows)

# Add Product
@app.route('/admin/add_product_index')
def addProductIndex():
    cur.execute("select * from category")
    rows = cur.fetchall()
    return render_template('admin/product/add_product.html', rows = rows)

@app.route('/admin/add_product', methods=['POST'])
def add_product():
    msg = ""
    if request.method == "POST":
        try:
            product_name = request.form['product_name']
            price = request.form['price']
            cost = request.form['cost']
            status = request.form['status']
            category_id = request.form['category_id']

            insert_query = "INSERT INTO product (product_name, price, cost, status, category_id) VALUES ( %s, %s, %s, %s, %s)"
            data = (product_name, price, cost, status, category_id)

            with db.cursor() as cursor:
                cursor.execute(insert_query, data)
                db.commit()
                
            msg = "Record successfully added"
            return redirect('/admin/product')
        except db.Error as err:
            db.rollback()
            msg = "Error in insert operation: " + str(err)
    return msg

# Edit Product
@app.route('/admin/edit_product_index/<int:product_id>')
def editProductIndex(product_id):
    cur.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
    rows = cur.fetchall()
    cur.execute("SELECT * FROM product natural join category")
    row = cur.fetchall()
    return render_template('admin/product/edit_product.html', rows=rows, res = row)

@app.route('/admin/edit_product', methods=['POST'])
def edit_product():
    if request.method == "POST":
        try:
            product_id = request.form['product_id']
            product_name = request.form['product_name']
            price = request.form['price']
            cost = request.form['cost']
            status = request.form['status']
            category_id = request.form['category_id']

            update_query = "UPDATE product SET product_name=%s, price=%s, cost=%s, status=%s, category_id=%s WHERE product_id=%s"
            data = (product_name, price, cost, status, category_id, product_id)
            
            with db.cursor() as cursor:
                cursor.execute(update_query, data)
                db.commit()
            msg = "Record successfully updated"
            return redirect('/admin/product')
        except db.Error as err:
            db.rollback()
            msg = "Error in update operation: " + str(err)
    return msg

# Delete Product
@app.route('/admin/delete_product', methods=['POST'])
def delete_product():
    if request.method == "POST":
        try:
            product_id = request.form['product_id']

            delete_query = "DELETE FROM product WHERE product_id = %s"
            
            with db.cursor() as cursor:
                cursor.execute(delete_query, (product_id,))
                db.commit()
            msg = "Record successfully deleted"
            return redirect('/admin/product')
        except db.Error:
            db.rollback()
            msg = "Error in delete operation"
    return msg

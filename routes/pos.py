from app import app, render_template, cur, jsonify, text


@app.route('/pos')
def pos_index():
    return render_template('pos_screen.html')



@app.route('/getAllCategory')
def getAllCategory():
    categories = cur.execute(text('SELECT * from category;'))
    cur.commit()

    json_string = [{'id': category.category_id, 'name': category.category_name} for category in categories]
    
    return json_string

@app.route('/getAllProduct')
def getAllProduct():
    products = cur.execute(text('SELECT product.*, category.* FROM product JOIN category ON product.category_id = category.category_id ;'))
    cur.commit()
    
    json_string = []
    for product in products:
        json_string.append(
            {
                'id': product.product_id,
                'name': product.product_name,
                'discount': product.discount,
                'price': product.price,
                'image': product.image,
                'category_name':product.category_name,
                'category_id':product.category_id,
            }
        )

    return json_string


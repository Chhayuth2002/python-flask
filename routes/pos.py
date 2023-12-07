from app import app, render_template, jsonify, text, engine


@app.route('/pos')
def pos_index():
    return render_template('pos_screen.html')



@app.route('/getAllCategory')
def getAllCategory():
    try:
        con = engine.connect()

        categories = con.execute(text('SELECT * from category;'))
        con.commit()

        json_string = [{'id': category.category_id, 'name': category.category_name} for category in categories]
        
        return json_string
    finally:
        con.close()
        

@app.route('/getAllProduct')
def getAllProduct():
    try:
        con = engine.connect()
        
        products = con.execute(text('SELECT product.*, category.* FROM product JOIN category ON product.category_id = category.category_id ;'))
        categories = con.execute(text('SELECT * from category;'))
        con.commit()
        category_list = [{'id': category.category_id, 'name': category.category_name} for category in categories]
        
        product_list = []
        for product in products:
            product_list.append(
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

        result = [
            product_list,
            category_list
        ]
        
        return result
    
    finally:
        con.close()



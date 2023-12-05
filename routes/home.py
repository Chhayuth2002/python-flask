from  app import app, render_template, request, cur, text

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')



# @app.route('/product_detail/<string:name>/<string:category>/<string:price>/<string:image>')
# def product_detail(name, category, price, image):
#     return render_template('product_detail.html', name=name, category=category, price=price, image=image)



